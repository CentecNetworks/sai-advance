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
#include "ctcs_api.h"

static uint32_t npm_reserved_acl_group_id = 0;


uint8 npm_pkt_ipv4_header[9600] =
{
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x08, 0x00, 0x45, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00,
};

uint8 npm_pkt_ipv6_header[9600] =
{
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x86, 0xDD, 0x60, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x11, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00,
};

static sai_status_t
_ctc_sai_calculate_ip_header_checsum(uint8 addr_family, int32 *checksum_ptr, uint8 *pkt )
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
            j = i + 14;
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
_ctc_sai_calculate_udp_header_checsum(uint8 addr_family, int32 *checksum_ptr , uint32 pkt_len, uint32 ipaddr_offset, uint32 udplen_offset, uint32 udphead_offset, uint32 npm_data_offset, uint8 *pkt  )
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

        // data is inc byte mode 
        if(j>(npm_data_offset+41))
        {
            pkt[j] = pkt[j-1] + 1;
            pkt[j+1] = pkt[j] + 1;
        }
                    
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
_ctc_sai_npm_test_ipv4_packet(ctc_sai_npm_t *p_npm_attr, ctc_npm_cfg_t *p_npm, uint8 *pkt)
{
    p_npm->pkt_format.pkt_header = (void*)pkt;
    p_npm->pkt_format.header_len = 83;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_npm_test_ipv6_packet(ctc_sai_npm_t *p_npm_attr, ctc_npm_cfg_t *p_npm, uint8 *pkt)
{
    p_npm->pkt_format.pkt_header = (void*)pkt;
    p_npm->pkt_format.header_len = 103;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_twamp_acl_stats_create(uint32_t *stats_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           rc = 0;
    uint8           lchip = 0;
    ctc_stats_statsid_t     ctc_stats;

    CTC_SAI_PTR_VALID_CHECK(stats_id);

    sal_memset(&ctc_stats, 0, sizeof(ctc_stats));
    ctc_stats.dir = CTC_INGRESS;
    ctc_stats.type = CTC_STATS_STATSID_TYPE_ACL;

    rc = ctcs_stats_create_statsid(lchip, &ctc_stats);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    *stats_id = ctc_stats.stats_id;
    return status;
}

sai_status_t 
ctc_sai_twamp_acl_stats_remove(uint32_t stats_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           rc = 0;
    uint8           lchip = 0;

    rc = ctcs_stats_destroy_statsid(lchip, stats_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    return status;
}

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

    
    for (i = 0; i < 8; i++ )
    {
        sal_memset(&para, 0, sizeof(ctc_diag_tbl_t));

        para.type = CTC_DIAG_TBL_OP_WRITE;

        sal_strncpy((char*)para.tbl_str, "AutoGenPktPktCfg", CTC_DIAG_TBL_NAME_SIZE);

        para.index = i;
        para.entry_num = 1;

        para.info = mem_malloc(MEM_CLI_MODULE,sizeof(ctc_diag_entry_info_t));
        if (NULL == para.info)
        {
            status = SAI_STATUS_NO_MEMORY;
            return status;
        }

        sal_memset(para.info, 0, sizeof(ctc_diag_entry_info_t));

        sal_strncpy((char*)para.info[0].str,"isHaveEndTlv", CTC_DIAG_TBL_NAME_SIZE);

        para.info->value[0] = 0;  // just for test
        para.info->mask[0] = 0xffffffff;

        status = ctcs_diag_tbl_control(lchip, &para);
        
        mem_free(para.info)

    }


    return status;
    
} 

static sai_status_t
ctc_sai_npm_acl_build_param_field(ctc_sai_npm_t *p_npm_attr, npm_acl_param_t *acl_entry)
{
    ctc_field_key_t field_key;
    int32_t         rc = 0;
    uint32_t        entry_id = 0;
    uint8           lchip = 0;
    ipv6_addr_t     ipv6_sa_addr = {0};
    ipv6_addr_t     ipv6_sa_addr_mask = {0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF};
    ipv6_addr_t     ipv6_da_addr = {0};
    ipv6_addr_t     ipv6_da_addr_mask = {0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF};
    uint32_t        ipv4_da = 0;
    uint32_t        ipv4_sa = 0;
    uint32_t        global_port = 0;

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);
    CTC_SAI_PTR_VALID_CHECK(acl_entry);

    entry_id = p_npm_attr->loop_acl_entry_id;

    /* Mapping keys */
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
    {
        sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

        field_key.type = CTC_FIELD_KEY_L3_TYPE;
        field_key.data = CTC_PARSER_L3_TYPE_IPV4;
        field_key.mask = 0xFFFFFFFF;

        rc = ctcs_acl_add_key_field(lchip,entry_id, &field_key);
    }
    else
    {
        sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

        field_key.type = CTC_FIELD_KEY_L3_TYPE;
        field_key.data = CTC_PARSER_L3_TYPE_IPV6;
        field_key.mask = 0xFFFFFFFF;

        rc = ctcs_acl_add_key_field(lchip,entry_id, &field_key);
    }

    if (p_npm_attr->is_loop_swap_ip)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_SA;
            //field_key.data = p_npm_attr->dst_ip.addr.ip4;
            ipv4_sa = sal_htonl(p_npm_attr->dst_ip.addr.ip4);
            field_key.data = ipv4_sa;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_DA;
            ipv4_da = sal_htonl(p_npm_attr->src_ip.addr.ip4);
            field_key.data = ipv4_da;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_PROTOCOL;
            field_key.data = 17;   // UDP protocol
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IPV6_SA;
            sal_memcpy(ipv6_sa_addr, &p_npm_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_sa_addr[0] = sal_htonl(ipv6_sa_addr[0]);
            ipv6_sa_addr[1] = sal_htonl(ipv6_sa_addr[1]);
            ipv6_sa_addr[2] = sal_htonl(ipv6_sa_addr[2]);
            ipv6_sa_addr[3] = sal_htonl(ipv6_sa_addr[3]);
            field_key.ext_data = ipv6_sa_addr;

            ipv6_sa_addr_mask[0] = sal_htonl(ipv6_sa_addr_mask[0]);
            ipv6_sa_addr_mask[1] = sal_htonl(ipv6_sa_addr_mask[1]);
            ipv6_sa_addr_mask[2] = sal_htonl(ipv6_sa_addr_mask[2]);
            ipv6_sa_addr_mask[3] = sal_htonl(ipv6_sa_addr_mask[3]);
            field_key.ext_mask = ipv6_sa_addr_mask;
            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IPV6_DA;
            sal_memcpy(ipv6_da_addr, &p_npm_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_da_addr[0] = sal_htonl(ipv6_da_addr[0]);
            ipv6_da_addr[1] = sal_htonl(ipv6_da_addr[1]);
            ipv6_da_addr[2] = sal_htonl(ipv6_da_addr[2]);
            ipv6_da_addr[3] = sal_htonl(ipv6_da_addr[3]);
            field_key.ext_data = ipv6_da_addr;

            ipv6_da_addr_mask[0] = sal_htonl(ipv6_da_addr_mask[0]);
            ipv6_da_addr_mask[1] = sal_htonl(ipv6_da_addr_mask[1]);
            ipv6_da_addr_mask[2] = sal_htonl(ipv6_da_addr_mask[2]);
            ipv6_da_addr_mask[3] = sal_htonl(ipv6_da_addr_mask[3]);
            field_key.ext_mask = ipv6_da_addr_mask;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_PROTOCOL;
            field_key.data = 17;   // UDP protocol
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
    }
    else
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_SA;
            //field_key.data = p_npm_attr->src_ip.addr.ip4;
            ipv4_sa = sal_htonl(p_npm_attr->src_ip.addr.ip4);
            field_key.data = ipv4_sa;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_DA;
            //field_key.data = p_npm_attr->dst_ip.addr.ip4;
            ipv4_da = sal_htonl(p_npm_attr->dst_ip.addr.ip4);
            field_key.data = ipv4_da;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_PROTOCOL;
            field_key.data = 17;   // UDP protocol
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IPV6_SA;
            sal_memcpy(ipv6_sa_addr, &p_npm_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_sa_addr[0] = sal_htonl(ipv6_sa_addr[0]);
            ipv6_sa_addr[1] = sal_htonl(ipv6_sa_addr[1]);
            ipv6_sa_addr[2] = sal_htonl(ipv6_sa_addr[2]);
            ipv6_sa_addr[3] = sal_htonl(ipv6_sa_addr[3]);
            field_key.ext_data = ipv6_sa_addr;

            ipv6_sa_addr_mask[0] = sal_htonl(ipv6_sa_addr_mask[0]);
            ipv6_sa_addr_mask[1] = sal_htonl(ipv6_sa_addr_mask[1]);
            ipv6_sa_addr_mask[2] = sal_htonl(ipv6_sa_addr_mask[2]);
            ipv6_sa_addr_mask[3] = sal_htonl(ipv6_sa_addr_mask[3]);
            field_key.ext_mask = ipv6_sa_addr_mask;
            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IPV6_DA;
            sal_memcpy(ipv6_da_addr, &p_npm_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_da_addr[0] = sal_htonl(ipv6_da_addr[0]);
            ipv6_da_addr[1] = sal_htonl(ipv6_da_addr[1]);
            ipv6_da_addr[2] = sal_htonl(ipv6_da_addr[2]);
            ipv6_da_addr[3] = sal_htonl(ipv6_da_addr[3]);
            field_key.ext_data = ipv6_da_addr;

            ipv6_da_addr_mask[0] = sal_htonl(ipv6_da_addr_mask[0]);
            ipv6_da_addr_mask[1] = sal_htonl(ipv6_da_addr_mask[1]);
            ipv6_da_addr_mask[2] = sal_htonl(ipv6_da_addr_mask[2]);
            ipv6_da_addr_mask[3] = sal_htonl(ipv6_da_addr_mask[3]);
            field_key.ext_mask = ipv6_da_addr_mask;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_PROTOCOL;
            field_key.data = 17;   // UDP protocol
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
    }

    if (p_npm_attr->priority)
    {
        sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

        field_key.type = CTC_FIELD_KEY_IP_DSCP;
        field_key.data = p_npm_attr->priority;
        field_key.mask = 0xFFFFFFFF;

        rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
    }

    if (p_npm_attr->is_loop_swap_ip)
    {
        if (p_npm_attr->udp_dst_port)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_L4_SRC_PORT;
            field_key.data = p_npm_attr->udp_dst_port;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }

        if (p_npm_attr->udp_src_port)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_L4_DST_PORT;
            field_key.data = p_npm_attr->udp_src_port;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
    }
    else
    {
        if (p_npm_attr->udp_dst_port)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_L4_DST_PORT;
            field_key.data = p_npm_attr->udp_dst_port;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }

        if (p_npm_attr->udp_src_port)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_L4_SRC_PORT;
            field_key.data = p_npm_attr->udp_src_port;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
    }

    if ( SAI_NPM_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI == p_npm_attr->encap_type)
    {
        sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_npm_attr->port_id, &global_port));
        field_key.type = CTC_FIELD_KEY_DST_GPORT;
        field_key.data = global_port;
        field_key.mask = 0xFFFFFFFF;

        rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
    }

    return SAI_STATUS_SUCCESS;
}
    
