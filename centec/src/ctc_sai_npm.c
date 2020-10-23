/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"
#include "sainpm.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_port.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_npm.h"
#include "ctc_sai_bridge.h"
#include "ctcs_api.h"


typedef struct ctc_sai_npm_master_s
{
    uint32 npm_reserved_ingress_acl_group_id;
    uint32 npm_reserved_egress_acl_group_id;
    
} ctc_sai_npm_master_t;

ctc_sai_npm_master_t* p_ctc_sai_npm[CTC_MAX_LOCAL_CHIP_NUM] = {NULL};


typedef struct  ctc_sai_npm_master_wb_s
{
    /*key*/
    uint32 lchip;
    uint32 calc_key_len[0];
    
    /*data*/    
    uint32 npm_reserved_ingress_acl_group_id;
    uint32 npm_reserved_egress_acl_group_id;
    
}ctc_sai_npm_master_wb_t;




#define ________SAI_NPM_PACKET________


uint8 npm_pkt_l2_header[22] =
{
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x81, 0x00, 0x00, 0x00,
    0x81, 0x00, 0x00, 0x00,
};
    

uint8 npm_pkt_ipv4_header[9600] =
{
    0x08, 0x00, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x11, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
};

uint8 npm_pkt_ipv6_header[9600] =
{
    0x86, 0xDD, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x11, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
};


#define ________SAI_NPM_CHECKSUM_________


static sai_status_t
_ctc_sai_npm_calculate_ip_header_checsum(uint8 addr_family, int32 *checksum_ptr, uint8 *pkt, uint8 vlan_num)
{
    int32   i = 0;
    int32   j = 0;
    int32   k = 0;    
    int32 buff[20] = {0};
    int32 checksum = 0;
    
    if(addr_family == 4)
    {
        for (i = 0; i < 20; i = i + 2 )
        {   
            j = i + 14 + vlan_num*4;
            buff[k] = (pkt[j]<<8) + pkt[j+1];
            k++;
        }

        for (i = 0; i < 10; i++ )
        {   
            checksum = checksum + buff[i];
        }        

        checksum = (checksum>>16) + (checksum & 0xffff);
        checksum = checksum + (checksum>>16);
        checksum = ~checksum;
        *checksum_ptr = checksum;    
    }

    return SAI_STATUS_SUCCESS;

}

static sai_status_t
_ctc_sai_npm_calculate_udp_header_checsum(uint8 addr_family, int32 *checksum_ptr , uint32 pkt_len, uint32 ipaddr_offset, uint32 udplen_offset, uint32 udphead_offset, uint32 npm_data_offset, uint8 *pkt  )
{
    int32   i = 0;
    int32   j = 0; 
    int32   a =0;
    int32 buff[4800] = {0};
    int32 checksum = 0;   
    int32 multiple = 0;
      
    multiple = (addr_family == 4)?4:16;    // multiple of 16bit   
    
    // pseudo header

    //ipsa and ipda
    for (i = 0; i < multiple ; i++ )
    {
        buff[a++] = (pkt[ipaddr_offset]<<8) + pkt[ipaddr_offset+1];
        ipaddr_offset = ipaddr_offset + 2;
    }

    // protocol
    buff[a++] = 17;

    // udp length
    buff[a++] = (pkt[udplen_offset]<<8) + pkt[udplen_offset+1];

    
    // udp header
    for (i = 0; i < 4 ; i++ )
    {
        buff[a++] = (pkt[udphead_offset]<<8) + pkt[udphead_offset+1];
        udphead_offset = udphead_offset + 2;
    }

    // udp data            
    for (i = 0; i < pkt_len - npm_data_offset ; i = i + 2 )
    {   
        j = i + npm_data_offset;                    
        buff[a++] = (pkt[j]<<8) + pkt[j+1];
    }
    
    // calc checksum
    
    for (i = 0; i < a ; i++ )
    {   
        checksum = checksum + buff[i];
    }        

    checksum = (checksum>>16) + (checksum & 0xffff);
    checksum = checksum + (checksum>>16);
    checksum = ~checksum;
    *checksum_ptr = checksum; 

    return SAI_STATUS_SUCCESS;

}


static sai_status_t
_ctc_sai_npm_test_ipv4_packet(ctc_sai_npm_t *p_npm_attr, ctc_npm_cfg_t *p_npm, uint8 *pkt, uint8 vlan_num)
{
    p_npm->pkt_format.pkt_header = (void*)pkt;
    p_npm->pkt_format.header_len = NPM_PACKET_BASE_HEADER_LENGTH_IPV4 + vlan_num*4;

    return SAI_STATUS_SUCCESS;
}



static sai_status_t
_ctc_sai_npm_test_ipv6_packet(ctc_sai_npm_t *p_npm_attr, ctc_npm_cfg_t *p_npm, uint8 *pkt, uint8 vlan_num)
{
    p_npm->pkt_format.pkt_header = (void*)pkt;
    p_npm->pkt_format.header_len = NPM_PACKET_BASE_HEADER_LENGTH_IPV6 + vlan_num*4;

    return SAI_STATUS_SUCCESS;
}