static sai_status_t
ctc_sai_npm_acl_build_param(ctc_sai_npm_t *p_npm_attr, npm_acl_param_t *acl_entry)
{
    ipv6_addr_t     ipv6_sa_addr = {0};
    ipv6_addr_t     ipv6_da_addr = {0};

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);
    CTC_SAI_PTR_VALID_CHECK(acl_entry);
    
    /* Mapping keys */
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
    {
        acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV4;
        acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
        acl_entry->key.u.ipv4_key.eth_type = 0x0800;
        acl_entry->key.u.ipv4_key.eth_type_mask = 0xFFFF;
    }
    else
    {
        acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV6;
        acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
        acl_entry->key.u.ipv4_key.eth_type = 0x86DD;
        acl_entry->key.u.ipv4_key.eth_type_mask = 0xFFFF;
    }

    CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L3_TYPE);

    if (p_npm_attr->is_loop_swap_ip)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L3_TYPE);
            acl_entry->key.u.ipv4_key.l3_type = CTC_PARSER_L3_TYPE_IPV4;
            acl_entry->key.u.ipv4_key.l3_type_mask = 0xf;
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_IP_SA);

            // loop for match swap ip and udp port 
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

            // loop for match swap ip and udp port 
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

            // loop for match swap ip and udp port 
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
            acl_entry->key.u.ipv4_key.dscp = p_npm_attr->priority;
            acl_entry->key.u.ipv4_key.dscp_mask = 0xFF;
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
        {
            acl_entry->key.u.ipv6_key.dscp = p_npm_attr->priority;
            acl_entry->key.u.ipv6_key.dscp_mask = 0xFF;
        }
    }

    if (p_npm_attr->is_loop_swap_ip)
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

#if 0
    uint32_t        acl_stats_id = 0;

    ctc_sai_twamp_acl_stats_create(&acl_stats_id);

    CTC_SET_FLAG(acl_entry->action.flag, CTC_ACL_ACTION_FLAG_STATS);
    acl_entry->action.stats_id = acl_stats_id;
#endif

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_npm_create_e2iloop_nexthop_for_hw_lookup(ctc_sai_npm_t *p_npm_attr, sai_object_id_t switch_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           ret = 0;
    uint32          nhid = 0;
    uint8           lchip = 0;
    uint8           gchip = 0;
    uint32          l3if_id = 0;
    ctc_l3if_t      l3if;
    ctc_l3if_property_t l3if_prop;
    ctc_internal_port_assign_para_t port_assign;

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));

    /*alloc global iloop port */
    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;   
    port_assign.gchip = gchip;
    ret = ctcs_alloc_internal_port(lchip, &port_assign);   
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate internal iloop port is %d\n", port_assign.inter_port);

    /*config inner l3if */
    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id);
    l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
    l3if.gport = port_assign.inter_port;
    ret = ctcs_l3if_create(lchip, l3if_id, &l3if);   
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    l3if_prop = CTC_L3IF_PROP_ROUTE_EN;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_IPV4_UCAST;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_IPV4_MCAST;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_IPV6_UCAST;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_ROUTE_ALL_PKT;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_VRF_EN;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
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
        }
    }

    ret = ctcs_port_set_phy_if_en(lchip, port_assign.inter_port, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate l3if_id  %d\n", l3if_id);

    /* add iloop nexthop */
    ctc_loopback_nexthop_param_t iloop_nh;
    sal_memset(&iloop_nh, 0, sizeof(ctc_loopback_nexthop_param_t));
    ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid);    
    iloop_nh.lpbk_lport = port_assign.inter_port;

    ret = ctcs_nh_add_iloop(lchip, nhid, &iloop_nh);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    p_npm_attr->l3if_id = l3if_id;
    p_npm_attr->iloop_port = port_assign.inter_port;
    p_npm_attr->iloop_nexthop = nhid;

    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate iloop nexthop  %d\n", nhid);

    /*alloc global eloop port */
    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ELOOP;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    port_assign.gchip = gchip;
    port_assign.nhid = p_npm_attr->iloop_nexthop;   
    ret = ctcs_alloc_internal_port(lchip, &port_assign);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate internal eloop port is %d\n", port_assign.inter_port);

    /* add eloop nexthop */
    ctc_misc_nh_param_t nh_param;

    sal_memset(&nh_param, 0, sizeof(ctc_misc_nh_param_t));
    ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid);
    if (p_npm_attr->role == SAI_NPM_SESSION_REFLECTOR)
    {
         nh_param.type = CTC_MISC_NH_TYPE_FLEX_EDIT_HDR;
         nh_param.gport = port_assign.inter_port;

         nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_IP_HDR;
         nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_SWAP_IP;
         if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family)
         {
             nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_IPV4;
         }

         nh_param.misc_param.flex_edit.packet_type = CTC_MISC_NH_PACKET_TYPE_UDPORTCP;
         nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_L4_HDR;
         nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_SWAP_L4_PORT;
         nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_UDP_PORT;
         nh_param.misc_param.flex_edit.dscp_select = CTC_NH_DSCP_SELECT_NONE;
    }
    else if (p_npm_attr->role == SAI_NPM_SESSION_SENDER)
    {
        nh_param.type = CTC_MISC_NH_TYPE_FLEX_EDIT_HDR;
        nh_param.gport = port_assign.inter_port;
    }

    ret = ctcs_nh_add_misc(lchip, nhid, &nh_param);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    p_npm_attr->eloop_port = port_assign.inter_port;
    p_npm_attr->eloop_nexthop = nhid;

    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The allocate eloop nexthop  %d\n", nhid);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_npm_remove_e2iloop_nexthop_for_hw_lookup(ctc_sai_npm_t *p_npm_attr, uint8 lchip)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           ret = 0;
    uint8           gchip = 0;
    uint32          l3if_id = 0;
    ctc_l3if_t      l3if;
    ctc_internal_port_assign_para_t port_assign;

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    
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

    /* delete internel port  */
    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.gchip = gchip;
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;
    port_assign.inter_port = p_npm_attr->iloop_port;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_free_internal_port(lchip, &port_assign));
    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The dealloc internal port is %d\n", port_assign.inter_port);

    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ELOOP;
    port_assign.gchip = gchip;
    port_assign.inter_port = p_npm_attr->eloop_port;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_free_internal_port(lchip, &port_assign));
    CTC_SAI_LOG_ERROR(SAI_API_NPM, "%%The dealloc internal port is %d\n", port_assign.inter_port);

    return status;
}