sai_status_t
_ctc_sai_npm_mapping_npm_session(ctc_sai_npm_t *p_npm_attr, ctc_npm_cfg_t *p_npm_cfg)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint16          udp_src_port = 0;
    uint16          udp_dst_port = 0;
    uint16          ip_header_lenth = 0;
    uint16          udp_header_lenth = 0;    
    uint32_t        ipv4_addr_tmp = 0;
    ipv6_addr_t     ipv6_sa_addr = {0};
    ipv6_addr_t     ipv6_da_addr = {0};
    mac_addr_t      mac_addr_tmp = {0};
        
    uint8 vlan_num = 0;
    uint32 l2_header_len = 0;
    uint32 l3_header_len = 0;
    uint8 tmp_pkt[9600] = {0};        
    
    int32 checksum = 0;
    uint16 pkt_checksum =0;
    uint8 tos = 0;
    

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);
    CTC_SAI_PTR_VALID_CHECK(p_npm_cfg);


    if(p_npm_attr->outer_vlan)
    {
        vlan_num++;
    }
    if(p_npm_attr->inner_vlan)
    {
        vlan_num++;
    }

    if ((p_npm_attr->packet_length < (64 + vlan_num*4)) && p_npm_attr->ip_addr_family == 4 )
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        return status;
    }

    if ((p_npm_attr->packet_length < (72 + vlan_num*4)) && p_npm_attr->ip_addr_family == 6 )
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        return status;
    }
    
    p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_NHID_VALID;  
    p_npm_cfg->nh_id = p_npm_attr->eloop_nexthop;   

    p_npm_cfg->pkt_format.ipg = 20;
    

    l2_header_len = 6 + 6 + vlan_num*4;
    
    sal_memcpy(tmp_pkt, npm_pkt_l2_header, sizeof(uint8)*l2_header_len);

    if (p_npm_attr->ip_addr_family == 4)
    {
    
        l3_header_len = 2 + 20 + 8 + 4 + 8;  // ether_type + ip_header_len + udp_header_len + seq_length + timestamp_length
        sal_memcpy(&tmp_pkt[l2_header_len], npm_pkt_ipv4_header, sizeof(uint8)*l3_header_len);

        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_TS_EN;
        if(p_npm_attr->ts_offset_set) 
        {
            p_npm_cfg->pkt_format.ts_offset = p_npm_attr->ts_offset;
        }
        else
        {
            p_npm_cfg->pkt_format.ts_offset = l2_header_len + 2 + 20 + 8 + 4;
            p_npm_attr->ts_offset = p_npm_cfg->pkt_format.ts_offset;
        }
        
        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_SEQ_EN;
        if(p_npm_attr->seq_offset_set) 
        {
            p_npm_cfg->pkt_format.seq_num_offset = p_npm_attr->seq_offset;
        }
        else
        {
            p_npm_cfg->pkt_format.seq_num_offset = l2_header_len + 2 + 20 + 8;
            p_npm_attr->seq_offset = p_npm_cfg->pkt_format.seq_num_offset;
        }

        if(  p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS)
        {
            // for modify the packet dst mac
            sal_memcpy(&mac_addr_tmp, &p_npm_attr->dst_mac, sizeof(sai_mac_t));
            *((uint8*)(&tmp_pkt[0])) = mac_addr_tmp[0];
            *((uint8*)(&tmp_pkt[1])) = mac_addr_tmp[1];
            *((uint8*)(&tmp_pkt[2])) = mac_addr_tmp[2];
            *((uint8*)(&tmp_pkt[3])) = mac_addr_tmp[3];
            *((uint8*)(&tmp_pkt[4])) = mac_addr_tmp[4];
            *((uint8*)(&tmp_pkt[5])) = mac_addr_tmp[5];

            // for modify the packet src mac
            sal_memcpy(&mac_addr_tmp, &p_npm_attr->src_mac, sizeof(sai_mac_t));
            *((uint8*)(&tmp_pkt[6])) = mac_addr_tmp[0];
            *((uint8*)(&tmp_pkt[7])) = mac_addr_tmp[1];
            *((uint8*)(&tmp_pkt[8])) = mac_addr_tmp[2];
            *((uint8*)(&tmp_pkt[9])) = mac_addr_tmp[3];
            *((uint8*)(&tmp_pkt[10])) = mac_addr_tmp[4];
            *((uint8*)(&tmp_pkt[11])) = mac_addr_tmp[5];


            if(p_npm_attr->outer_vlan)
            {
                *((uint8*)(&tmp_pkt[12])) = 0x81;
                *((uint8*)(&tmp_pkt[13])) = 0x00;
                *((uint8*)(&tmp_pkt[14])) = p_npm_attr->outer_vlan >> 8 ;
                *((uint8*)(&tmp_pkt[15])) = p_npm_attr->outer_vlan & 0xFF ;          
            }        
            
            if(p_npm_attr->inner_vlan)
            {
                *((uint8*)(&tmp_pkt[16])) = 0x81;
                *((uint8*)(&tmp_pkt[17])) = 0x00;
                *((uint8*)(&tmp_pkt[18])) = p_npm_attr->inner_vlan >> 8 ;
                *((uint8*)(&tmp_pkt[19])) = p_npm_attr->inner_vlan & 0xFF ;          
            } 

        }
        
        // for modify the packet src ip
        sal_memcpy(&ipv4_addr_tmp, &p_npm_attr->src_ip.addr.ip4, sizeof(sai_ip4_t));
         *((uint32*)(&tmp_pkt[26+vlan_num*4])) = ipv4_addr_tmp;

        // for modify the packet dst ip
        ipv4_addr_tmp = 0;
        sal_memcpy(&ipv4_addr_tmp, &p_npm_attr->dst_ip.addr.ip4, sizeof(sai_ip4_t));
         *((uint32*)(&tmp_pkt[30+vlan_num*4])) = ipv4_addr_tmp;

        // for modify ip header ttl
        tmp_pkt[22+vlan_num*4] = p_npm_attr->ttl;

        // for modify ip header tos    
        tmp_pkt[15+vlan_num*4] = p_npm_attr->priority << 2;

        // for modify ip header length       
        ip_header_lenth = p_npm_attr->packet_length - 14 - 4 - (vlan_num*4);
        *((uint16*)(&tmp_pkt[16+vlan_num*4])) = sal_htons(ip_header_lenth);
        
        udp_src_port = p_npm_attr->udp_src_port & 0xFFFF;
         *((uint16*)(&tmp_pkt[34+vlan_num*4])) = sal_htons(udp_src_port);

        udp_dst_port = p_npm_attr->udp_dst_port & 0xFFFF;
         *((uint16*)(&tmp_pkt[36+vlan_num*4])) = sal_htons(udp_dst_port);

        // for modify udp header length
        udp_header_lenth = p_npm_attr->packet_length - 34 - 4 - (vlan_num*4);
        *((uint16*)(&tmp_pkt[38+vlan_num*4])) = sal_htons(udp_header_lenth);
            
        // for modify ip header checksum  
        status = _ctc_sai_npm_calculate_ip_header_checsum(4, &checksum, tmp_pkt, vlan_num); 
        pkt_checksum = checksum & 0xFFFF;
        *((uint16*)(&tmp_pkt[24+vlan_num*4])) = sal_htons(pkt_checksum);        

        // for modify udp header checksum  
        status = _ctc_sai_npm_calculate_udp_header_checsum(4, &checksum, p_npm_attr->packet_length - 4, 26+vlan_num*4, 38+vlan_num*4, 34+vlan_num*4, 42+vlan_num*4, tmp_pkt); 
        pkt_checksum = checksum & 0xFFFF;
        *((uint16*)(&tmp_pkt[40+vlan_num*4])) = sal_htons(pkt_checksum); 

        status = _ctc_sai_npm_test_ipv4_packet(p_npm_attr, p_npm_cfg, tmp_pkt, vlan_num);

        p_npm_attr->packet_offset = 42+vlan_num*4;
       
    }
    
    else if (p_npm_attr->ip_addr_family == 6)
    {
        
        l3_header_len = 2 + 40 + 8 + 4 + 8;  // ether_type + ip_header_len + udp_header_len + seq_length + timestamp_length
        
        sal_memcpy(&tmp_pkt[l2_header_len], npm_pkt_ipv6_header, sizeof(uint8)*l3_header_len);

        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_TS_EN;
        if(p_npm_attr->ts_offset_set) 
        {
            p_npm_cfg->pkt_format.ts_offset = p_npm_attr->ts_offset;
        }
        else
        {
            p_npm_cfg->pkt_format.ts_offset = l2_header_len + 2 + 40 + 8 + 4;
            p_npm_attr->ts_offset = p_npm_cfg->pkt_format.ts_offset;
        }
        
        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_SEQ_EN;
        if(p_npm_attr->seq_offset_set) 
        {
            p_npm_cfg->pkt_format.seq_num_offset = p_npm_attr->seq_offset;
        }
        else
        {
            p_npm_cfg->pkt_format.seq_num_offset = l2_header_len + 2 + 40 + 8;
            p_npm_attr->seq_offset = p_npm_cfg->pkt_format.seq_num_offset;
        }


        if(  p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS)
        {

            // for modify the packet dst mac
            sal_memcpy(&mac_addr_tmp, &p_npm_attr->dst_mac, sizeof(sai_mac_t));
            *((uint8*)(&tmp_pkt[0])) = mac_addr_tmp[0];
            *((uint8*)(&tmp_pkt[1])) = mac_addr_tmp[1];
            *((uint8*)(&tmp_pkt[2])) = mac_addr_tmp[2];
            *((uint8*)(&tmp_pkt[3])) = mac_addr_tmp[3];
            *((uint8*)(&tmp_pkt[4])) = mac_addr_tmp[4];
            *((uint8*)(&tmp_pkt[5])) = mac_addr_tmp[5];

            // for modify the packet src mac
            sal_memcpy(&mac_addr_tmp, &p_npm_attr->src_mac, sizeof(sai_mac_t));
            *((uint8*)(&tmp_pkt[6])) = mac_addr_tmp[0];
            *((uint8*)(&tmp_pkt[7])) = mac_addr_tmp[1];
            *((uint8*)(&tmp_pkt[8])) = mac_addr_tmp[2];
            *((uint8*)(&tmp_pkt[9])) = mac_addr_tmp[3];
            *((uint8*)(&tmp_pkt[10])) = mac_addr_tmp[4];
            *((uint8*)(&tmp_pkt[11])) = mac_addr_tmp[5];



            if(p_npm_attr->outer_vlan)
            {
                *((uint8*)(&tmp_pkt[12])) = 0x81;
                *((uint8*)(&tmp_pkt[13])) = 0x00;
                *((uint8*)(&tmp_pkt[14])) = p_npm_attr->outer_vlan >> 8 ;
                *((uint8*)(&tmp_pkt[15])) = p_npm_attr->outer_vlan & 0xFF ;          
            }        
            
            if(p_npm_attr->inner_vlan)
            {
                *((uint8*)(&tmp_pkt[16])) = 0x81;
                *((uint8*)(&tmp_pkt[17])) = 0x00;
                *((uint8*)(&tmp_pkt[18])) = p_npm_attr->inner_vlan >> 8 ;
                *((uint8*)(&tmp_pkt[19])) = p_npm_attr->inner_vlan & 0xFF ;          
            }         
        }

        // for modify the packet src ip 
        sal_memcpy(ipv6_sa_addr, &p_npm_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
        *((uint32*)(&tmp_pkt[22+vlan_num*4])) = ipv6_sa_addr[0];
        *((uint32*)(&tmp_pkt[26+vlan_num*4])) = ipv6_sa_addr[1];
        *((uint32*)(&tmp_pkt[30+vlan_num*4])) = ipv6_sa_addr[2];
        *((uint32*)(&tmp_pkt[34+vlan_num*4])) = ipv6_sa_addr[3]; 
        
        // for modify the packet dst ip  
        sal_memcpy(ipv6_da_addr, &p_npm_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
        *((uint32*)(&tmp_pkt[38+vlan_num*4])) = ipv6_da_addr[0];
        *((uint32*)(&tmp_pkt[42+vlan_num*4])) = ipv6_da_addr[1];
        *((uint32*)(&tmp_pkt[46+vlan_num*4])) = ipv6_da_addr[2];
        *((uint32*)(&tmp_pkt[50+vlan_num*4])) = ipv6_da_addr[3]; 
        

        // for modify ipv6 header ttl
        tmp_pkt[21+vlan_num*4] = p_npm_attr->ttl;
        
        // for modify ipv6 header tos
        tos = p_npm_attr->priority << 2;
        tmp_pkt[14+vlan_num*4] = tmp_pkt[14+vlan_num*4] + (tos >> 4);        
        tmp_pkt[15+vlan_num*4] = tmp_pkt[15+vlan_num*4] + (tos << 4); 
        

        udp_src_port = p_npm_attr->udp_src_port & 0xFFFF;
         *((uint16*)(&tmp_pkt[54+vlan_num*4])) = sal_htons(udp_src_port);

        udp_dst_port = p_npm_attr->udp_dst_port & 0xFFFF;
         *((uint16*)(&tmp_pkt[56+vlan_num*4])) = sal_htons(udp_dst_port);

        // for modify ip header length       
        ip_header_lenth = p_npm_attr->packet_length - 54 - 4 - (vlan_num*4);
        *((uint16*)(&tmp_pkt[18+vlan_num*4])) = sal_htons(ip_header_lenth);
        
        // for modify udp header length
        udp_header_lenth = p_npm_attr->packet_length - 54 - 4 - (vlan_num*4);
        *((uint16*)(&tmp_pkt[58+vlan_num*4])) = sal_htons(udp_header_lenth);
        
        
        // for modify udp header checksum  
        status = _ctc_sai_npm_calculate_udp_header_checsum(6, &checksum, p_npm_attr->packet_length - 4, 22+vlan_num*4, 58+vlan_num*4, 54+vlan_num*4, 62+vlan_num*4, tmp_pkt); 
        pkt_checksum = checksum & 0xFFFF;
        *((uint16*)(&tmp_pkt[60+vlan_num*4])) = sal_htons(pkt_checksum); 

        status = _ctc_sai_npm_test_ipv6_packet(p_npm_attr, p_npm_cfg, tmp_pkt, vlan_num);        

        p_npm_attr->packet_offset = 62+vlan_num*4;        
    }

    p_npm_cfg->rate = p_npm_attr->tx_rate;

    if (SAI_NPM_TX_MODE_CONTINUOUS == p_npm_attr->pkt_tx_mode)
    {
        p_npm_cfg->tx_mode = CTC_NPM_TX_MODE_CONTINUOUS;
        if (p_npm_attr->pkt_duration)
        {
            p_npm_cfg->timeout = p_npm_attr->pkt_duration;
        }
        else
        {
            p_npm_cfg->timeout = 0;
        }
    }
    else if (SAI_NPM_TX_MODE_PACKET_NUM == p_npm_attr->pkt_tx_mode)
    {
        p_npm_cfg->tx_mode = CTC_NPM_TX_MODE_PACKET_NUM;
        p_npm_cfg->packet_num = p_npm_attr->pkt_cnt;
    }
    else if (SAI_NPM_TX_MODE_PERIOD == p_npm_attr->pkt_tx_mode)
    {
        p_npm_cfg->tx_mode = CTC_NPM_TX_MODE_PERIOD;
        p_npm_cfg->tx_period = p_npm_attr->period;
    }
    else
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        return status;           
    }

    if (p_npm_attr->packet_length)
    {
        p_npm_cfg->pkt_format.frame_size_mode = 0;  //fix frame size
        p_npm_cfg->pkt_format.frame_size = p_npm_attr->packet_length;

        // default to use the pattern 
        p_npm_cfg->pkt_format.pattern_type = CTC_NPM_PATTERN_TYPE_REPEAT;
        p_npm_cfg->pkt_format.repeat_pattern = 0x00;
    }

    return status;
}


#define ________SAI_NPM_DB_________


static sai_status_t
_ctc_sai_npm_build_db(uint8 lchip, sai_object_id_t session_id, ctc_sai_npm_t** npm_info)
{
    sai_status_t            status = SAI_STATUS_SUCCESS;
    ctc_sai_npm_t         *pst_npm = NULL;

    pst_npm = ctc_sai_db_get_object_property(lchip, session_id);
    if (NULL != pst_npm)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }

    pst_npm = mem_malloc(MEM_OAM_MODULE, sizeof(ctc_sai_npm_t));
    if (NULL == pst_npm)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(pst_npm, 0, sizeof(ctc_sai_npm_t));
    status = ctc_sai_db_add_object_property(lchip, session_id, pst_npm);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(pst_npm);
    }

    *npm_info = pst_npm;

    return status;
}