sai_status_t
ctc_sai_npm_acl_add(sai_object_id_t npm_session_id, ctc_sai_npm_t *p_npm_attr)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           rc = 0;
    uint32_t        entry_id = 0;
    uint8           lchip = 0;
    ctc_acl_entry_t acl_entry;
    npm_acl_param_t param;
    uint32_t        group_index = 0;
    ctc_acl_field_action_t field_action;

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);

    sal_memset(&field_action, 0, sizeof(field_action));
    sal_memset(&acl_entry, 0, sizeof(acl_entry));
    sal_memset(&param, 0, sizeof(param));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_id, &lchip));

    ctc_sai_npm_acl_entry_id_alloc(&entry_id);

    p_npm_attr->loop_acl_entry_id = entry_id;
  
    acl_entry.entry_id = p_npm_attr->loop_acl_entry_id;
    group_index = npm_reserved_acl_group_id; 

    acl_entry.mode = 1;
    acl_entry.key_type = CTC_ACL_KEY_FWD;
    if ((rc = ctcs_acl_add_entry(lchip, group_index, &acl_entry)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl add entry failed: %d\n", ctc_get_error_desc(rc));
        return rc;
    }

    status = ctc_sai_npm_acl_build_param_field(p_npm_attr, &param);
    sal_memcpy(&acl_entry, &param, sizeof(npm_acl_param_t));

    if (p_npm_attr->eloop_nexthop)
    {
        sal_memset(&field_action, 0, sizeof(field_action));

        field_action.type = CTC_ACL_FIELD_ACTION_REDIRECT;
        field_action.data0 = p_npm_attr->eloop_nexthop;
        rc = ctcs_acl_add_action_field(lchip, entry_id, &field_action);
    }

    if ((rc = ctcs_acl_install_entry(lchip, entry_id)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl install entry failed: %d\n", ctc_get_error_desc(rc));
        goto error1;
    }

    return status;

error1:
    rc = ctcs_acl_remove_entry(lchip, entry_id);
    return rc;
}

sai_status_t
ctc_sai_npm_acl_del(uint32_t entry_id, uint8 lchip)
{
    int32       rc = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;

    // refer to session id, do not alloc
    rc = ctcs_acl_uninstall_entry(lchip, entry_id);
    if (rc)
    {
        return SAI_STATUS_FAILURE;
    }

    // uninstall the entry, when disable the npm session
    rc = ctcs_acl_remove_entry(lchip, entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    status = ctc_sai_npm_acl_entry_id_dealloc(entry_id);

    return status;
}

sai_status_t
ctc_sai_npm_global_acl_add(sai_object_id_t npm_session_id, ctc_sai_npm_t *p_npm_attr)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           rc = 0;
    uint32_t        entry_id = 0;
    uint32_t        session_id = 0;
    uint8           lchip = 0;
    ctc_acl_entry_t acl_entry;
    npm_acl_param_t param;
    uint32_t        group_index = 0;

    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);

    sal_memset(&acl_entry, 0, sizeof(acl_entry));
    sal_memset(&param, 0, sizeof(param));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_id, &lchip));
    status = ctc_sai_npm_acl_build_param(p_npm_attr, &param);
    sal_memcpy(&acl_entry, &param, sizeof(npm_acl_param_t));

     // refer to session id, do not alloc
    ctc_sai_oid_get_npm_session_id(npm_session_id, &session_id);

    ctc_sai_npm_acl_entry_id_alloc(&entry_id);

    // save the entry id
    p_npm_attr->oam_acl_entry_id = entry_id;
    
    acl_entry.entry_id = p_npm_attr->oam_acl_entry_id; 
    group_index = npm_reserved_acl_group_id; 

    if ((rc = ctcs_acl_add_entry(lchip, group_index, &acl_entry)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl add entry failed: %d\n", ctc_get_error_desc(rc));
        return rc;
    }

    ctc_acl_oam_t   npm_acl_oam;
    ctc_acl_field_action_t act_field;

    sal_memset(&act_field, 0, sizeof(ctc_acl_field_action_t));
    sal_memset(&npm_acl_oam, 0, sizeof(ctc_acl_oam_t));

    act_field.type = CTC_ACL_FIELD_ACTION_OAM;
    npm_acl_oam.oam_type = CTC_ACL_OAM_TYPE_FLEX;
    npm_acl_oam.lmep_index = p_npm_attr->lmep_index;

    if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
    {
        npm_acl_oam.packet_offset = 42;
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
    {
        npm_acl_oam.packet_offset = 42 + 20; 
    }

    act_field.ext_data = &npm_acl_oam;
    rc = ctcs_acl_add_action_field(lchip, entry_id, &act_field);

    if ((rc = ctcs_acl_install_entry(lchip, entry_id)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "acl install entry failed: %d\n", ctc_get_error_desc(rc));
        goto error1;
    }

    return status;

error1:
    rc = ctcs_acl_remove_entry(lchip, acl_entry.entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    return status;
}

sai_status_t
ctc_sai_npm_global_acl_del(uint32_t entry_id, uint8 lchip)
{
    int32       rc = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;

    rc = ctcs_acl_uninstall_entry(lchip, entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    // uninstall the entry, when disable the npm session
    rc = ctcs_acl_remove_entry(lchip, entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    status = ctc_sai_npm_acl_entry_id_dealloc(entry_id);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_npm_global_acl_init(void)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_acl_group_info_t    acl_group;
    uint32_t    group_id = 0;
    int32       rc = 0;
    uint8       lchip = 0;
    uint32_t    group_index = 0;

    ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, &group_index);
    npm_reserved_acl_group_id = group_index; 

    sal_memset(&acl_group, 0, sizeof(acl_group));
    acl_group.type     = CTC_ACL_GROUP_TYPE_NONE;
    acl_group.dir      = CTC_INGRESS;
    group_id           = npm_reserved_acl_group_id;
    rc = ctcs_acl_create_group(lchip, group_id, &acl_group);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    rc = ctcs_acl_install_group(lchip, group_id, &acl_group);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    return status;
}

sai_status_t
ctc_sai_npm_acl_entry_id_alloc(uint32_t *acl_entry_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8           lchip = 0;
    uint32_t        entry_index = 0;

    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, &entry_index);
    *acl_entry_id = entry_index; 
    return status;
}

sai_status_t
ctc_sai_npm_acl_entry_id_dealloc(uint32_t acl_entry_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8           lchip = 0;

    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, acl_entry_id);
    return status;
}

sai_status_t
ctc_sai_npm_mep_index_get_by_session_id(uint8 lchip, uint32_t session_id, uint32_t *p_mep_index)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint32_t        lmep_index = 0;

    if (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
    {
        lmep_index = session_id + 0x1FF7;
    }
    else 
    {
        // tmp for tm, need to be added in tm2    
        status = SAI_STATUS_NOT_SUPPORTED;
        //lmep_index = session_id + 0x3FF7;
    }

    *p_mep_index = lmep_index;

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

sai_status_t
_ctc_sai_npm_mapping_npm_session(ctc_sai_npm_t *p_npm_attr, ctc_npm_cfg_t *p_npm_cfg, sai_object_id_t switch_id, uint8 *pkt)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint16          udp_src_port = 0;
    uint16          udp_dst_port = 0;
    uint16          ip_header_lenth = 0;
    uint16          udp_header_lenth = 0;    
    uint32_t        ipv4_addr_tmp = 0;
    ipv6_addr_t     ipv6_sa_addr = {0};
    ipv6_addr_t     ipv6_da_addr = {0};
    int32 checksum = 0;
    uint16 pkt_checksum =0;
    uint8 tos = 0;
    uint8 tmp_pkt[9600] = {0};
 
    CTC_SAI_PTR_VALID_CHECK(p_npm_attr);
    CTC_SAI_PTR_VALID_CHECK(p_npm_cfg);
    CTC_SAI_PTR_VALID_CHECK(pkt);

    sal_memcpy(tmp_pkt, pkt, sizeof(uint8)*103);

    if ((p_npm_attr->packet_length < NPM_PACKET_BASE_LENGTH_IPV4) && SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family )
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        return status;
    }

    if ((p_npm_attr->packet_length < NPM_PACKET_BASE_LENGTH_IPV6) && SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family )
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        return status;
    }
    
    // sdk only support assign dest_gport
    p_npm_cfg->dest_gport = p_npm_attr->eloop_port;

    if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
    {
        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_TS_EN;
        p_npm_cfg->pkt_format.ts_offset = 46;

        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_SEQ_EN;
        p_npm_cfg->pkt_format.seq_num_offset = 42;
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
    {
        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_TS_EN;
        p_npm_cfg->pkt_format.ts_offset = 46 + 20;

        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_SEQ_EN;
        p_npm_cfg->pkt_format.seq_num_offset = 42 + 20;
    }

    p_npm_cfg->pkt_format.ipg = 20;

    if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
    {
        if (p_npm_attr->udp_src_port)
        {
            udp_src_port = p_npm_attr->udp_src_port & 0xFFFF;
             *((uint16*)(&tmp_pkt[34])) = sal_htons(udp_src_port);
        }

        if (p_npm_attr->udp_dst_port)
        {
            udp_dst_port = p_npm_attr->udp_dst_port & 0xFFFF;
             *((uint16*)(&tmp_pkt[36])) = sal_htons(udp_dst_port);
        }

        // for modify ip header ttl
        tmp_pkt[22] = p_npm_attr->ttl;

        // for modify ip header tos    
        tmp_pkt[15] = p_npm_attr->priority << 2;

        // for modify ip header length       
        ip_header_lenth = p_npm_attr->packet_length - 14 - 4;
        *((uint16*)(&tmp_pkt[16])) = sal_htons(ip_header_lenth);
        
        // for modify udp header length
        udp_header_lenth = p_npm_attr->packet_length - 34 - 4;
        *((uint16*)(&tmp_pkt[38])) = sal_htons(udp_header_lenth);


        // for modify the packet src ip
        sal_memcpy(&ipv4_addr_tmp, &p_npm_attr->src_ip.addr.ip4, sizeof(sai_ip4_t));
         *((uint32*)(&tmp_pkt[26])) = ipv4_addr_tmp;

        // for modify the packet dst ip
        ipv4_addr_tmp = 0;
        sal_memcpy(&ipv4_addr_tmp, &p_npm_attr->dst_ip.addr.ip4, sizeof(sai_ip4_t));
         *((uint32*)(&tmp_pkt[30])) = ipv4_addr_tmp;
            
        // for modify ip header checksum  
        status = _ctc_sai_calculate_ip_header_checsum(4, &checksum, tmp_pkt); 
        pkt_checksum = checksum & 0xFFFF;
        *((uint16*)(&tmp_pkt[24])) = sal_htons(pkt_checksum);        

        // for modify udp header checksum  
        status = _ctc_sai_calculate_udp_header_checsum(4, &checksum, p_npm_attr->packet_length - 4, 26, 38, 34, 42, tmp_pkt); 
        pkt_checksum = checksum & 0xFFFF;
        *((uint16*)(&tmp_pkt[40])) = sal_htons(pkt_checksum); 
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
    {
        if (p_npm_attr->udp_src_port)
        {
            udp_src_port = p_npm_attr->udp_src_port & 0xFFFF;
             *((uint16*)(&tmp_pkt[54])) = sal_htons(udp_src_port);
        }

        if (p_npm_attr->udp_dst_port)
        {
            udp_dst_port = p_npm_attr->udp_dst_port & 0xFFFF;
             *((uint16*)(&tmp_pkt[56])) = sal_htons(udp_dst_port);
        }

        // for modify ipv6 header ttl
        tmp_pkt[21] = p_npm_attr->ttl;
        
        // for modify ipv6 header tos
        tos = p_npm_attr->priority << 2;
        tmp_pkt[14] = tmp_pkt[14] + (tos >> 4);        
        tmp_pkt[15] = tmp_pkt[15] + (tos << 4); 

        // for modify ip header length       
        ip_header_lenth = p_npm_attr->packet_length - 54 - 4;
        *((uint16*)(&tmp_pkt[18])) = sal_htons(ip_header_lenth);
        
        // for modify udp header length
        udp_header_lenth = p_npm_attr->packet_length - 54 - 4;
        *((uint16*)(&tmp_pkt[58])) = sal_htons(udp_header_lenth);

        // for modify the packet src ip 
        sal_memcpy(ipv6_sa_addr, &p_npm_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
        *((uint32*)(&tmp_pkt[22])) = ipv6_sa_addr[0];
        *((uint32*)(&tmp_pkt[26])) = ipv6_sa_addr[1];
        *((uint32*)(&tmp_pkt[30])) = ipv6_sa_addr[2];
        *((uint32*)(&tmp_pkt[34])) = ipv6_sa_addr[3]; 

        // for modify the packet dst ip  
        sal_memcpy(ipv6_da_addr, &p_npm_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
        *((uint32*)(&tmp_pkt[38])) = ipv6_da_addr[0];
        *((uint32*)(&tmp_pkt[42])) = ipv6_da_addr[1];
        *((uint32*)(&tmp_pkt[46])) = ipv6_da_addr[2];
        *((uint32*)(&tmp_pkt[50])) = ipv6_da_addr[3]; 

        // for modify udp header checksum  
        status = _ctc_sai_calculate_udp_header_checsum(6, &checksum, p_npm_attr->packet_length - 4, 22, 58, 54, 62, tmp_pkt); 
        pkt_checksum = checksum & 0xFFFF;
        *((uint16*)(&tmp_pkt[60])) = sal_htons(pkt_checksum); 
    }
                
    // for init the npm test packet
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_npm_attr->dst_ip.addr_family)
    {
        status = _ctc_sai_npm_test_ipv4_packet(p_npm_attr, p_npm_cfg, tmp_pkt);
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_npm_attr->dst_ip.addr_family)
    {
        status = _ctc_sai_npm_test_ipv6_packet(p_npm_attr, p_npm_cfg, tmp_pkt);
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
        p_npm_cfg->pkt_format.pattern_type = CTC_NPM_PATTERN_TYPE_INC_BYTE;
        p_npm_cfg->pkt_format.repeat_pattern = 0x01;
    }

    return status;
}

static sai_status_t
ctc_sai_npm_parser_session_attr(uint32_t attr_count, const sai_attribute_t *attr_list, ctc_sai_npm_t *p_npm_attr)
{
    sai_status_t            status = SAI_STATUS_SUCCESS;
    uint32_t                index = 0;
    const sai_attribute_value_t     *attr_value = NULL;

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

    if ((p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_IP) || (p_npm_attr->encap_type == SAI_NPM_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI))
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_NPM_PORT, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_npm_attr->port_id = attr_value->oid;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }    
    }
    else
    {
        // Do not care npm port
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NPM_SESSION_ATTR_RECEIVE_PORT, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_npm_attr->receive_port_id = attr_value->oid;
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

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_TWAMP, npm_ctc_oid.value));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_L3IF, p_db_npm->l3if_id));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_npm->iloop_nexthop));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_npm->eloop_nexthop));    
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, p_db_npm->oam_acl_entry_id));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, npm_reserved_acl_group_id));

    if (SAI_NPM_SESSION_REFLECTOR == p_db_npm->role)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_L3IF, p_db_npm->oam_l3if_id));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_npm->oam_iloop_nh_id));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_npm->oam_eloop_nh_id));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, p_db_npm->loop_acl_entry_id));        
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

        if (p_npm_attr->user_nh_id)
        {
            status = SAI_STATUS_NOT_SUPPORTED;
            return status;
        }
    }

    return status;
}


#define ________SAI_API________

static sai_status_t
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
    uint32_t                global_port = 0;
    uint32_t                mep_index = 0;

    CTC_SAI_PTR_VALID_CHECK(npm_session_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    ctc_sai_oid_get_lchip(switch_id, &lchip);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_TWAMP, &npm_id));
    npm_tmp_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_NPM, lchip, 0, 0, npm_id);

    sal_memset(&npm_attr, 0, sizeof(ctc_sai_npm_t));
    status = ctc_sai_npm_parser_session_attr(attr_count, attr_list, &npm_attr);
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

    if (SAI_NPM_SESSION_SENDER == npm_attr.role)
    {
        // no need install oam maid and mep
    }
    else if (SAI_NPM_SESSION_REFLECTOR == npm_attr.role)
    {
        // Do not create the oam mep, RFC 2544/ 1564 test packet just swap ip and loop force route
    }

    if (TRUE == npm_attr.hw_lookup)
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_npm_create_e2iloop_nexthop_for_hw_lookup(&npm_attr, switch_id),status, error1);
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_gport(npm_attr.receive_port_id, &global_port),status, error4);
    if (SAI_NPM_SESSION_SENDER == npm_attr.role)
    {
        if (npm_attr.receive_port_id)
        {
            // for sender receive port enable acl match to oam engine
            sal_memset(&npm_cfg, 0, sizeof(npm_cfg));
            sal_memset(&acl_prop, 0, sizeof(acl_prop));
            acl_prop.acl_en = 1;
            acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY;
            acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_L2_L3;

            CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, global_port, &acl_prop),status, error4);
            CTC_SAI_CTC_ERROR_GOTO(ctc_sai_npm_mep_index_get_by_session_id(lchip, npm_id, &mep_index),status, error5);

            // get lmep_index by npm session id, due to tm start from 0x1FF7
            npm_attr.lmep_index = mep_index;
            npm_attr.is_loop_swap_ip = 1;
            ret = ctc_sai_npm_global_acl_add(npm_tmp_oid, &npm_attr);
            if (ret)
            {
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
                status = ctc_sai_mapping_error_ctc(ret);
                goto error5;
            }
        }

        if (SAI_IP_ADDR_FAMILY_IPV4 == npm_attr.src_ip.addr_family) 
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_npm_mapping_npm_session(&npm_attr, &npm_cfg, switch_id, npm_pkt_ipv4_header),status, error6);
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == npm_attr.src_ip.addr_family) 
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_npm_mapping_npm_session(&npm_attr, &npm_cfg, switch_id, npm_pkt_ipv6_header),status, error6);
        }

        session_id = npm_id & 0xFF;
        npm_cfg.session_id = session_id;
        ret = ctcs_npm_set_config(lchip, &npm_cfg);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error6;
        }

        // just for temp test
        ctc_sai_npm_write_hardware_table(lchip);

        if(npm_attr.trans_enable)
        {
            ret = ctcs_npm_set_transmit_en(lchip, session_id, npm_attr.trans_enable);
            if (ret)
            {
                CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
                status = ctc_sai_mapping_error_ctc(ret);
                goto error6;
            }
        }
    }
    else if (SAI_NPM_SESSION_REFLECTOR == npm_attr.role)
    {
        sal_memset(&acl_prop, 0, sizeof(acl_prop));
        acl_prop.acl_en = 1;
        acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY;
        acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_FORWARD;

        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, global_port, &acl_prop),status, error4);

        //npm_attr.is_loop_swap_ip = 0;
        ret = ctc_sai_npm_acl_add(npm_tmp_oid, &npm_attr);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error6;
        }
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_npm_build_db(lchip, npm_tmp_oid, &p_npm_info), status, error7);

    sal_memcpy(p_npm_info, &npm_attr, sizeof(ctc_sai_npm_t));

    *npm_session_id = npm_tmp_oid;

    return status;