static sai_status_t
_ctc_sai_npm_remove_db(uint8 lchip, sai_object_id_t session_oid)
{
    sai_status_t            status = SAI_STATUS_SUCCESS;
    ctc_sai_npm_t         *pst_npm = NULL;

    pst_npm = ctc_sai_db_get_object_property(lchip, session_oid);
    if (NULL == pst_npm)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    status = ctc_sai_db_remove_object_property(lchip, session_oid);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "_ctc_sai_npm_remove_db error!\n");
        return status;
    }

    mem_free(pst_npm);
    return SAI_STATUS_SUCCESS;
}




#define ________SAI_NPM_NH________



static sai_status_t
_ctc_sai_npm_create_e2iloop_nexthop(ctc_sai_npm_t *p_npm_attr, uint8 lchip)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           ret = 0;
    uint32          nhid = 0;
    uint32          eloop_nhid = 0;    
    uint8           gchip = 0;
    uint32          l3if_id = 0;
    ctc_l3if_t      l3if;
    ctc_l3if_property_t l3if_prop;
    ctc_internal_port_assign_para_t port_assign;
    ctc_internal_port_assign_para_t port_assign_eloop;
    uint8  l3_encap = 0;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);    
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));

    ctc_loopback_nexthop_param_t iloop_nh;
    sal_memset(&iloop_nh, 0, sizeof(ctc_loopback_nexthop_param_t));
    

    // L3
    
    if ( p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_RAW_IP || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_MPLS_L3VPN )
    {

        l3_encap = 1;
        
        /*alloc iloop nexthop id */
        ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ret);
            status = ret;
            goto error0;
        }

        /*alloc global iloop port */
        sal_memset(&port_assign, 0, sizeof(port_assign));
        port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;   
        port_assign.gchip = gchip;
        ret = ctcs_alloc_internal_port(lchip, &port_assign);   
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error1;
        }
        
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate internal iloop port is %d\n", port_assign.inter_port);
        
        /*config inner l3if */
        sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
        ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ret);
            status = ret;
            goto error2;
        }
        
        l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
        l3if.gport = port_assign.inter_port;
        ret = ctcs_l3if_create(lchip, l3if_id, &l3if);   
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error3;
        }
        
        l3if_prop = CTC_L3IF_PROP_ROUTE_EN;
        ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error4;
        }
        l3if_prop = CTC_L3IF_PROP_IPV4_UCAST;
        ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error4;
        }
        l3if_prop = CTC_L3IF_PROP_IPV4_MCAST;
        ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error4;
        }
        l3if_prop = CTC_L3IF_PROP_IPV6_UCAST;
        ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret); 
            goto error4;
        }
        l3if_prop = CTC_L3IF_PROP_ROUTE_ALL_PKT;
        ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret); 
            goto error4;
        }
        l3if_prop = CTC_L3IF_PROP_VRF_EN;
        ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);  
            goto error4;
        }
        
        /* for vpn instance */
        if (p_npm_attr->vrf_oid)
        {
            uint32 vrf_id_tmp = 0;
            ctc_sai_oid_get_vrf_id_u32(p_npm_attr->vrf_oid, &vrf_id_tmp);
        
            l3if_prop = CTC_L3IF_PROP_VRF_ID;
            ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, vrf_id_tmp);
            if (ret)
            {
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
                status = ctc_sai_mapping_error_ctc(ret);
                goto error4;
            }
        }
        
        ret = ctcs_port_set_phy_if_en(lchip, port_assign.inter_port, 1);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error4;
        }
        
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate l3if_id  %d\n", l3if_id);


        /* add iloop nexthop */
        ctc_loopback_nexthop_param_t iloop_nh;
        sal_memset(&iloop_nh, 0, sizeof(ctc_loopback_nexthop_param_t));
                  
        iloop_nh.lpbk_lport = port_assign.inter_port;

        
        if ( p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_MPLS_L3VPN && p_npm_attr->role == SAI_NPM_SESSION_REFLECTOR )
        {
            iloop_nh.inner_packet_type_valid = 1;

            if (p_npm_attr->ip_addr_family == 4)
            {
                iloop_nh.inner_packet_type = CTC_PARSER_PKT_TYPE_IP_OR_IPV6;
            }
            else if (p_npm_attr->ip_addr_family == 6)
            {
                iloop_nh.inner_packet_type = CTC_PARSER_PKT_TYPE_IPV6;
            }

        }

        ret = ctcs_nh_add_iloop(lchip, nhid, &iloop_nh);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error5;
        }

        p_npm_attr->l3if_id = l3if_id;
        p_npm_attr->iloop_port = port_assign.inter_port;
        p_npm_attr->iloop_nexthop = nhid;

        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate iloop nexthop  %d\n", nhid);

    }

    // L2  
    
    else
    {
    
        /* add iloop nexthop */
    
        ctc_loopback_nexthop_param_t iloop_nh;
        sal_memset(&iloop_nh, 0, sizeof(ctc_loopback_nexthop_param_t));
       
        p_bridge_port = ctc_sai_db_get_object_property(lchip, p_npm_attr->test_port_oid);
        if (NULL == p_bridge_port)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }                   
        iloop_nh.lpbk_lport = p_bridge_port->gport;   
                    
        ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ret);
            status = ret;
            goto error0;
        }

        ret = ctcs_nh_add_iloop(lchip, nhid, &iloop_nh);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error1;

        }

        p_npm_attr->iloop_nexthop = nhid;

        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate iloop nexthop  %d\n", nhid);        

    }
    

    /*alloc global eloop port */
    sal_memset(&port_assign_eloop, 0, sizeof(port_assign_eloop));
    port_assign_eloop.type = CTC_INTERNAL_PORT_TYPE_ELOOP;
    port_assign_eloop.gchip = gchip;
    port_assign_eloop.nhid = p_npm_attr->iloop_nexthop; 
    
    ret = ctcs_alloc_internal_port(lchip, &port_assign_eloop);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
        goto error6;
    }

    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate internal eloop port is %d\n", port_assign_eloop.inter_port);

    /* add eloop nexthop */
    ctc_misc_nh_param_t nh_param;

    sal_memset(&nh_param, 0, sizeof(ctc_misc_nh_param_t));
    ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &eloop_nhid);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ret);
        status = ret;
        goto error7;
    }
    

    nh_param.type = CTC_MISC_NH_TYPE_FLEX_EDIT_HDR;
    nh_param.gport = port_assign_eloop.inter_port;
    nh_param.misc_param.flex_edit.dscp_select = CTC_NH_DSCP_SELECT_NONE;


    if (p_npm_attr->role == SAI_NPM_SESSION_SENDER)
    {        
        nh_param.misc_param.flex_edit.packet_type = CTC_MISC_NH_PACKET_TYPE_UDPORTCP;
        nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_UPDATE_UDP_CHKSUM;

        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family)
        {
            nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_IPV4;         // just for match sdk api (use 6w)
        }
           
        nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_IP_HDR;   // just for match sdk api
    }
    
    else if ( p_npm_attr->role == SAI_NPM_SESSION_REFLECTOR )
    {

        nh_param.misc_param.flex_edit.packet_type = CTC_MISC_NH_PACKET_TYPE_UDPORTCP;
        
        nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_IP_HDR;
        nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_SWAP_IP;

        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family)
        {
            nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_IPV4;
        }
        
        nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_L4_HDR;
        nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_SWAP_L4_PORT;        
        nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_UDP_PORT;

        if ( p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS )
        {
            nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_L2_HDR;
            nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_SWAP_MACDA; 
        }

    }
        
    ret = ctcs_nh_add_misc(lchip, eloop_nhid, &nh_param);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
        goto error8;
    }

    p_npm_attr->eloop_port = port_assign_eloop.inter_port;
    p_npm_attr->eloop_nexthop = eloop_nhid;

    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate eloop nexthop  %d\n", eloop_nhid);

    return SAI_STATUS_SUCCESS;


error8:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP,eloop_nhid);
error7:
    ctcs_free_internal_port(lchip, &port_assign_eloop);    
error6:
    ctcs_nh_remove_iloop(lchip, p_npm_attr->iloop_nexthop);
error5:
    if(l3_encap)
    {
        ctcs_port_set_phy_if_en(lchip, port_assign.inter_port, 0);
    }
error4:
    if(l3_encap)
    {
        ctcs_l3if_destory(lchip, l3if_id, &l3if);
    }
error3:
    if(l3_encap)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF,nhid);
    }
error2:
    if(l3_encap)
    {
        ctcs_free_internal_port(lchip, &port_assign);
    }    
error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP,nhid);
error0:
    return status;  
    
}


static sai_status_t
_ctc_sai_npm_remove_e2iloop_nexthop(ctc_sai_npm_t *p_npm_attr, uint8 lchip)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           ret = 0;
    uint8           gchip = 0;
    uint32          l3if_id = 0;
    ctc_l3if_t      l3if;
    ctc_internal_port_assign_para_t port_assign;

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    

    //L3     

    if ( p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_RAW_IP || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_MPLS_L3VPN )
    {


        /* delete l3if  */
        sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
        l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
        l3if.gport = p_npm_attr->iloop_port;
        l3if_id = p_npm_attr->l3if_id;

        ret = ctcs_l3if_destory(lchip, l3if_id, &l3if);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
        }

        ret = ctcs_port_set_phy_if_en(lchip, l3if.gport, 0);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
        }

        status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, l3if_id);


        /* delete internel port  */
        sal_memset(&port_assign, 0, sizeof(port_assign));
        port_assign.gchip = gchip;
        port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;
        port_assign.inter_port = p_npm_attr->iloop_port;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_free_internal_port(lchip, &port_assign));
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The dealloc internal port is %d\n", port_assign.inter_port);


    }

    /* delete loop nexthop  */
    if (p_npm_attr->iloop_nexthop)
    {
        ret = ctcs_nh_remove_iloop(lchip, p_npm_attr->iloop_nexthop);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
        }

        status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_npm_attr->iloop_nexthop);
    }

    if (p_npm_attr->eloop_nexthop)
    {
        ret = ctcs_nh_remove_misc(lchip, p_npm_attr->eloop_nexthop);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
        }

        status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_npm_attr->eloop_nexthop);
    }

    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.gchip = gchip;    
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ELOOP;
    port_assign.inter_port = p_npm_attr->eloop_port;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_free_internal_port(lchip, &port_assign));
    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The dealloc internal port is %d\n", port_assign.inter_port);

    return status;
}


#define ________SAI_NPM_ACL________