error7:
    if (SAI_NPM_SESSION_REFLECTOR == p_npm_info->role)
    {
        ctc_sai_npm_acl_del(p_npm_info->loop_acl_entry_id, lchip);
    }
error6:
    if (SAI_NPM_SESSION_SENDER == npm_attr.role)
    {
        ctc_sai_npm_global_acl_del(npm_attr.oam_acl_entry_id, lchip);
    }
error5:     
    acl_prop.acl_en = 0;
    acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY; 
    ctcs_port_set_acl_property(lchip, global_port, &acl_prop);
    ctcs_port_set_acl_property(lchip, npm_attr.iloop_port, &acl_prop);     
error4:
    _ctc_sai_npm_remove_e2iloop_nexthop_for_hw_lookup(&npm_attr, lchip);    
error1:
    ctc_sai_db_free_id(lchip, SAI_OBJECT_TYPE_NPM, npm_id);
    
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "Failed to create npm session entry:%d\n", status);
    }

    return status;
}

static sai_status_t
ctc_sai_npm_remove_npm_session(sai_object_id_t npm_session_oid)
{
    ctc_sai_npm_t     *p_npm_info = NULL;
    sai_status_t        status = SAI_STATUS_SUCCESS;
    uint8               lchip = 0;
    uint32              session_id = 0;
    uint8               session_id_tmp = 0;
    int32               ret = 0;
    ctc_acl_property_t acl_prop;
    uint32          global_port = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_oid, &lchip));
    p_npm_info = ctc_sai_db_get_object_property(lchip, npm_session_oid);
    if (NULL == p_npm_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error1; 
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_gport(p_npm_info->receive_port_id, &global_port), status, error1);

    status = ctc_sai_oid_get_npm_session_id(npm_session_oid, &session_id);
    session_id_tmp = session_id & 0xFF;
    if (SAI_NPM_SESSION_SENDER == p_npm_info->role)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_npm_set_transmit_en(lchip, session_id_tmp, 0), status, error1);

        sal_memset(&acl_prop, 0, sizeof(acl_prop));
        acl_prop.acl_en = 0;
        acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, global_port, &acl_prop), status, error1);

        ret = ctc_sai_npm_global_acl_del(p_npm_info->oam_acl_entry_id, lchip);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error1; 
        }
    }
    else if (SAI_NPM_SESSION_REFLECTOR == p_npm_info->role)
    {
        sal_memset(&acl_prop, 0, sizeof(acl_prop));
        acl_prop.acl_en = 0;
        acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, global_port, &acl_prop), status, error1);

        ret = ctc_sai_npm_acl_del(p_npm_info->loop_acl_entry_id, lchip);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error1;
        }

        sal_memset(&acl_prop, 0, sizeof(acl_prop));
        acl_prop.acl_en = 0;
        acl_prop.acl_priority = NPM_PORT_ACL_LOOKUP_PRIORITY;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, p_npm_info->iloop_port, &acl_prop), status, error1);

        ret = ctc_sai_npm_global_acl_del(p_npm_info->oam_acl_entry_id, lchip);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error1;
        }
    }

    ret = ctcs_npm_clear_stats(lchip, session_id_tmp);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
        goto error1; 
    }

    if (TRUE == p_npm_info->hw_lookup)
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_npm_remove_e2iloop_nexthop_for_hw_lookup(p_npm_info, lchip), status, error1);
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_npm_remove_db(lchip, npm_session_oid),status, error1);
    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_TWAMP, session_id);

    return status;

error1:    
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "Failed to remove npm session entry:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_npm_get_npm_session_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t        status = SAI_STATUS_SUCCESS;
    uint8               lchip = 0;
    ctc_sai_npm_t     *p_npm_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_npm_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_npm_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_NPM_SESSION_ATTR_NPM_PORT:
            attr->value.oid = p_npm_info->port_id;
            break;

        case SAI_NPM_SESSION_ATTR_RECEIVE_PORT:
            attr->value.oid = p_npm_info->receive_port_id;
            break;
        
        case SAI_NPM_SESSION_ATTR_SESSION_ROLE:
            attr->value.s32 = p_npm_info->role;
            break;

        case SAI_NPM_SESSION_ATTR_UDP_SRC_PORT:
            attr->value.u32 = p_npm_info->udp_src_port;
            break;

        case SAI_NPM_SESSION_ATTR_UDP_DST_PORT:
            attr->value.u32 = p_npm_info->udp_dst_port;
            break;

        case SAI_NPM_SESSION_ATTR_SRC_IP:
            sal_memcpy(&attr->value.ipaddr, &p_npm_info->src_ip, sizeof(sai_ip_address_t));
            break;

        case SAI_NPM_SESSION_ATTR_DST_IP:
            sal_memcpy(&attr->value.ipaddr, &p_npm_info->dst_ip, sizeof(sai_ip_address_t));
            break;

        case SAI_NPM_SESSION_ATTR_TC:
            attr->value.u8 = p_npm_info->priority;
            break;

        case SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER:
            attr->value.oid = p_npm_info->vrf_oid;
            break;

        case SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE:
            attr->value.s32 = p_npm_info->encap_type;
            break;

        case SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
            attr->value.booldata = p_npm_info->trans_enable;
            break;

        case SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID:
            attr->value.booldata = p_npm_info->hw_lookup;
            break;

        case SAI_NPM_SESSION_ATTR_PACKET_LENGTH:
            attr->value.u32 = p_npm_info->packet_length;
            break;

        case SAI_NPM_SESSION_ATTR_PKT_TX_MODE:
            attr->value.s32 = p_npm_info->pkt_tx_mode;
            break;

        case SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD:
            attr->value.u32 = p_npm_info->period;
            break;

        case SAI_NPM_SESSION_ATTR_TX_RATE:
            attr->value.u32 = p_npm_info->tx_rate;
            break;

        case SAI_NPM_SESSION_ATTR_TX_PKT_CNT:
            attr->value.u32 = p_npm_info->pkt_cnt;
            break;

        case SAI_NPM_SESSION_ATTR_TX_PKT_DURATION:
            attr->value.u32 = p_npm_info->pkt_duration;
            break;

        default:
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "Get npm attribute not implement\n");
            return  SAI_STATUS_NOT_IMPLEMENTED + attr_idx;
    }

    return status;
}