static sai_status_t
_ctc_sai_npm_acl_build_param(ctc_sai_npm_t *p_npm_attr, npm_acl_param_t *acl_entry)
{
    ipv6_addr_t     ipv6_sa_addr = {0};
    ipv6_addr_t     ipv6_da_addr = {0};

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);
    CTC_SAI_PTR_VALID_CHECK(acl_entry);



    if( p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS )
    {


        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)

        {
            //acl_entry->key.u.ipv4_key.l2_type = CTC_PARSER_L2_TYPE_ETH_V2;
            //acl_entry->key.u.ipv4_key.l2_type_mask = 0xf;


            if (p_npm_attr->is_swap_acl_key)
            {

                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_MAC_SA);
                sal_memcpy(&acl_entry->key.u.ipv4_key.mac_sa, &p_npm_attr->dst_mac, sizeof(sai_mac_t));        
                sal_memset(&acl_entry->key.u.ipv4_key.mac_sa_mask, 0xff, sizeof(sai_mac_t));

                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_MAC_DA);
                sal_memcpy(&acl_entry->key.u.ipv4_key.mac_da, &p_npm_attr->src_mac, sizeof(sai_mac_t));
                sal_memset(&acl_entry->key.u.ipv4_key.mac_da_mask, 0xff, sizeof(sai_mac_t)); 

            }
            
            else
            {

                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_MAC_SA);
                sal_memcpy(&acl_entry->key.u.ipv4_key.mac_sa, &p_npm_attr->src_mac, sizeof(sai_mac_t));
                sal_memset(&acl_entry->key.u.ipv4_key.mac_sa_mask, 0xff, sizeof(sai_mac_t));

                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_MAC_DA);
                sal_memcpy(&acl_entry->key.u.ipv4_key.mac_da, &p_npm_attr->dst_mac, sizeof(sai_mac_t));
                sal_memset(&acl_entry->key.u.ipv4_key.mac_da_mask, 0xff, sizeof(sai_mac_t)); 

            }
        }

        else
        {

            //acl_entry->key.u.ipv6_key.l2_type = CTC_PARSER_L2_TYPE_ETH_V2;
            //acl_entry->key.u.ipv6_key.l2_type_mask = 0xf;
            
            
            if (p_npm_attr->is_swap_acl_key)
            {
            
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_MAC_SA);
                sal_memcpy(&acl_entry->key.u.ipv6_key.mac_sa, &p_npm_attr->dst_mac, sizeof(sai_mac_t));        
                sal_memset(&acl_entry->key.u.ipv6_key.mac_sa_mask, 0xff, sizeof(sai_mac_t));
            
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_MAC_DA);
                sal_memcpy(&acl_entry->key.u.ipv6_key.mac_da, &p_npm_attr->src_mac, sizeof(sai_mac_t));
                sal_memset(&acl_entry->key.u.ipv6_key.mac_da_mask, 0xff, sizeof(sai_mac_t)); 
            
            }
            
            else
            {
            
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_MAC_SA);
                sal_memcpy(&acl_entry->key.u.ipv6_key.mac_sa, &p_npm_attr->src_mac, sizeof(sai_mac_t));
                sal_memset(&acl_entry->key.u.ipv6_key.mac_sa_mask, 0xff, sizeof(sai_mac_t));
            
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_MAC_DA);
                sal_memcpy(&acl_entry->key.u.ipv6_key.mac_da, &p_npm_attr->dst_mac, sizeof(sai_mac_t));
                sal_memset(&acl_entry->key.u.ipv6_key.mac_da_mask, 0xff, sizeof(sai_mac_t)); 
            
            }

        }

    }


    
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
    {
        acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV4;
        acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
        //acl_entry->key.u.ipv4_key.eth_type = 0x0800;
        //acl_entry->key.u.ipv4_key.eth_type_mask = 0xFFFF;
        CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L3_TYPE);
    }
    else
    {
        acl_entry->key.u.ipv6_key.l3_type = CTC_PARSER_L3_TYPE_IPV6;
        acl_entry->key.u.ipv6_key.l3_type_mask = 0xf;
        //acl_entry->key.u.ipv6_key.eth_type = 0x86DD;
        //acl_entry->key.u.ipv6_key.eth_type_mask = 0xFFFF;
        CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L3_TYPE);
    }

    

    if (p_npm_attr->is_swap_acl_key)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV4;
            acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_IP_SA);

            acl_entry->key.u.ipv4_key.ip_sa = sal_htonl(p_npm_attr->dst_ip.addr.ip4);
            acl_entry->key.u.ipv4_key.ip_sa_mask = 0xFFFFFFFF;

            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV4;
            acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_IP_DA);

            acl_entry->key.u.ipv4_key.ip_da = sal_htonl(p_npm_attr->src_ip.addr.ip4);
            acl_entry->key.u.ipv4_key.ip_da_mask = 0xFFFFFFFF;

            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV4;
            acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L4_PROTOCOL);
            acl_entry->key.u.ipv4_key.l4_protocol = 17;
            acl_entry->key.u.ipv4_key.l4_protocol_mask = 0xFF;
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv6_key.l3_type = CTC_PARSER_L3_TYPE_IPV6;
            acl_entry->key.u.ipv6_key.l3_type_mask = 0xf;

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_IP_SA);
            sal_memcpy(ipv6_sa_addr, &p_npm_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_sa_addr[0] = sal_htonl(ipv6_sa_addr[0]);
            ipv6_sa_addr[1] = sal_htonl(ipv6_sa_addr[1]);
            ipv6_sa_addr[2] = sal_htonl(ipv6_sa_addr[2]);
            ipv6_sa_addr[3] = sal_htonl(ipv6_sa_addr[3]);
            sal_memcpy(&acl_entry->key.u.ipv6_key.ip_sa, ipv6_sa_addr, sizeof(ipv6_addr_t));
            sal_memset(&acl_entry->key.u.ipv6_key.ip_sa_mask, 0xff, sizeof(ipv6_addr_t));

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv6_key.l3_type = CTC_PARSER_L3_TYPE_IPV6;
            acl_entry->key.u.ipv6_key.l3_type_mask = 0xf;

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_IP_DA);
            sal_memcpy(ipv6_da_addr, &p_npm_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_da_addr[0] = sal_htonl(ipv6_da_addr[0]);
            ipv6_da_addr[1] = sal_htonl(ipv6_da_addr[1]);
            ipv6_da_addr[2] = sal_htonl(ipv6_da_addr[2]);
            ipv6_da_addr[3] = sal_htonl(ipv6_da_addr[3]);
            sal_memcpy(&acl_entry->key.u.ipv6_key.ip_da, ipv6_da_addr, sizeof(ipv6_addr_t));
            sal_memset(&acl_entry->key.u.ipv6_key.ip_da_mask, 0xff, sizeof(ipv6_addr_t));

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv6_key.l3_type = CTC_PARSER_L3_TYPE_IPV6;
            acl_entry->key.u.ipv6_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L4_PROTOCOL);
            acl_entry->key.u.ipv6_key.l4_protocol = 17;
            acl_entry->key.u.ipv6_key.l4_protocol_mask = 0xFF;
        }
    }
    else
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV4;
            acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_IP_SA);

            acl_entry->key.u.ipv4_key.ip_sa = sal_htonl(p_npm_attr->src_ip.addr.ip4);
            acl_entry->key.u.ipv4_key.ip_sa_mask = 0xFFFFFFFF;

            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV4;
            acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_IP_DA);

            acl_entry->key.u.ipv4_key.ip_da = sal_htonl(p_npm_attr->dst_ip.addr.ip4);
            acl_entry->key.u.ipv4_key.ip_da_mask = 0xFFFFFFFF;

            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV4;
            acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L4_PROTOCOL);
            acl_entry->key.u.ipv4_key.l4_protocol = 17;
            acl_entry->key.u.ipv4_key.l4_protocol_mask = 0xFF;
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv6_key.l3_type = CTC_PARSER_L3_TYPE_IPV6;
            acl_entry->key.u.ipv6_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_IP_SA);

            sal_memcpy(ipv6_sa_addr, &p_npm_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_sa_addr[0] = sal_htonl(ipv6_sa_addr[0]);
            ipv6_sa_addr[1] = sal_htonl(ipv6_sa_addr[1]);
            ipv6_sa_addr[2] = sal_htonl(ipv6_sa_addr[2]);
            ipv6_sa_addr[3] = sal_htonl(ipv6_sa_addr[3]);
            sal_memcpy(&acl_entry->key.u.ipv6_key.ip_sa, ipv6_sa_addr, sizeof(ipv6_addr_t));
            sal_memset(&acl_entry->key.u.ipv6_key.ip_sa_mask, 0xff, sizeof(ipv6_addr_t));

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv6_key.l3_type = CTC_PARSER_L3_TYPE_IPV6;
            acl_entry->key.u.ipv6_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_IP_DA);

            sal_memcpy(ipv6_da_addr, &p_npm_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_da_addr[0] = sal_htonl(ipv6_da_addr[0]);
            ipv6_da_addr[1] = sal_htonl(ipv6_da_addr[1]);
            ipv6_da_addr[2] = sal_htonl(ipv6_da_addr[2]);
            ipv6_da_addr[3] = sal_htonl(ipv6_da_addr[3]);
            sal_memcpy(&acl_entry->key.u.ipv6_key.ip_da, ipv6_da_addr, sizeof(ipv6_addr_t));
            sal_memset(&acl_entry->key.u.ipv6_key.ip_da_mask, 0xff, sizeof(ipv6_addr_t));

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv6_key.l3_type = CTC_PARSER_L3_TYPE_IPV6;
            acl_entry->key.u.ipv6_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L4_PROTOCOL);
            acl_entry->key.u.ipv6_key.l4_protocol = 17;
            acl_entry->key.u.ipv6_key.l4_protocol_mask = 0xFF;
        }
    }

    if (p_npm_attr->priority)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_DSCP);
            acl_entry->key.u.ipv4_key.dscp = p_npm_attr->priority;
            acl_entry->key.u.ipv4_key.dscp_mask = 0xFF;
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_DSCP);
            acl_entry->key.u.ipv6_key.dscp = p_npm_attr->priority;
            acl_entry->key.u.ipv6_key.dscp_mask = 0xFF;
        }
    }

    if (p_npm_attr->is_swap_acl_key)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
        {
            if (p_npm_attr->udp_dst_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.sub_flag, CTC_ACL_IPV4_KEY_SUB_FLAG_L4_SRC_PORT);
                acl_entry->key.u.ipv4_key.l4_src_port_use_mask = 1;
                acl_entry->key.u.ipv4_key.l4_src_port_0 = p_npm_attr->udp_dst_port & 0xFFFF;
                acl_entry->key.u.ipv4_key.l4_src_port_1 = 0xFFFF;
            }

            if (p_npm_attr->udp_src_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.sub_flag, CTC_ACL_IPV4_KEY_SUB_FLAG_L4_DST_PORT);
                acl_entry->key.u.ipv4_key.l4_dst_port_use_mask = 1;
                acl_entry->key.u.ipv4_key.l4_dst_port_0 = p_npm_attr->udp_src_port & 0xFFFF;
                acl_entry->key.u.ipv4_key.l4_dst_port_1 = 0xFFFF;
            }
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
        {
            if (p_npm_attr->udp_dst_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.sub_flag, CTC_ACL_IPV6_KEY_SUB_FLAG_L4_SRC_PORT);
                acl_entry->key.u.ipv6_key.l4_src_port_use_mask = 1;
                acl_entry->key.u.ipv6_key.l4_src_port_0 = p_npm_attr->udp_dst_port & 0xFFFF;
                acl_entry->key.u.ipv6_key.l4_src_port_1 = 0xFFFF;
            }

            if (p_npm_attr->udp_src_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.sub_flag, CTC_ACL_IPV6_KEY_SUB_FLAG_L4_DST_PORT);
                acl_entry->key.u.ipv6_key.l4_dst_port_use_mask = 1;
                acl_entry->key.u.ipv6_key.l4_dst_port_0 = p_npm_attr->udp_src_port & 0xFFFF;
                acl_entry->key.u.ipv6_key.l4_dst_port_1 = 0xFFFF;
            }
        }
    }
    else
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
        {
            if (p_npm_attr->udp_dst_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.sub_flag, CTC_ACL_IPV4_KEY_SUB_FLAG_L4_DST_PORT);
                acl_entry->key.u.ipv4_key.l4_dst_port_use_mask = 1;
                acl_entry->key.u.ipv4_key.l4_dst_port_0 = p_npm_attr->udp_dst_port & 0xFFFF;
                acl_entry->key.u.ipv4_key.l4_dst_port_1 = 0xFFFF;
            }

            if (p_npm_attr->udp_src_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.sub_flag, CTC_ACL_IPV4_KEY_SUB_FLAG_L4_SRC_PORT);
                acl_entry->key.u.ipv4_key.l4_src_port_use_mask = 1;
                acl_entry->key.u.ipv4_key.l4_src_port_0 = p_npm_attr->udp_src_port & 0xFFFF;
                acl_entry->key.u.ipv4_key.l4_src_port_1 = 0xFFFF;
            }
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
        {
            if (p_npm_attr->udp_dst_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.sub_flag, CTC_ACL_IPV6_KEY_SUB_FLAG_L4_DST_PORT);
                acl_entry->key.u.ipv6_key.l4_dst_port_use_mask = 1;
                acl_entry->key.u.ipv6_key.l4_dst_port_0 = p_npm_attr->udp_dst_port & 0xFFFF;
                acl_entry->key.u.ipv6_key.l4_dst_port_1 = 0xFFFF;
            }

            if (p_npm_attr->udp_src_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.sub_flag, CTC_ACL_IPV6_KEY_SUB_FLAG_L4_SRC_PORT);
                acl_entry->key.u.ipv6_key.l4_src_port_use_mask = 1;
                acl_entry->key.u.ipv6_key.l4_src_port_0 = p_npm_attr->udp_src_port & 0xFFFF;
                acl_entry->key.u.ipv6_key.l4_src_port_1 = 0xFFFF;
            }
        }
    }

    if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
    {
        acl_entry->key.type = CTC_ACL_KEY_IPV4;
        acl_entry->key.u.ipv4_key.key_size = CTC_ACL_KEY_SIZE_DOUBLE;
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
    {
        acl_entry->key.type = CTC_ACL_KEY_IPV6;
    }

    return SAI_STATUS_SUCCESS;
}


sai_status_t
_ctc_sai_npm_acl_entry_id_alloc(uint8 lchip, uint32_t *acl_entry_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint32_t        entry_index = 0;

    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, &entry_index);
    *acl_entry_id = entry_index; 
    return status;
}


sai_status_t
_ctc_sai_npm_acl_entry_id_dealloc(uint8 lchip, uint32_t acl_entry_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;

    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, acl_entry_id);
    return status;
}


sai_status_t
_ctc_sai_npm_egress_acl_add(ctc_sai_npm_t *p_npm_attr, uint8  lchip)
{
        
    int32           ret = 0;
    uint32_t        entry_id = 0;
    ctc_acl_entry_t acl_entry;
    npm_acl_param_t param;
    uint32_t        group_index = 0;
    ctc_acl_field_action_t act_field;
    ctc_acl_vlan_edit_t   npm_acl_vlan_edit;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;


    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);

    sal_memset(&acl_entry, 0, sizeof(acl_entry));
    sal_memset(&param, 0, sizeof(param));

    status = _ctc_sai_npm_acl_build_param(p_npm_attr, &param);
    sal_memcpy(&acl_entry, &param, sizeof(npm_acl_param_t));

    status = _ctc_sai_npm_acl_entry_id_alloc(lchip, &entry_id);
    p_npm_attr->egress_acl_entry_id = entry_id;
    
    acl_entry.entry_id = p_npm_attr->egress_acl_entry_id; 
    group_index = p_ctc_sai_npm[lchip]->npm_reserved_egress_acl_group_id ; 

    ret = ctcs_acl_add_entry(lchip, group_index, &acl_entry);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl add entry failed: %d\n", ctc_get_error_desc(ret));
        return ret;
    }

    sal_memset(&act_field, 0, sizeof(ctc_acl_field_action_t));
    sal_memset(&npm_acl_vlan_edit, 0, sizeof(ctc_acl_vlan_edit_t));

    act_field.type = CTC_ACL_FIELD_ACTION_VLAN_EDIT;

    npm_acl_vlan_edit.stag_op = CTC_ACL_VLAN_TAG_OP_REP_OR_ADD;
    npm_acl_vlan_edit.svid_sl = CTC_ACL_VLAN_TAG_SL_NEW;


    p_bridge_port = ctc_sai_db_get_object_property(lchip, p_npm_attr->test_port_oid);
    if (NULL == p_bridge_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }    
        
    npm_acl_vlan_edit.svid_new = p_bridge_port->vlan_id;

    act_field.ext_data = &npm_acl_vlan_edit;

    ret = ctcs_acl_add_action_field(lchip, entry_id, &act_field);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl add entry action failed: %d\n", ctc_get_error_desc(ret));
        goto error1;
    }

    ret = ctcs_acl_install_entry(lchip, entry_id);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl install entry failed: %d\n", ctc_get_error_desc(ret));
        goto error1;
    }

    return ret;

error1:
    ctcs_acl_remove_entry(lchip, acl_entry.entry_id);
    return ret;    
}

sai_status_t
_ctc_sai_npm_ingress_acl_add(ctc_sai_npm_t *p_npm_attr, uint8  lchip)
{
    int32           ret = 0;
    uint32_t        entry_id = 0;
    ctc_acl_entry_t acl_entry;
    npm_acl_param_t param;
    uint32_t        group_index = 0;
    ctc_acl_field_action_t act_field;
    ctc_acl_oam_t   npm_acl_oam;
    sai_status_t    status = SAI_STATUS_SUCCESS;


    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);

    sal_memset(&acl_entry, 0, sizeof(acl_entry));
    sal_memset(&param, 0, sizeof(param));

    status = _ctc_sai_npm_acl_build_param(p_npm_attr, &param);
    sal_memcpy(&acl_entry, &param, sizeof(npm_acl_param_t));

    status = _ctc_sai_npm_acl_entry_id_alloc(lchip, &entry_id);
    p_npm_attr->ingress_acl_entry_id = entry_id;
    
    acl_entry.entry_id = p_npm_attr->ingress_acl_entry_id; 
    group_index = p_ctc_sai_npm[lchip]->npm_reserved_ingress_acl_group_id ; 

    ret = ctcs_acl_add_entry(lchip, group_index, &acl_entry);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl add entry failed: %d\n", ctc_get_error_desc(ret));
        return ret;
    }

    if (p_npm_attr->role == SAI_NPM_SESSION_SENDER )
    {
        sal_memset(&act_field, 0, sizeof(ctc_acl_field_action_t));
        sal_memset(&npm_acl_oam, 0, sizeof(ctc_acl_oam_t));

        act_field.type = CTC_ACL_FIELD_ACTION_OAM;
        npm_acl_oam.oam_type = CTC_ACL_OAM_TYPE_FLEX;
        npm_acl_oam.lmep_index = NPM_LMEP_INDEX + p_npm_attr->session_id;

        npm_acl_oam.packet_offset = p_npm_attr->packet_offset;

        act_field.ext_data = &npm_acl_oam;

        ret = ctcs_acl_add_action_field(lchip, entry_id, &act_field);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl add entry action failed: %d\n", ctc_get_error_desc(ret));
            goto error1;
        }
    }
    else if (p_npm_attr->role == SAI_NPM_SESSION_REFLECTOR )
    {

        sal_memset(&act_field, 0, sizeof(act_field));
        act_field.type = CTC_ACL_FIELD_ACTION_REDIRECT;
        act_field.data0 = p_npm_attr->eloop_nexthop;
        ret = ctcs_acl_add_action_field(lchip, entry_id, &act_field);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl add entry action failed: %d\n", ctc_get_error_desc(ret));
            goto error1;
        }

    }


    ret = ctcs_acl_install_entry(lchip, entry_id);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl install entry failed: %d\n", ctc_get_error_desc(ret));
        goto error1;
    }

    return ret;

error1:
    ctcs_acl_remove_entry(lchip, acl_entry.entry_id);
    return ret;
}

sai_status_t
_ctc_sai_npm_acl_del(uint32_t entry_id, uint8 lchip)
{
    int32       rc = 0;

    rc = ctcs_acl_uninstall_entry(lchip, entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        return rc;
    }

    rc = ctcs_acl_remove_entry(lchip, entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        return rc;
    }

    return rc;
}



#define ________SAI_NPM_CHECK________