static sai_status_t 
ctc_sai_npm_set_npm_session_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    sai_status_t        status = SAI_STATUS_SUCCESS;
    ctc_sai_npm_t     *p_npm_info = NULL;
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
    { SAI_NPM_SESSION_ATTR_NPM_PORT,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    }, 
    { SAI_NPM_SESSION_ATTR_RECEIVE_PORT,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr 
    },    
    { SAI_NPM_SESSION_ATTR_SESSION_ROLE,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr 
    },
    { SAI_NPM_SESSION_ATTR_UDP_SRC_PORT,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_UDP_DST_PORT,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_SRC_IP,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_DST_IP,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_TC,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_PACKET_LENGTH,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_PKT_TX_MODE,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_TX_RATE,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_TX_PKT_CNT,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    },
    { SAI_NPM_SESSION_ATTR_TX_PKT_DURATION,
      ctc_sai_npm_get_npm_session_attr,
      ctc_sai_npm_set_npm_session_attr
    }
};

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
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "Failed to set stp attr:%d, status:%d\n", attr->id,status);
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

int32
ctc_sai_npm_time_delay_transfer(uint64 time, uint32* time_s, uint32* time_ms, uint32* time_us, uint32* time_ns)
{
    *time_s = time / 1000000000;
    *time_ms = (time - ((*time_s) * 1000000000)) / 1000000;
    *time_us = (time - ((*time_s) * 1000000000) - ((*time_ms) * 1000000)) / 1000;
    *time_ns = time - (*time_s) * 1000000000 - (*time_ms) * 1000000 - (*time_us) * 1000;

    return 0;
}

sai_status_t
ctc_sai_npm_get_npm_session_stats(sai_object_id_t npm_session_id, 
                                        uint32_t number_of_counters, 
                                        const sai_stat_id_t *counter_ids, 
                                        uint64_t *counters)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32   ret = 0;
    uint8   lchip = 0;
    uint8   session_id = 0;
    uint32  tmp_session_id = 0;
    uint64  duration_ts = 0;
    uint64  fl = 0;
    uint8   stats_index = 0;
    ctc_npm_stats_t npm_stats;
    ctc_sai_npm_t     *p_npm_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NPM);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);

    sal_memset(&npm_stats, 0, sizeof(ctc_npm_stats_t));
    
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_id, &lchip));
    p_npm_info = ctc_sai_db_get_object_property(lchip, npm_session_id);
    if (NULL == p_npm_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    status = ctc_sai_oid_get_npm_session_id(npm_session_id, &tmp_session_id);
    session_id = tmp_session_id & 0xFF;
    
    ret = ctcs_npm_get_stats(lchip, session_id, &npm_stats);
    duration_ts = (npm_stats.last_ts >= npm_stats.first_ts) ? (npm_stats.last_ts - npm_stats.first_ts) : 0;

    /*FL*/
    if (0 == npm_stats.tx_en)
    {
        if (npm_stats.tx_pkts >= npm_stats.rx_pkts)
        {
            fl = npm_stats.tx_pkts - npm_stats.rx_pkts;
        }
    }

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

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(npm_session_oid, &lchip));
    p_npm_info = ctc_sai_db_get_object_property(lchip, npm_session_oid);
    if (NULL == p_npm_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
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
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_NPM;
    wb_info.data_len = sizeof(ctc_sai_npm_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_npm_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_NPM, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    ctc_sai_npm_global_acl_init();
    ctc_sai_npm_init_session_max(lchip);
    
    if (1 == SDK_WORK_PLATFORM)
    {
        ctc_sai_npm_write_hardware_table(lchip); 
    } 
    
    return SAI_STATUS_SUCCESS;
}