sai_status_t
_ctc_sai_npm_parser_session_attr(uint32_t attr_count, const sai_attribute_t *attr_list, ctc_sai_npm_t *p_npm_attr)
{
    sai_status_t            status = SAI_STATUS_SUCCESS;
    uint32_t                index = 0;
    const sai_attribute_value_t     *attr_value = NULL;
    uint8  is_l2 = 0;    
    sai_object_type_t type = SAI_OBJECT_TYPE_NULL;
    sai_object_id_t   tmp_port_id = 0;
    ctc_object_id_t tmp_ctc_oid;
    uint32 i = 0;

    sal_memset(&tmp_port_id, 0, sizeof(sai_object_id_t));
    sal_memset(&tmp_ctc_oid, 0, sizeof(ctc_object_id_t));    

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_SESSION_ROLE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->role = attr_value->s32;
    }    
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    } 


    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->encap_type = attr_value->s32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }


    if(  p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS || p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS)
    {
        is_l2 = 1;    
    }
    else
    {
        is_l2 = 0;
    }    

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_NPM_TEST_PORT, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->test_port_oid = attr_value->oid;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }  



    status = ctc_sai_oid_get_type(p_npm_attr->test_port_oid, &type);

    if( is_l2 && type != SAI_OBJECT_TYPE_BRIDGE_PORT )
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "SAI_NPM_SESSION_ATTR_NPM_TEST_PORT type is wrong\n");
        return  SAI_STATUS_INVALID_PARAMETER;
    }
    else if ( !is_l2 && type != SAI_OBJECT_TYPE_PORT )
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "SAI_NPM_SESSION_ATTR_NPM_TEST_PORT type is wrong\n");
        return  SAI_STATUS_INVALID_PARAMETER;
    }

    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->receive_port_count = attr_value->objlist.count;

        if ( p_npm_attr->receive_port_count == 0 )
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "receive port list can not be empty");
            return  SAI_STATUS_INVALID_PARAMETER;
        }
        
        for (i = 0; i < p_npm_attr->receive_port_count; i++)
        {
            tmp_port_id = attr_value->objlist.list[i];
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, tmp_port_id, &tmp_ctc_oid);
            CTC_BMP_SET(p_npm_attr->receive_port_bits, CTC_MAP_GPORT_TO_LPORT(tmp_ctc_oid.value));   
        }        
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }  

    if (is_l2)

    {
    
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_SRC_MAC, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            sal_memcpy(&p_npm_attr->src_mac, &attr_value->mac, sizeof(sai_mac_t));
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
        

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_DST_MAC, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            sal_memcpy(&p_npm_attr->dst_mac, &attr_value->mac, sizeof(sai_mac_t));
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }


        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_OUTER_VLANID, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->outer_vlan = attr_value->u16;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_INNER_VLANID, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->inner_vlan = attr_value->u16;
        }

    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_SRC_IP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&p_npm_attr->src_ip, &attr_value->ipaddr, sizeof(p_npm_attr->src_ip));
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }  

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_DST_IP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&p_npm_attr->dst_ip, &attr_value->ipaddr, sizeof(p_npm_attr->dst_ip));
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_UDP_SRC_PORT, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->udp_src_port = attr_value->u32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }  

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_UDP_DST_PORT, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->udp_dst_port = attr_value->u32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }  


    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_TC, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->priority = attr_value->u8;
    }
    else
    {
        p_npm_attr->priority = 0;
    } 

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->vrf_oid = attr_value->oid;
    }
    else
    {
        p_npm_attr->vrf_oid = 0;
    }     

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->hw_lookup = attr_value->booldata;
    }    
    else
    {
        p_npm_attr->hw_lookup = true;
    }

    if (SAI_NPM_SESSION_SENDER == p_npm_attr->role)
    {
    
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_TTL, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->ttl = attr_value->u8;
        }    
        else
        {
            p_npm_attr->ttl = 255;
        } 

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->trans_enable = attr_value->booldata;
        }
        else
        {
            p_npm_attr->trans_enable = false;
        }


        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_PACKET_LENGTH, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->packet_length = attr_value->u32;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_TX_RATE, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->tx_rate = attr_value->u32;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }     
        
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_PKT_TX_MODE, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->pkt_tx_mode = attr_value->s32;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        } 

        if(p_npm_attr->pkt_tx_mode == SAI_NPM_TX_MODE_CONTINUOUS)
        {
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_TX_PKT_DURATION, &attr_value, &index);
            if(SAI_STATUS_SUCCESS == status)
            {
                p_npm_attr->pkt_duration = attr_value->u32;
            }
            else
            {
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
                return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }         
        }
        else if(p_npm_attr->pkt_tx_mode == SAI_NPM_TX_MODE_PACKET_NUM)
        {   
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_TX_PKT_CNT, &attr_value, &index);
            if(SAI_STATUS_SUCCESS == status)
            {
                p_npm_attr->pkt_cnt = attr_value->u32;
            }
            else
            {
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
                return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }                 
        }    
        else if(p_npm_attr->pkt_tx_mode == SAI_NPM_TX_MODE_PERIOD)
        {
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD, &attr_value, &index);
            if(SAI_STATUS_SUCCESS == status)
            {
                p_npm_attr->period = attr_value->u32;
            }
            else
            {
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
                return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }         
        }
        else 
        {
            return  SAI_STATUS_INVALID_PARAMETER;        
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_TIMESTAMP_OFFSET, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->ts_offset = attr_value->u32;
            p_npm_attr->ts_offset_set = 1;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_SEQUENCE_NUMBER_OFFSET, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->seq_offset = attr_value->u32;
            p_npm_attr->seq_offset_set = 1;
        }
        
    }

    return SAI_STATUS_SUCCESS;
}



static sai_status_t
_ctc_sai_npm_unsupport_attr_check(ctc_sai_npm_t *p_npm_attr, uint8 lchip)

{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 chip_type = CTC_CHIP_TSINGMA;

    chip_type = ctcs_get_chip_type(lchip);
    
    if(CTC_CHIP_TSINGMA == chip_type)
    {
        if (TRUE != p_npm_attr->hw_lookup)
        {
            status = SAI_STATUS_NOT_SUPPORTED;
            return status;
        }
    }
  
    return status;
}


#define ________SAI_NPM_ATTR________


sai_status_t
_ctc_sai_npm_get_npm_session_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t        status = SAI_STATUS_SUCCESS;
    uint8               lchip = 0;
    ctc_sai_npm_t     *p_npm_info = NULL;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;
    uint32 port_num = 0;
    sai_object_id_t* receive_ports;
    

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    ctcs_get_gchip_id(lchip, &gchip);
    
    p_npm_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_npm_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_NPM_SESSION_ATTR_SESSION_ROLE:
            attr->value.s32 = p_npm_info->role;
            break;
        case SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE:
            attr->value.s32 = p_npm_info->encap_type;
            break;  
        case SAI_NPM_SESSION_ATTR_NPM_TEST_PORT:
            attr->value.oid = p_npm_info->test_port_oid;
            break;
        case SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT:
            receive_ports =  mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*p_npm_info->receive_port_count);
            if (NULL == receive_ports)
            {
                return SAI_STATUS_NO_MEMORY;
            }
            sal_memset(receive_ports, 0, sizeof(sai_object_id_t)*p_npm_info->receive_port_count);

            
            for (bit_cnt = 0; bit_cnt < sizeof(p_npm_info->receive_port_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_npm_info->receive_port_bits, bit_cnt))
                {
                    receive_ports[port_num] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt));
                    port_num++;
                }
            }
            
            status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), receive_ports, port_num, &attr->value.objlist);
            mem_free(receive_ports);
            
            break;       
        case SAI_NPM_SESSION_ATTR_SRC_MAC:
            sal_memcpy(&attr->value.mac, &p_npm_info->src_mac, sizeof(sai_mac_t));
            break;
        case SAI_NPM_SESSION_ATTR_DST_MAC:
            sal_memcpy(&attr->value.mac, &p_npm_info->dst_mac, sizeof(sai_mac_t));
            break;
        case SAI_NPM_SESSION_ATTR_OUTER_VLANID:
            attr->value.u16= p_npm_info->outer_vlan;
            break;
        case SAI_NPM_SESSION_ATTR_INNER_VLANID:
            attr->value.u16 = p_npm_info->inner_vlan;
            break;
        case SAI_NPM_SESSION_ATTR_SRC_IP:
            sal_memcpy(&attr->value.ipaddr, &p_npm_info->src_ip, sizeof(sai_ip_address_t));
            break;
        case SAI_NPM_SESSION_ATTR_DST_IP:
            sal_memcpy(&attr->value.ipaddr, &p_npm_info->dst_ip, sizeof(sai_ip_address_t));
            break;
        case SAI_NPM_SESSION_ATTR_UDP_SRC_PORT:
            attr->value.u32 = p_npm_info->udp_src_port;
            break;
        case SAI_NPM_SESSION_ATTR_UDP_DST_PORT:
            attr->value.u32 = p_npm_info->udp_dst_port;
            break;
        case SAI_NPM_SESSION_ATTR_TTL:
            attr->value.u8 = p_npm_info->ttl;
            break;
        case SAI_NPM_SESSION_ATTR_TC:
            attr->value.u8 = p_npm_info->priority;
            break;
        case SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
            attr->value.booldata = p_npm_info->trans_enable;
            break;       
        case SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER:
            attr->value.oid = p_npm_info->vrf_oid;
            break;
        case SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID:
            attr->value.booldata = p_npm_info->hw_lookup;
            break;
        case SAI_NPM_SESSION_ATTR_PACKET_LENGTH:
            attr->value.u32 = p_npm_info->packet_length;
            break;
        case SAI_NPM_SESSION_ATTR_TX_RATE:
            attr->value.u32 = p_npm_info->tx_rate;
            break;       
        case SAI_NPM_SESSION_ATTR_PKT_TX_MODE:
            attr->value.s32 = p_npm_info->pkt_tx_mode;
            break;
        case SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD:
            attr->value.u32 = p_npm_info->period;
            break;
        case SAI_NPM_SESSION_ATTR_TX_PKT_CNT:
            attr->value.u32 = p_npm_info->pkt_cnt;
            break;
        case SAI_NPM_SESSION_ATTR_TX_PKT_DURATION:
            attr->value.u32 = p_npm_info->pkt_duration;
            break;
        case SAI_NPM_SESSION_ATTR_TIMESTAMP_OFFSET:
            attr->value.u32 = p_npm_info->ts_offset;
            break;
        case SAI_NPM_SESSION_ATTR_SEQUENCE_NUMBER_OFFSET:
            attr->value.u32 = p_npm_info->seq_offset;
            break;

        default:
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "Get npm attribute not implement\n");
            return  SAI_STATUS_NOT_IMPLEMENTED + attr_idx;
    }

    return status;
}

static sai_status_t 
_ctc_sai_npm_set_npm_session_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    sai_status_t        status = SAI_STATUS_SUCCESS;
    ctc_sai_npm_t       *p_npm_info = NULL;
    uint8               lchip = 0;
    uint8               session_id_tmp = 0;
    uint32              session_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_npm_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);

    if (NULL == p_npm_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (SAI_NPM_SESSION_SENDER != p_npm_info->role)
    {
        return  SAI_STATUS_INVALID_PARAMETER;
    }

    if (SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT != attr->id)
    {
        return  SAI_STATUS_INVALID_PARAMETER;
    }
    else
    {
        if (attr->value.booldata == p_npm_info->trans_enable)
        {
            return  SAI_STATUS_SUCCESS;
        }
    }

    status = ctc_sai_oid_get_npm_session_id(key->key.object_id, &session_id);
    session_id_tmp = session_id & 0xFF;

    CTC_SAI_CTC_ERROR_RETURN(ctcs_npm_set_transmit_en(lchip, session_id_tmp, attr->value.booldata));

    p_npm_info->trans_enable = attr->value.booldata;

    return SAI_STATUS_SUCCESS;
}

static ctc_sai_attr_fn_entry_t  npm_attr_fn_entries[] =
{
    { SAI_NPM_SESSION_ATTR_SESSION_ROLE,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr 
    },
    { SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },    
    { SAI_NPM_SESSION_ATTR_NPM_TEST_PORT,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    }, 
    { SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr 
    },    

    { SAI_NPM_SESSION_ATTR_SRC_MAC,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_DST_MAC,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_OUTER_VLANID,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_INNER_VLANID,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },

    { SAI_NPM_SESSION_ATTR_SRC_IP,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_DST_IP,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },


    { SAI_NPM_SESSION_ATTR_UDP_SRC_PORT,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_UDP_DST_PORT,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },

    { SAI_NPM_SESSION_ATTR_TTL,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },

    { SAI_NPM_SESSION_ATTR_TC,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },


    { SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },

    { SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    
    { SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_PACKET_LENGTH,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },

    { SAI_NPM_SESSION_ATTR_TX_RATE,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    
    { SAI_NPM_SESSION_ATTR_PKT_TX_MODE,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },

    { SAI_NPM_SESSION_ATTR_TX_PKT_CNT,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_TX_PKT_DURATION,
      _ctc_sai_npm_get_npm_session_attr,
      _ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_TIMESTAMP_OFFSET,
      _ctc_sai_npm_get_npm_session_attr,
      NULL
    },
    { SAI_NPM_SESSION_ATTR_SEQUENCE_NUMBER_OFFSET,
      _ctc_sai_npm_get_npm_session_attr,
      NULL
    },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};




#define ________SAI_NPM_WB________

static sai_status_t
_ctc_sai_npm_wb_sync_cb1(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_status_t ret = 0;
    ctc_wb_data_t wb_data;
    ctc_sai_npm_master_wb_t npm_master_wb;
    
    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    
    CTC_WB_INIT_DATA_T((&wb_data),ctc_sai_npm_master_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_NPM_GLOBAL);
    npm_master_wb.lchip = lchip;
    npm_master_wb.npm_reserved_ingress_acl_group_id = p_ctc_sai_npm[lchip]->npm_reserved_ingress_acl_group_id;
    npm_master_wb.npm_reserved_egress_acl_group_id = p_ctc_sai_npm[lchip]->npm_reserved_egress_acl_group_id;

    sal_memcpy((uint8*)wb_data.buffer, (uint8*)&npm_master_wb, sizeof(ctc_sai_npm_master_wb_t));

    wb_data.valid_cnt = 1;
    CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);

done:
out:
    CTC_WB_FREE_BUFFER(wb_data.buffer);
    return status;
}


static sai_status_t
_ctc_sai_npm_wb_reload_cb1(uint8 lchip)
{
    sai_status_t ret = 0;
    ctc_wb_query_t wb_query;
    ctc_sai_npm_master_wb_t npm_master_wb;
    uint32 entry_cnt = 0;

    sal_memset(&npm_master_wb, 0, sizeof(ctc_sai_npm_master_wb_t));

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    
    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_npm_master_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_NPM_GLOBAL);
    CTC_SAI_CTC_ERROR_GOTO(ctc_wb_query_entry(&wb_query), ret, out);

    if (wb_query.valid_cnt != 0)
    {
        sal_memcpy((uint8*)&npm_master_wb, (uint8*)(wb_query.buffer)+entry_cnt*(wb_query.key_len + wb_query.data_len),
            (wb_query.key_len+wb_query.data_len));

        p_ctc_sai_npm[lchip]->npm_reserved_ingress_acl_group_id = npm_master_wb.npm_reserved_ingress_acl_group_id;
        p_ctc_sai_npm[lchip]->npm_reserved_egress_acl_group_id = npm_master_wb.npm_reserved_egress_acl_group_id;      
    }


    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, p_ctc_sai_npm[lchip]->npm_reserved_ingress_acl_group_id));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, p_ctc_sai_npm[lchip]->npm_reserved_egress_acl_group_id));


out:    
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }
            
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_npm_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_sai_npm_t *p_db_npm = (ctc_sai_npm_t*)data;
    sai_object_id_t npm_sai_oid = *(sai_object_id_t*)key;
    ctc_object_id_t npm_ctc_oid;
    
    sal_memset(&npm_ctc_oid, 0, sizeof(ctc_object_id_t));
    
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NPM, npm_sai_oid, &npm_ctc_oid));

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NPM, npm_ctc_oid.value));

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, p_db_npm->ingress_acl_entry_id));
    
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_npm->eloop_nexthop)); 

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_npm->iloop_nexthop));
    

    if (p_db_npm->l3if_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_L3IF, p_db_npm->l3if_id));
    }

    if (p_db_npm->egress_acl_entry_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, p_db_npm->egress_acl_entry_id));
    }

    return SAI_STATUS_SUCCESS;
}




#define ________SAI_API________


sai_status_t
ctc_sai_npm_create_npm_session(sai_object_id_t *npm_session_id,  sai_object_id_t switch_id, 
                        uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t            status = SAI_STATUS_SUCCESS;
    int32                   ret = 0;
    uint8                   lchip = 0;
    uint32_t                npm_id = 0;
    sai_object_id_t         npm_tmp_oid = 0;
    ctc_npm_cfg_t           npm_cfg;
    ctc_sai_npm_t           npm_attr;
    ctc_sai_npm_t           *p_npm_info = NULL;
    uint8_t                 session_id = 0;
    ctc_acl_property_t      acl_prop;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;

    

    CTC_SAI_PTR_VALID_CHECK(npm_session_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    ctc_sai_oid_get_lchip(switch_id, &lchip);

    ctcs_get_gchip_id(lchip, &gchip);
    
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NPM, &npm_id),status, error0);
    
    npm_tmp_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_NPM, lchip, 0, 0, npm_id);

    sal_memset(&npm_attr, 0, sizeof(ctc_sai_npm_t));

    if (1 == SDK_WORK_PLATFORM)
    {
        status = ctc_sai_npm_write_hardware_table(lchip); 
    }
    
    status = _ctc_sai_npm_parser_session_attr(attr_count, attr_list, &npm_attr);
    if (CTC_SAI_ERROR(status))
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error1;
    }

    status = _ctc_sai_npm_unsupport_attr_check(&npm_attr, lchip);
    if (CTC_SAI_ERROR(status))
    {
        status = SAI_STATUS_NOT_SUPPORTED;
        goto error1;
    }

    npm_attr.session_id = npm_id;
   

    if (SAI_IP_ADDR_FAMILY_IPV4 == npm_attr.src_ip.addr_family) 
    {
        npm_attr.ip_addr_family = 4;
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == npm_attr.src_ip.addr_family) 
    {
        npm_attr.ip_addr_family = 6;    
    }


    sal_memset(&acl_prop, 0, sizeof(acl_prop));
    acl_prop.acl_en = 1;
    acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY;
    acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_L2_L3;


    if( npm_attr.receive_port_count )
    {

        for (bit_cnt = 0; bit_cnt < sizeof(npm_attr.receive_port_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(npm_attr.receive_port_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &acl_prop),status, error1);    
            }
        }
    }

    if (TRUE == npm_attr.hw_lookup)
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_npm_create_e2iloop_nexthop(&npm_attr, lchip),status, error2);
    }


    if (SAI_NPM_SESSION_SENDER == npm_attr.role)
    {

        npm_attr.is_swap_acl_key = 1;        
        ret = _ctc_sai_npm_ingress_acl_add(&npm_attr, lchip);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error3;
        }
        
        sal_memset(&npm_cfg, 0, sizeof(npm_cfg));

        CTC_SAI_ERROR_GOTO(_ctc_sai_npm_mapping_npm_session(&npm_attr, &npm_cfg),status, error4);
 
        npm_cfg.session_id = npm_id;
        
        ret = ctcs_npm_set_config(lchip, &npm_cfg);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error4;
        }

        if(npm_attr.trans_enable)
        {
            ret = ctcs_npm_set_transmit_en(lchip, session_id, npm_attr.trans_enable);
            if (ret)
            {
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
                status = ctc_sai_mapping_error_ctc(ret);
                goto error4;
            }
        }
     
    }
    
    else if (SAI_NPM_SESSION_REFLECTOR == npm_attr.role)
    {

        npm_attr.is_swap_acl_key = 0;
        ret = _ctc_sai_npm_ingress_acl_add(&npm_attr, lchip);        
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error3;
        }

        if ( npm_attr.encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS || npm_attr.encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS )
        {

            sal_memset(&acl_prop, 0, sizeof(acl_prop));
            acl_prop.acl_en = 1;
            acl_prop.direction = CTC_EGRESS;
            acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY;
            acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_L2_L3;

            CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, npm_attr.eloop_port, &acl_prop),status, error4);
            
            npm_attr.is_swap_acl_key = 1;
            ret = _ctc_sai_npm_egress_acl_add(&npm_attr, lchip);        
            if (ret)
            {
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
                status = ctc_sai_mapping_error_ctc(ret);
                goto error5;
            } 
        }        
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_npm_build_db(lchip, npm_tmp_oid, &p_npm_info), status, error6);

    sal_memcpy(p_npm_info, &npm_attr, sizeof(ctc_sai_npm_t));

    *npm_session_id = npm_tmp_oid;

    return status;

error6: 
    if(SAI_NPM_SESSION_REFLECTOR == npm_attr.role)
    {
        _ctc_sai_npm_acl_del(npm_attr.egress_acl_entry_id, lchip);
    }
error5:   
    if(SAI_NPM_SESSION_REFLECTOR == npm_attr.role)
    {
        acl_prop.acl_en = 0;
        acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY; 
        ctcs_port_set_acl_property(lchip, npm_attr.eloop_port, &acl_prop);
    }
error4:   
    _ctc_sai_npm_acl_del(npm_attr.ingress_acl_entry_id, lchip);
error3:
    _ctc_sai_npm_remove_e2iloop_nexthop(&npm_attr, lchip);   
error2:     
    acl_prop.acl_en = 0;
    acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY; 
    if( npm_attr.receive_port_count )
    {
        for (bit_cnt = 0; bit_cnt < sizeof(npm_attr.receive_port_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(npm_attr.receive_port_bits, bit_cnt))
            {
                ctcs_port_set_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &acl_prop);
            }
        }
    }    
error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NPM, npm_id);
error0:    
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "Failed to create npm session entry:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_npm_remove_npm_session(sai_object_id_t npm_session_oid)
{
    ctc_sai_npm_t     *p_npm_info = NULL;
    sai_status_t        status = SAI_STATUS_SUCCESS;
    uint8               lchip = 0;
    uint32              session_id = 0;
    uint8               session_id_tmp = 0;
    int32               ret = 0;
    ctc_acl_property_t acl_prop;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;
    

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_oid, &lchip));

    ctcs_get_gchip_id(lchip, &gchip);
    
    p_npm_info = ctc_sai_db_get_object_property(lchip, npm_session_oid);
    if (NULL == p_npm_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error1; 
    }

    sal_memset(&acl_prop, 0, sizeof(acl_prop));
    acl_prop.acl_en = 0;
    acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY;

    if( p_npm_info->receive_port_count )
    {

        for (bit_cnt = 0; bit_cnt < sizeof(p_npm_info->receive_port_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_npm_info->receive_port_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &acl_prop),status, error1);    
            }
        }
    }

    ret = _ctc_sai_npm_acl_del(p_npm_info->ingress_acl_entry_id, lchip);      
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
        goto error1;
    }    
    
    if (SAI_NPM_SESSION_SENDER == p_npm_info->role)
    {

        status = ctc_sai_oid_get_npm_session_id(npm_session_oid, &session_id);
        session_id_tmp = session_id & 0xFF;
    
        CTC_SAI_CTC_ERROR_GOTO(ctcs_npm_set_transmit_en(lchip, session_id_tmp, 0), status, error1);

        ret = ctcs_npm_clear_stats(lchip, session_id_tmp);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error1; 
        }
    
    }
    
    else if (SAI_NPM_SESSION_REFLECTOR == p_npm_info->role)
    {

        if( p_npm_info->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS || p_npm_info->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS)
        {
        
            sal_memset(&acl_prop, 0, sizeof(acl_prop));
            acl_prop.acl_en = 0;
            acl_prop.direction = CTC_EGRESS;
            acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY;
            
            CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, p_npm_info->eloop_port, &acl_prop),status, error1);
            
            ret = _ctc_sai_npm_acl_del(p_npm_info->egress_acl_entry_id, lchip);      
            if (ret)
            {
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
                status = ctc_sai_mapping_error_ctc(ret);
                goto error1;
            }  

        }
        
    }

    if (TRUE == p_npm_info->hw_lookup)
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_npm_remove_e2iloop_nexthop(p_npm_info, lchip), status, error1);
    }


    CTC_SAI_ERROR_GOTO(_ctc_sai_npm_remove_db(lchip, npm_session_oid),status, error1);
    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NPM, session_id);

    return status;

error1:    
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "Failed to remove npm session entry:%d\n", status);
    }
    return status;
}


sai_status_t
ctc_sai_npm_set_npm_attr(sai_object_id_t npm_session_id, const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = npm_session_id };
    uint8           lchip = 0;
    char            key_str[MAX_KEY_STR_LEN];
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_id, &lchip));
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_NPM, npm_attr_fn_entries, attr);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "Failed to set npm attr:%d, status:%d\n", attr->id,status);
    }

    return status;
}

sai_status_t
ctc_sai_npm_get_npm_attr(sai_object_id_t npm_session_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_object_key_t key = { .key.object_id = npm_session_id};
    sai_status_t    status = SAI_STATUS_SUCCESS;
    char            key_str[MAX_KEY_STR_LEN];
    uint32_t        loop_index = 0;
    uint8           lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_id, &lchip));

    while (loop_index < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str, SAI_OBJECT_TYPE_NPM,
                                    loop_index, npm_attr_fn_entries, &attr_list[loop_index]), status, out);
        loop_index ++;
    }

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "Failed to get npm attr. status:%d, attr_id:%d\n", status, attr_list[loop_index].id);
    }

    return status;
}

sai_status_t
ctc_sai_npm_get_npm_session_stats(sai_object_id_t npm_session_id, 
                                        uint32_t number_of_counters, 
                                        const sai_stat_id_t *counter_ids, 
                                        uint64_t *counters)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    int32   ret = 0;
    uint8   lchip = 0;
    uint8   session_id = 0;
    uint32  tmp_session_id = 0;
    uint64  fl = 0;
    uint8   stats_index = 0;
    ctc_npm_stats_t npm_stats;
    ctc_sai_npm_t     *p_npm_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);

    sal_memset(&npm_stats, 0, sizeof(ctc_npm_stats_t));
    
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_id, &lchip));
    p_npm_info = ctc_sai_db_get_object_property(lchip, npm_session_id);
    if (NULL == p_npm_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(p_npm_info->role != SAI_NPM_SESSION_SENDER)
    {
        return SAI_STATUS_INVALID_PARAMETER;        
    }

    status = ctc_sai_oid_get_npm_session_id(npm_session_id, &tmp_session_id);
    session_id = tmp_session_id & 0xFF;
    
    ret = ctcs_npm_get_stats(lchip, session_id, &npm_stats);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
        return status;
    }

    /*FL*/
    
    if (0 == npm_stats.tx_en)
    {
        if (npm_stats.tx_pkts >= npm_stats.rx_pkts)
        {
            fl = npm_stats.tx_pkts - npm_stats.rx_pkts;
        }
    }

    /*FD*/
    
    for (stats_index = 0; stats_index < number_of_counters; stats_index ++)
    {
        switch(counter_ids[stats_index])
        {
            case SAI_NPM_SESSION_STATS_RX_PACKETS:
                counters[stats_index] = npm_stats.rx_pkts;
                break;

            case SAI_NPM_SESSION_STATS_RX_BYTE:
                counters[stats_index] = npm_stats.rx_bytes;
                break;

            case SAI_NPM_SESSION_STATS_TX_PACKETS:
                counters[stats_index] = npm_stats.tx_pkts;
                break;

            case SAI_NPM_SESSION_STATS_TX_BYTE:
                counters[stats_index] = npm_stats.tx_bytes;
                break;

            case SAI_NPM_SESSION_STATS_DROP_PACKETS:
                counters[stats_index] = fl;
                break;
            
            case SAI_NPM_SESSION_STATS_MAX_LATENCY:
                counters[stats_index] = npm_stats.max_delay;
                break;

            case SAI_NPM_SESSION_STATS_MIN_LATENCY:
                counters[stats_index] = npm_stats.min_delay;
                break;

            case SAI_NPM_SESSION_STATS_AVG_LATENCY:
                counters[stats_index] = npm_stats.tx_pkts ? (npm_stats.total_delay / npm_stats.tx_pkts) : 0;
                break;

            default:
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "Get npm stats not implement\n");
                return  SAI_STATUS_NOT_IMPLEMENTED;
        }
    }    

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_npm_clear_npm_session_stats( sai_object_id_t npm_session_oid, uint32_t stats_count, const sai_stat_id_t *counter_ids)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32       ret = 0;
    uint8       lchip = 0;
    uint8       session_id = 0;
    uint32      session_id_tmp = 0;
    ctc_sai_npm_t     *p_npm_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_oid, &lchip));
    p_npm_info = ctc_sai_db_get_object_property(lchip, npm_session_oid);
    if (NULL == p_npm_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(p_npm_info->role != SAI_NPM_SESSION_SENDER)
    {
        return SAI_STATUS_INVALID_PARAMETER;        
    }

    status = ctc_sai_oid_get_npm_session_id(npm_session_oid, &session_id_tmp);
    session_id = session_id_tmp & 0xFF;
    
    ret = ctcs_npm_clear_stats(lchip, session_id);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
        return status;
    }

    return status;
}


#define ________SAI_INIT________


sai_status_t
ctc_sai_npm_write_hardware_table(uint8 lchip)
{
    sai_status_t  status = SAI_STATUS_SUCCESS;
    ctc_diag_tbl_t para;
    uint8   i = 0;

    for (i = 0; i < 8; i++ )
    {
        sal_memset(&para, 0, sizeof(ctc_diag_tbl_t));

        para.type = CTC_DIAG_TBL_OP_WRITE;

        sal_strncpy((char*)para.tbl_str, "AutoGenPktEn", CTC_DIAG_TBL_NAME_SIZE);

        para.index = i;
        para.entry_num = 1;

        para.info = mem_malloc(MEM_CLI_MODULE,sizeof(ctc_diag_entry_info_t));
        if (NULL == para.info)
        {
            status = SAI_STATUS_NO_MEMORY;
            return status;
        }

        sal_memset(para.info, 0, sizeof(ctc_diag_entry_info_t));

        sal_strncpy((char*)para.info[0].str,"tokenBytesCnt", CTC_DIAG_TBL_NAME_SIZE);

        para.info->value[0] = 0xffffffff;  // just for test
        para.info->mask[0] = 0xffffffff;

        status = ctcs_diag_tbl_control(lchip, &para);
        
        mem_free(para.info)

    }

    return status;
    
} 

sai_status_t
ctc_sai_npm_init_session_max(uint8 lchip)
{
    ctc_npm_global_cfg_t  npm_glb_config;
    sal_memset(&npm_glb_config, 0, sizeof(ctc_npm_global_cfg_t));

    if (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
    {
        npm_glb_config.session_mode = CTC_NPM_SESSION_MODE_4;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_npm_set_global_config(lchip, &npm_glb_config)); 
    }
    
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_npm_global_acl_init(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_acl_group_info_t    acl_group;
    uint32_t    group_id = 0;
    int32       rc = 0;
    uint32_t    group_index = 0;

    ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, &group_index);
    p_ctc_sai_npm[lchip]->npm_reserved_ingress_acl_group_id = group_index; 

    ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, &group_index);
    p_ctc_sai_npm[lchip]->npm_reserved_egress_acl_group_id = group_index;

        

    sal_memset(&acl_group, 0, sizeof(acl_group));
    acl_group.type     = CTC_ACL_GROUP_TYPE_NONE;
    acl_group.dir      = CTC_INGRESS;
    group_id           = p_ctc_sai_npm[lchip]->npm_reserved_ingress_acl_group_id;
    rc = ctcs_acl_create_group(lchip, group_id, &acl_group);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
        return status;
    }

    rc = ctcs_acl_install_group(lchip, group_id, &acl_group);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
        return status;
    }

    sal_memset(&acl_group, 0, sizeof(acl_group));
    acl_group.type     = CTC_ACL_GROUP_TYPE_NONE;
    acl_group.dir      = CTC_EGRESS;
    group_id           = p_ctc_sai_npm[lchip]->npm_reserved_egress_acl_group_id;
    rc = ctcs_acl_create_group(lchip, group_id, &acl_group);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
        return status;
    }

    rc = ctcs_acl_install_group(lchip, group_id, &acl_group);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
        return status;
    }

    return SAI_STATUS_SUCCESS;
}


const sai_npm_api_t ctc_sai_npm_api = {
    ctc_sai_npm_create_npm_session,
    ctc_sai_npm_remove_npm_session,
    ctc_sai_npm_set_npm_attr,
    ctc_sai_npm_get_npm_attr,
    ctc_sai_npm_get_npm_session_stats,
    ctc_sai_npm_clear_npm_session_stats,
};

sai_status_t
ctc_sai_npm_api_init()
{
    ctc_sai_register_module_api(SAI_API_NPM, (void*)&ctc_sai_npm_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_npm_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    uint8 value = 1;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_NPM;
    wb_info.data_len = sizeof(ctc_sai_npm_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_npm_wb_reload_cb;
    
    wb_info.wb_sync_cb1 = _ctc_sai_npm_wb_sync_cb1;
    wb_info.wb_reload_cb1 = _ctc_sai_npm_wb_reload_cb1;
    
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_NPM, (void*)(&wb_info));


    if(NULL != p_ctc_sai_npm[lchip])
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    p_ctc_sai_npm[lchip] = mem_malloc(MEM_OAM_MODULE, sizeof(ctc_sai_npm_master_t));
    if (NULL == p_ctc_sai_npm[lchip])
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_ctc_sai_npm[lchip], 0, sizeof(ctc_sai_npm_master_t));
    

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);



    ctc_sai_npm_global_acl_init(lchip);
    ctc_sai_npm_init_session_max(lchip);

    // for vpws second parser    
    ctcs_global_ctl_set(lchip, CTC_GLOBAL_VPWS_SNOOPING_PARSER, &value);
    
    if (1 == SDK_WORK_PLATFORM)
    {
        ctc_sai_npm_write_hardware_table(lchip); 
    } 
    
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_npm_db_deinit(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;


    if(NULL == p_ctc_sai_npm[lchip])
    {
        return status;
    }
    
    if(NULL != p_ctc_sai_npm[lchip])
    {
        mem_free(p_ctc_sai_npm[lchip]);
    }

    return status;
}

