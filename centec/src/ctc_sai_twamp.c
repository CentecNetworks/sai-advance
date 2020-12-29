/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"
#include "saitwamp.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_port.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_twamp.h"
#include "ctcs_api.h"


static uint32_t twamp_oam_maid_ref_cnt = 0;

typedef struct ctc_sai_twamp_master_s
{
    uint32 twamp_reserved_ingress_acl_group_id;
    
} ctc_sai_twamp_master_t;

ctc_sai_twamp_master_t* p_ctc_sai_twamp[CTC_MAX_LOCAL_CHIP_NUM] = {NULL};


typedef struct  ctc_sai_twamp_master_wb_s
{
    /*key*/
    uint32 lchip;
    uint32 calc_key_len[0];
    
    /*data*/    
    uint32 twamp_reserved_ingress_acl_group_id;
    
}ctc_sai_twamp_master_wb_t;



uint8 twamp_pkt_ipv4_header[9600] =
{
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x08, 0x00, 0x45, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00,
};

uint8 twamp_pkt_ipv6_header[9600] =
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
_ctc_sai_calculate_udp_header_checsum(uint8 addr_family, int32 *checksum_ptr , uint32 pkt_len, uint32 ipaddr_offset, uint32 udplen_offset, uint32 udphead_offset, uint32 twamp_data_offset, uint8 *pkt  )
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
    for (i = 0; i < pkt_len - twamp_data_offset ; i = i + 2 )
    {   
        j = i + twamp_data_offset;                    
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
_ctc_sai_twamp_test_ipv4_packet(ctc_sai_twamp_t *p_twamp_attr, ctc_npm_cfg_t *p_npm, uint8 *pkt)
{
    p_npm->pkt_format.pkt_header = (void*)pkt;
    p_npm->pkt_format.header_len = 83;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_twamp_test_ipv6_packet(ctc_sai_twamp_t *p_twamp_attr, ctc_npm_cfg_t *p_npm, uint8 *pkt)
{
    p_npm->pkt_format.pkt_header = (void*)pkt;
    p_npm->pkt_format.header_len = 103;

    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_twamp_write_hardware_table(uint8 lchip)
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



static int32
_ctc_sai_twamp_build_maid_twamp(ctc_oam_maid_t* maid, char* md_name, char* ma_name)
{
    uint8 md_name_len = 0;
    uint8 ma_name_len = 0;
    uint8 maid_len = 0;

    md_name_len = sal_strlen(md_name);
    ma_name_len = sal_strlen(ma_name);
    if (md_name_len > 43)
    {
        return -1;
    }
    else
    {
        if (ma_name_len > (44 - md_name_len))
        {
            return -1;
        }
    }

    maid->maid[0] = 0x4;  /* MD name format */
    maid->maid[1] = md_name_len; /* MD name len */
    sal_memcpy(&maid->maid[2], md_name, md_name_len); /* copy md name string */

    maid->maid[2 + md_name_len] = 0x2; /* MA name format */
    maid->maid[3 + md_name_len] = ma_name_len; /* MA name len */
    sal_memcpy(&maid->maid[4 + md_name_len], ma_name, ma_name_len);

    maid_len = 4 + md_name_len + ma_name_len;
    maid->maid_len = maid_len;

    return 0;
}


static sai_status_t
_ctc_sai_twamp_create_oam_maid(uint8 lchip)
{
    ctc_oam_maid_t maid;
    char  md_name[] = "npm";
    char  ma_name[] = "twamp";
    int32 ret = 0;
    sai_status_t  status = SAI_STATUS_SUCCESS;

    sal_memset(&maid, 0, sizeof(maid));

    maid.mep_type = CTC_OAM_MEP_TYPE_ETH_1AG;

    ret = _ctc_sai_twamp_build_maid_twamp(&maid, md_name, ma_name);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%invalid md name or ma name \n");
        status = ctc_sai_mapping_error_ctc(ret);
    }

    ret = ctcs_oam_add_maid(lchip, &maid);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% fail to add twamp oam maid \n");
        status = ctc_sai_mapping_error_ctc(ret);
    }

    return status;
}

static sai_status_t
_ctc_sai_twamp_remove_oam_maid(uint8 lchip)
{
    ctc_oam_maid_t maid;
    char  md_name[] = "npm";
    char  ma_name[] = "twamp";
    int32 ret = 0;
    sai_status_t  status = SAI_STATUS_SUCCESS;

    sal_memset(&maid, 0, sizeof(maid));
    
    maid.mep_type = CTC_OAM_MEP_TYPE_ETH_1AG;

    ret = _ctc_sai_twamp_build_maid_twamp(&maid, md_name, ma_name);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%invalid md name or ma name \n");
        status = ctc_sai_mapping_error_ctc(ret);
    }

    ret = ctcs_oam_remove_maid(lchip, &maid);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% fail to remove twamp oam maid  \n");
        status = ctc_sai_mapping_error_ctc(ret);
    }

    return status;
}


static sai_status_t
_ctc_sai_twamp_create_e2iloop_nexthop_for_oam(ctc_sai_twamp_t *p_twamp_attr, sai_object_id_t switch_id)
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

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));

     /*alloc global iloop port */
     
     sal_memset(&port_assign, 0, sizeof(port_assign));
     
     port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;    
     CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
     port_assign.gchip = gchip;    
     ret = ctcs_alloc_internal_port(lchip, &port_assign);   
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     
     CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate internal iloop port is %d\n", port_assign.inter_port);
     
     /*config inner l3if */
     
     sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
     ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id);
     l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
     l3if.gport = port_assign.inter_port;
     ret = ctcs_l3if_create(lchip, l3if_id, &l3if);   
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     
     CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate l3if_id is %d\n", l3if_id);

     l3if_prop = CTC_L3IF_PROP_ROUTE_EN;
     ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     l3if_prop = CTC_L3IF_PROP_IPV4_UCAST;
     ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     l3if_prop = CTC_L3IF_PROP_IPV4_MCAST;
     ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     l3if_prop = CTC_L3IF_PROP_IPV6_UCAST;
     ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     l3if_prop = CTC_L3IF_PROP_ROUTE_ALL_PKT;
     ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     l3if_prop = CTC_L3IF_PROP_VRF_EN;
     ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     
     /* for vpn instance */
     
     if (p_twamp_attr->vrf_oid)
     {
         uint32 vrf_id_tmp = 0;
         ctc_sai_oid_get_vrf_id_u32(p_twamp_attr->vrf_oid, &vrf_id_tmp);
     
         l3if_prop = CTC_L3IF_PROP_VRF_ID;
         ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, vrf_id_tmp);
         if (ret)
         {
             CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
             status = ctc_sai_mapping_error_ctc(ret);
         }
     }
     ret = ctcs_port_set_phy_if_en(lchip, port_assign.inter_port, 1);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     
     /* add iloop nexthop */
     
     ctc_loopback_nexthop_param_t iloop_nh;
     sal_memset(&iloop_nh, 0, sizeof(ctc_loopback_nexthop_param_t));
     ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid);  
       
     iloop_nh.lpbk_lport = port_assign.inter_port;
     ret = ctcs_nh_add_iloop(lchip, nhid, &iloop_nh);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     
     p_twamp_attr->oam_l3if_id = l3if_id;
     
     p_twamp_attr->oam_iloop_port = port_assign.inter_port;
     p_twamp_attr->oam_iloop_nh_id = nhid;

     CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate iloop nexthop id  is %d\n", nhid); 
     
     /*alloc global eloop port */
     
     sal_memset(&port_assign, 0, sizeof(port_assign));
     port_assign.type = CTC_INTERNAL_PORT_TYPE_ELOOP;
     CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
     port_assign.gchip = gchip;
     port_assign.nhid = p_twamp_attr->oam_iloop_nh_id;   
     ret = ctcs_alloc_internal_port(lchip, &port_assign);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }
     
     CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate internal eloop port is %d\n", port_assign.inter_port);
     
     /* add eloop nexthop */
     
     ctc_misc_nh_param_t nh_param;
     
     sal_memset(&nh_param, 0, sizeof(ctc_misc_nh_param_t));
     
     ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid);
  
     nh_param.type = CTC_MISC_NH_TYPE_FLEX_EDIT_HDR;
     nh_param.gport = port_assign.inter_port;

     nh_param.misc_param.flex_edit.packet_type = CTC_MISC_NH_PACKET_TYPE_UDPORTCP;
     
     nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_IP_HDR;
     nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_SWAP_IP;         

     nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_L4_HDR;
     nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_SWAP_L4_PORT;
     
     nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_UDP_PORT;

     nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_UPDATE_UDP_CHKSUM;
     
     nh_param.misc_param.flex_edit.dscp_select = CTC_NH_DSCP_SELECT_NONE;
     
     if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family )
     {
         nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_IPV4;
     }

     ret = ctcs_nh_add_misc(lchip, nhid, &nh_param);
     if (ret)
     {
         CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
         status = ctc_sai_mapping_error_ctc(ret);
     }     
   
    p_twamp_attr->oam_eloop_port = port_assign.inter_port;
    p_twamp_attr->oam_eloop_nh_id = nhid;
    
    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate eloop nexthop id  is %d\n", nhid);   

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_twamp_remove_e2iloop_nexthop_for_oam(ctc_sai_twamp_t *p_twamp_attr, uint8 lchip)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           ret = 0;
    uint8           gchip = 0;
    uint32          l3if_id = 0;
    ctc_l3if_t      l3if;
    ctc_internal_port_assign_para_t port_assign;

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);

    /* delete l3if  */
    
    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
    l3if.gport = p_twamp_attr->oam_iloop_port;
    l3if_id = p_twamp_attr->oam_l3if_id;

    ret = ctcs_l3if_destory(lchip, l3if_id, &l3if);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
 
    ret = ctcs_port_set_phy_if_en(lchip, l3if.gport, 0);    
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, l3if_id);

    /* delete internel port  */

    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.gchip = gchip;
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;
    port_assign.inter_port = p_twamp_attr->oam_iloop_port;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_free_internal_port(lchip, &port_assign));
    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The dealloc internal port is %d\n", port_assign.inter_port);
    
    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ELOOP;
    port_assign.gchip = gchip;
    port_assign.inter_port = p_twamp_attr->oam_eloop_port;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_free_internal_port(lchip, &port_assign));
    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The dealloc internal port is %d\n", port_assign.inter_port);

    /* delete loop nexthop  */  
    
    ret = ctcs_nh_remove_iloop(lchip, p_twamp_attr->oam_iloop_nh_id);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }    
    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_twamp_attr->oam_iloop_nh_id);    
        
    ret = ctcs_nh_remove_misc(lchip, p_twamp_attr->oam_eloop_nh_id);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }    
    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_twamp_attr->oam_eloop_nh_id);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_twamp_create_oam_mep_index(ctc_sai_twamp_t *p_twamp_attr, sai_object_id_t switch_id, uint32_t twamp_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8           lchip = 0;
    int32           ret = 0;
    ctc_oam_maid_t  maid;
    char            md_name[] = "npm";
    char            ma_name[] = "twamp";
    ctc_oam_lmep_t  lmep;
    ctc_oam_y1731_lmep_t* p_y1731_lmep  = &lmep.u.y1731_lmep;
    uint32 nexthop_id_tmp = 0;
    uint32 bit_cnt = 0;
    uint8  gchip = 0;    

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);

    sal_memset(&lmep, 0, sizeof(lmep));
    sal_memset(&maid, 0, sizeof(maid));

    maid.mep_type = CTC_OAM_MEP_TYPE_ETH_1AG;  // need to get from ctcs_oam_add_maid
    
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    ctcs_get_gchip_id(lchip, &gchip);

    
    if( p_twamp_attr->receive_port_count )
    {
    
        for (bit_cnt = 0; bit_cnt < sizeof(p_twamp_attr->receive_port_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_twamp_attr->receive_port_bits, bit_cnt))
            {
                lmep.key.u.eth.gport = CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt); 
                break;
            }
        }
    }



    
    lmep.key.u.eth.md_level = TWAMP_ADD_MEP_KEY_RESERVED_LEVEL;
    lmep.key.u.eth.l2vpn_oam_id = TWAMP_ADD_MEP_KEY_RESERVED_FID + twamp_id;

    ret = _ctc_sai_twamp_build_maid_twamp(&maid, md_name, ma_name);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%invalid md name or ma name \n");
    }
    else
    {
        sal_memcpy(&lmep.maid, &maid, sizeof(maid));
    }

    p_y1731_lmep->tpid_index = CTC_PARSER_L2_TPID_SVLAN_TPID_0;
    p_y1731_lmep->ccm_interval = TWAMP_OAM_CCM_INTERVAL;
    p_y1731_lmep->mep_id = TWAMP_ADD_MEP_RESERVED_MEP_ID;                    
    p_y1731_lmep->flag |= CTC_OAM_Y1731_LMEP_FLAG_MEP_EN;       
    p_y1731_lmep->flag |= CTC_OAM_Y1731_LMEP_FLAG_TWAMP_EN;    

    if (SAI_TWAMP_SESSION_ROLE_REFLECTOR == p_twamp_attr->role)
    {
        if (p_twamp_attr->user_nh_id)
        {
            ctc_sai_oid_get_nexthop_id(p_twamp_attr->user_nh_id, &nexthop_id_tmp);
            p_y1731_lmep->nhid = nexthop_id_tmp;           
        } 
        else
        {    
            status = _ctc_sai_twamp_create_e2iloop_nexthop_for_oam(p_twamp_attr, switch_id);
            p_y1731_lmep->nhid = p_twamp_attr->oam_eloop_nh_id;
        }
        p_y1731_lmep->flag |= CTC_OAM_Y1731_LMEP_FLAG_TWAMP_REFLECT_EN;
    }

    ret = ctcs_oam_add_lmep(lchip, &lmep);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% failed to add lmep \n");
        status = ctc_sai_mapping_error_ctc(ret);
    }
    else
    {
        p_twamp_attr->lmep_index = lmep.lmep_index;
    }

    return status;
}

static sai_status_t
_ctc_sai_twamp_remove_oam_mep_index(ctc_sai_twamp_t *p_twamp_attr, sai_object_id_t session_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8           lchip = 0;
    int32           ret = 0;
    uint32          session_id_tmp = 0;
    ctc_oam_lmep_t  lmep;
    uint32 bit_cnt = 0;
    uint8  gchip = 0; 

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);

    ctc_sai_oid_get_lchip(session_id, &lchip);
    status = ctc_sai_oid_get_twamp_session_id(session_id, &session_id_tmp);

    ctcs_get_gchip_id(lchip, &gchip);
    
    sal_memset(&lmep, 0, sizeof(lmep));
    lmep.key.mep_type = CTC_OAM_MEP_TYPE_ETH_1AG;
    
    if( p_twamp_attr->receive_port_count )
    {
    
        for (bit_cnt = 0; bit_cnt < sizeof(p_twamp_attr->receive_port_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_twamp_attr->receive_port_bits, bit_cnt))
            {
                lmep.key.u.eth.gport = CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt); 
                break;
            }
        }
    }

    
    lmep.key.u.eth.md_level = TWAMP_ADD_MEP_KEY_RESERVED_LEVEL; 
    lmep.key.u.eth.l2vpn_oam_id = TWAMP_ADD_MEP_KEY_RESERVED_FID + session_id_tmp;
    lmep.u.y1731_lmep.flag |= CTC_OAM_Y1731_LMEP_FLAG_TWAMP_EN;
    
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(session_id, &lchip));
    ret = ctcs_oam_remove_lmep(lchip, &lmep);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    if (SAI_TWAMP_SESSION_ROLE_REFLECTOR == p_twamp_attr->role)
    {
        if (p_twamp_attr->user_nh_id)
        {
            // do nothing, nexthop id is not created by sai
        }
        else
        {
            // need to remove the iloop nexthop
            status = _ctc_sai_twamp_remove_e2iloop_nexthop_for_oam(p_twamp_attr, lchip);
        }
    }
    
    return status;
}

static sai_status_t
_ctc_sai_twamp_update_oam_mep(ctc_sai_twamp_t *p_twamp_attr, uint32_t session_id, uint8 lchip)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           ret = 0;    
    uint32          oam_session_id = 0xff;
    ctc_oam_update_t    lmep_update;
    uint32 bit_cnt = 0;
    uint8  gchip = 0; 

    sal_memset(&lmep_update, 0, sizeof(lmep_update));
    
    lmep_update.is_local = 1;

    oam_session_id = session_id;

    ctcs_get_gchip_id(lchip, &gchip);


    if( p_twamp_attr->receive_port_count )
    {
    
        for (bit_cnt = 0; bit_cnt < sizeof(p_twamp_attr->receive_port_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_twamp_attr->receive_port_bits, bit_cnt))
            {
                lmep_update.key.u.eth.gport = CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt); 
                break;
            }
        }
    }

    lmep_update.key.u.eth.l2vpn_oam_id = TWAMP_ADD_MEP_KEY_RESERVED_FID + session_id;
    lmep_update.key.u.eth.md_level = TWAMP_ADD_MEP_KEY_RESERVED_LEVEL;       
    lmep_update.update_type    = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_NPM;
    lmep_update.update_value   = oam_session_id;
    
    ret = ctcs_oam_update_lmep(lchip, &lmep_update);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    return status;
}


static sai_status_t
ctc_sai_twamp_acl_build_param_field(ctc_sai_twamp_t *p_twamp_attr, twamp_acl_param_t *acl_entry)
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

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);
    CTC_SAI_PTR_VALID_CHECK(acl_entry);

    entry_id = p_twamp_attr->loop_acl_entry_id;

    /* Mapping keys */
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
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

    if (p_twamp_attr->is_loop_swap_ip)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_SA;
            ipv4_sa = sal_htonl(p_twamp_attr->dst_ip.addr.ip4);
            field_key.data = ipv4_sa;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_DA;
            ipv4_da = sal_htonl(p_twamp_attr->src_ip.addr.ip4);
            field_key.data = ipv4_da;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_PROTOCOL;
            field_key.data = 17;   // UDP protocol
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IPV6_SA;
            sal_memcpy(ipv6_sa_addr, &p_twamp_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
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
            sal_memcpy(ipv6_da_addr, &p_twamp_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
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
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_SA;
            ipv4_sa = sal_htonl(p_twamp_attr->src_ip.addr.ip4);
            field_key.data = ipv4_sa;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_DA;
            ipv4_da = sal_htonl(p_twamp_attr->dst_ip.addr.ip4);
            field_key.data = ipv4_da;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);

            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IP_PROTOCOL;
            field_key.data = 17;   // UDP protocol
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_IPV6_SA;
            sal_memcpy(ipv6_sa_addr, &p_twamp_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
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
            sal_memcpy(ipv6_da_addr, &p_twamp_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
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

    
    if (p_twamp_attr->priority)
    {
        sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

        field_key.type = CTC_FIELD_KEY_IP_DSCP;
        field_key.data = p_twamp_attr->priority;
        field_key.mask = 0xFFFFFFFF;

        rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
    }
    

    if (p_twamp_attr->is_loop_swap_ip)
    {
        if (p_twamp_attr->udp_dst_port)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_L4_SRC_PORT;
            field_key.data = p_twamp_attr->udp_dst_port;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }

        if (p_twamp_attr->udp_src_port)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_L4_DST_PORT;
            field_key.data = p_twamp_attr->udp_src_port;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
    }
    else
    {
        if (p_twamp_attr->udp_dst_port)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_L4_DST_PORT;
            field_key.data = p_twamp_attr->udp_dst_port;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }

        if (p_twamp_attr->udp_src_port)
        {
            sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

            field_key.type = CTC_FIELD_KEY_L4_SRC_PORT;
            field_key.data = p_twamp_attr->udp_src_port;
            field_key.mask = 0xFFFFFFFF;

            rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
        }
    }

    if ( SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI == p_twamp_attr->encap_type )
    {
        sal_memset(&field_key, 0, sizeof(ctc_field_key_t));

        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_twamp_attr->port_id, &global_port));
        field_key.type = CTC_FIELD_KEY_DST_GPORT;
        field_key.data = global_port;
        field_key.mask = 0xFFFFFFFF;

        rc = ctcs_acl_add_key_field(lchip, entry_id, &field_key);
    }

    return SAI_STATUS_SUCCESS;
}
    
static sai_status_t
ctc_sai_twamp_acl_build_param(ctc_sai_twamp_t *p_twamp_attr, twamp_acl_param_t *acl_entry)
{
    ipv6_addr_t     ipv6_sa_addr = {0};
    ipv6_addr_t     ipv6_da_addr = {0};

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);
    CTC_SAI_PTR_VALID_CHECK(acl_entry);
    
    /* Mapping keys */
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
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

    
    if (p_twamp_attr->is_loop_swap_ip)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
        {
            
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_IP_SA); 
            acl_entry->key.u.ipv4_key.ip_sa = sal_htonl(p_twamp_attr->dst_ip.addr.ip4);
            acl_entry->key.u.ipv4_key.ip_sa_mask = 0xFFFFFFFF;
            
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_IP_DA);
            acl_entry->key.u.ipv4_key.ip_da = sal_htonl(p_twamp_attr->src_ip.addr.ip4);
            acl_entry->key.u.ipv4_key.ip_da_mask = 0xFFFFFFFF;
            
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L4_PROTOCOL);
            acl_entry->key.u.ipv4_key.l4_protocol = 17;
            acl_entry->key.u.ipv4_key.l4_protocol_mask = 0xFF;
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
        {

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_IP_SA);
            sal_memcpy(ipv6_sa_addr, &p_twamp_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_sa_addr[0] = sal_htonl(ipv6_sa_addr[0]);
            ipv6_sa_addr[1] = sal_htonl(ipv6_sa_addr[1]);
            ipv6_sa_addr[2] = sal_htonl(ipv6_sa_addr[2]);
            ipv6_sa_addr[3] = sal_htonl(ipv6_sa_addr[3]);
            sal_memcpy(&acl_entry->key.u.ipv6_key.ip_sa, ipv6_sa_addr, sizeof(ipv6_addr_t));
            sal_memset(&acl_entry->key.u.ipv6_key.ip_sa_mask, 0xff, sizeof(ipv6_addr_t));

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_IP_DA);
            sal_memcpy(ipv6_da_addr, &p_twamp_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_da_addr[0] = sal_htonl(ipv6_da_addr[0]);
            ipv6_da_addr[1] = sal_htonl(ipv6_da_addr[1]);
            ipv6_da_addr[2] = sal_htonl(ipv6_da_addr[2]);
            ipv6_da_addr[3] = sal_htonl(ipv6_da_addr[3]);
            sal_memcpy(&acl_entry->key.u.ipv6_key.ip_da, ipv6_da_addr, sizeof(ipv6_addr_t));
            sal_memset(&acl_entry->key.u.ipv6_key.ip_da_mask, 0xff, sizeof(ipv6_addr_t));
            
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L4_PROTOCOL);
            acl_entry->key.u.ipv6_key.l4_protocol = 17;
            acl_entry->key.u.ipv6_key.l4_protocol_mask = 0xFF;
        }
    }
    else
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
        {
            
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_IP_SA);
            acl_entry->key.u.ipv4_key.ip_sa = sal_htonl(p_twamp_attr->src_ip.addr.ip4);
            acl_entry->key.u.ipv4_key.ip_sa_mask = 0xFFFFFFFF;
            
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_IP_DA);
            acl_entry->key.u.ipv4_key.ip_da = sal_htonl(p_twamp_attr->dst_ip.addr.ip4);
            acl_entry->key.u.ipv4_key.ip_da_mask = 0xFFFFFFFF;
            
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_L4_PROTOCOL);
            acl_entry->key.u.ipv4_key.l4_protocol = 17;
            acl_entry->key.u.ipv4_key.l4_protocol_mask = 0xFF;
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_IP_SA);
            sal_memcpy(ipv6_sa_addr, &p_twamp_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_sa_addr[0] = sal_htonl(ipv6_sa_addr[0]);
            ipv6_sa_addr[1] = sal_htonl(ipv6_sa_addr[1]);
            ipv6_sa_addr[2] = sal_htonl(ipv6_sa_addr[2]);
            ipv6_sa_addr[3] = sal_htonl(ipv6_sa_addr[3]);
            sal_memcpy(&acl_entry->key.u.ipv6_key.ip_sa, ipv6_sa_addr, sizeof(ipv6_addr_t));
            sal_memset(&acl_entry->key.u.ipv6_key.ip_sa_mask, 0xff, sizeof(ipv6_addr_t));

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_IP_DA);
            sal_memcpy(ipv6_da_addr, &p_twamp_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
            ipv6_da_addr[0] = sal_htonl(ipv6_da_addr[0]);
            ipv6_da_addr[1] = sal_htonl(ipv6_da_addr[1]);
            ipv6_da_addr[2] = sal_htonl(ipv6_da_addr[2]);
            ipv6_da_addr[3] = sal_htonl(ipv6_da_addr[3]);
            sal_memcpy(&acl_entry->key.u.ipv6_key.ip_da, ipv6_da_addr, sizeof(ipv6_addr_t));
            sal_memset(&acl_entry->key.u.ipv6_key.ip_da_mask, 0xff, sizeof(ipv6_addr_t));

            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_L4_PROTOCOL);
            acl_entry->key.u.ipv6_key.l4_protocol = 17;
            acl_entry->key.u.ipv6_key.l4_protocol_mask = 0xFF;
        }
    }
    
    if (p_twamp_attr->priority)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv4_key.flag, CTC_ACL_IPV4_KEY_FLAG_DSCP);
            acl_entry->key.u.ipv4_key.dscp = p_twamp_attr->priority;
            acl_entry->key.u.ipv4_key.dscp_mask = 0xFF;
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
        {
            CTC_SET_FLAG(acl_entry->key.u.ipv6_key.flag, CTC_ACL_IPV6_KEY_FLAG_DSCP);
            acl_entry->key.u.ipv6_key.dscp = p_twamp_attr->priority;
            acl_entry->key.u.ipv6_key.dscp_mask = 0xFF;
        }
    }
    

    if (p_twamp_attr->is_loop_swap_ip)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
        {
            if (p_twamp_attr->udp_dst_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.sub_flag, CTC_ACL_IPV4_KEY_SUB_FLAG_L4_SRC_PORT);
                acl_entry->key.u.ipv4_key.l4_src_port_use_mask = 1;
                acl_entry->key.u.ipv4_key.l4_src_port_0 = p_twamp_attr->udp_dst_port & 0xFFFF;
                acl_entry->key.u.ipv4_key.l4_src_port_1 = 0xFFFF;
            }

            if (p_twamp_attr->udp_src_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.sub_flag, CTC_ACL_IPV4_KEY_SUB_FLAG_L4_DST_PORT);
                acl_entry->key.u.ipv4_key.l4_dst_port_use_mask = 1;
                acl_entry->key.u.ipv4_key.l4_dst_port_0 = p_twamp_attr->udp_src_port & 0xFFFF;
                acl_entry->key.u.ipv4_key.l4_dst_port_1 = 0xFFFF;
            }
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
        {
            if (p_twamp_attr->udp_dst_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.sub_flag, CTC_ACL_IPV6_KEY_SUB_FLAG_L4_SRC_PORT);
                acl_entry->key.u.ipv6_key.l4_src_port_use_mask = 1;
                acl_entry->key.u.ipv6_key.l4_src_port_0 = p_twamp_attr->udp_dst_port & 0xFFFF;
                acl_entry->key.u.ipv6_key.l4_src_port_1 = 0xFFFF;
            }

            if (p_twamp_attr->udp_src_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.sub_flag, CTC_ACL_IPV6_KEY_SUB_FLAG_L4_DST_PORT);
                acl_entry->key.u.ipv6_key.l4_dst_port_use_mask = 1;
                acl_entry->key.u.ipv6_key.l4_dst_port_0 = p_twamp_attr->udp_src_port & 0xFFFF;
                acl_entry->key.u.ipv6_key.l4_dst_port_1 = 0xFFFF;
            }
        }
    }
    else
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
        {
            if (p_twamp_attr->udp_dst_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.sub_flag, CTC_ACL_IPV4_KEY_SUB_FLAG_L4_DST_PORT);
                acl_entry->key.u.ipv4_key.l4_dst_port_use_mask = 1;
                acl_entry->key.u.ipv4_key.l4_dst_port_0 = p_twamp_attr->udp_dst_port & 0xFFFF;
                acl_entry->key.u.ipv4_key.l4_dst_port_1 = 0xFFFF;
            }

            if (p_twamp_attr->udp_src_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv4_key.sub_flag, CTC_ACL_IPV4_KEY_SUB_FLAG_L4_SRC_PORT);
                acl_entry->key.u.ipv4_key.l4_src_port_use_mask = 1;
                acl_entry->key.u.ipv4_key.l4_src_port_0 = p_twamp_attr->udp_src_port & 0xFFFF;
                acl_entry->key.u.ipv4_key.l4_src_port_1 = 0xFFFF;
            }
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
        {
            if (p_twamp_attr->udp_dst_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.sub_flag, CTC_ACL_IPV6_KEY_SUB_FLAG_L4_DST_PORT);
                acl_entry->key.u.ipv6_key.l4_dst_port_use_mask = 1;
                acl_entry->key.u.ipv6_key.l4_dst_port_0 = p_twamp_attr->udp_dst_port & 0xFFFF;
                acl_entry->key.u.ipv6_key.l4_dst_port_1 = 0xFFFF;
            }

            if (p_twamp_attr->udp_src_port)
            {
                CTC_SET_FLAG(acl_entry->key.u.ipv6_key.sub_flag, CTC_ACL_IPV6_KEY_SUB_FLAG_L4_SRC_PORT);
                acl_entry->key.u.ipv6_key.l4_src_port_use_mask = 1;
                acl_entry->key.u.ipv6_key.l4_src_port_0 = p_twamp_attr->udp_src_port & 0xFFFF;
                acl_entry->key.u.ipv6_key.l4_src_port_1 = 0xFFFF;
            }
        }
    }

    if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
    {
        acl_entry->key.type = CTC_ACL_KEY_IPV4;
        acl_entry->key.u.ipv4_key.key_size = CTC_ACL_KEY_SIZE_DOUBLE;
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
    {
        acl_entry->key.type = CTC_ACL_KEY_IPV6;
    }

    return SAI_STATUS_SUCCESS;
}



static sai_status_t
_ctc_sai_twamp_create_e2iloop_nexthop_for_hw_lookup(ctc_sai_twamp_t *p_twamp_attr, sai_object_id_t switch_id)
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

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));

    /*alloc global iloop port */

    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;   
    port_assign.gchip = gchip;
    ret = ctcs_alloc_internal_port(lchip, &port_assign);   
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate internal iloop port is %d\n", port_assign.inter_port);

    /*config inner l3if */
    
    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id);
    l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
    l3if.gport = port_assign.inter_port;
    ret = ctcs_l3if_create(lchip, l3if_id, &l3if);   
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    l3if_prop = CTC_L3IF_PROP_ROUTE_EN;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_IPV4_UCAST;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_IPV4_MCAST;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_IPV6_UCAST;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_ROUTE_ALL_PKT;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
    l3if_prop = CTC_L3IF_PROP_VRF_EN;
    ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    /* for vpn instance */
    
    if (p_twamp_attr->vrf_oid)
    {
        uint32 vrf_id_tmp = 0;
        ctc_sai_oid_get_vrf_id_u32(p_twamp_attr->vrf_oid, &vrf_id_tmp);

        l3if_prop = CTC_L3IF_PROP_VRF_ID;
        ret = ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, vrf_id_tmp);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
        }
    }
    ret = ctcs_port_set_phy_if_en(lchip, port_assign.inter_port, 1);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate l3if_id  %d\n", l3if_id);
    

    /* add iloop nexthop */
    
    ctc_loopback_nexthop_param_t iloop_nh;
    sal_memset(&iloop_nh, 0, sizeof(ctc_loopback_nexthop_param_t));
    ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid);    
    iloop_nh.lpbk_lport = port_assign.inter_port;
    
    ret = ctcs_nh_add_iloop(lchip, nhid, &iloop_nh);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    p_twamp_attr->l3if_id = l3if_id;
    
    p_twamp_attr->iloop_port = port_assign.inter_port;
    p_twamp_attr->iloop_nexthop = nhid;

    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate iloop nexthop  %d\n", nhid);
    

    /*alloc global eloop port */
    
    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ELOOP;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    port_assign.gchip = gchip;
    port_assign.nhid = p_twamp_attr->iloop_nexthop;   
    ret = ctcs_alloc_internal_port(lchip, &port_assign);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate internal eloop port is %d\n", port_assign.inter_port);

    /* add eloop nexthop */
    
    ctc_misc_nh_param_t nh_param;

    sal_memset(&nh_param, 0, sizeof(ctc_misc_nh_param_t));

    ret = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid);


    if ((p_twamp_attr->encap_type == SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI || p_twamp_attr->encap_type == SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_NNI ) && p_twamp_attr->role == SAI_TWAMP_SESSION_ROLE_REFLECTOR)
    {
        nh_param.type = CTC_MISC_NH_TYPE_OVER_L2;
        nh_param.gport = port_assign.inter_port;  

        uint8 mac_addr_da[6] = {0x00,0x77,0x66,0x55,0x44,0x00};
        uint8 mac_addr_sa[6] = {0x00,0x00,0x00,0x00,0x00,0x01};

        sal_memcpy(&nh_param.misc_param.over_l2edit.mac_da, mac_addr_da, sizeof(sai_mac_t));
        sal_memcpy(&nh_param.misc_param.over_l2edit.mac_sa, mac_addr_sa, sizeof(sai_mac_t));    

        if(SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family)
        {
            nh_param.misc_param.over_l2edit.ether_type = 0x0800;
        }
        else
        {
            nh_param.misc_param.over_l2edit.ether_type = 0x86DD;
        }        
    }
    else 
    {
        nh_param.type = CTC_MISC_NH_TYPE_FLEX_EDIT_HDR;
        nh_param.gport = port_assign.inter_port;
        
        nh_param.misc_param.flex_edit.dscp_select = CTC_NH_DSCP_SELECT_NONE;
    
        nh_param.misc_param.flex_edit.packet_type = CTC_MISC_NH_PACKET_TYPE_UDPORTCP;
        
        nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_UPDATE_UDP_CHKSUM;

        if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family)
        {
            nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_IPV4;         // just for match sdk api (use 6w)
        }
           
        nh_param.misc_param.flex_edit.flag |= CTC_MISC_NH_FLEX_EDIT_REPLACE_IP_HDR;   // just for match sdk api
        
    }

    ret = ctcs_nh_add_misc(lchip, nhid, &nh_param);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    p_twamp_attr->eloop_port = port_assign.inter_port;
    p_twamp_attr->eloop_nexthop = nhid;

    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The allocate eloop nexthop  %d\n", nhid);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_twamp_remove_e2iloop_nexthop_for_hw_lookup(ctc_sai_twamp_t *p_twamp_attr, uint8 lchip)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           ret = 0;
    uint8           gchip = 0;
    uint32          l3if_id = 0;
    ctc_l3if_t      l3if;
    ctc_internal_port_assign_para_t port_assign;

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);

    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    
    /* delete l3if  */
    
    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
    l3if.gport = p_twamp_attr->iloop_port;
    l3if_id = p_twamp_attr->l3if_id;

    ret = ctcs_l3if_destory(lchip, l3if_id, &l3if);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }
 
    ret = ctcs_port_set_phy_if_en(lchip, l3if.gport, 0);    
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }

    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, l3if_id);

    /* delete internel port  */

    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.gchip = gchip;
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;
    port_assign.inter_port = p_twamp_attr->iloop_port;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_free_internal_port(lchip, &port_assign));
    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The dealloc internal port is %d\n", port_assign.inter_port);
    
    sal_memset(&port_assign, 0, sizeof(port_assign));
    port_assign.type = CTC_INTERNAL_PORT_TYPE_ELOOP;
    port_assign.gchip = gchip;
    port_assign.inter_port = p_twamp_attr->eloop_port;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_free_internal_port(lchip, &port_assign));
    CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%%The dealloc internal port is %d\n", port_assign.inter_port);

    /* delete loop nexthop  */  
    
    ret = ctcs_nh_remove_iloop(lchip, p_twamp_attr->iloop_nexthop);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }    
    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_twamp_attr->iloop_nexthop);
        
    ret = ctcs_nh_remove_misc(lchip, p_twamp_attr->eloop_nexthop);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
    }    
    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_twamp_attr->eloop_nexthop);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_twamp_acl_add(sai_object_id_t twamp_session_id, ctc_sai_twamp_t *p_twamp_attr)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           rc = 0;
    uint32_t        entry_id = 0;
    uint8           lchip = 0;
    ctc_acl_entry_t acl_entry;
    twamp_acl_param_t param;
    uint32_t        group_index = 0;
    ctc_acl_field_action_t field_action;

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);

    sal_memset(&field_action, 0, sizeof(field_action));
    sal_memset(&acl_entry, 0, sizeof(acl_entry));
    sal_memset(&param, 0, sizeof(param));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(twamp_session_id, &lchip));

    ctc_sai_twamp_acl_entry_id_alloc(&entry_id);

    p_twamp_attr->loop_acl_entry_id = entry_id;
  
    acl_entry.entry_id = p_twamp_attr->loop_acl_entry_id;
    group_index = p_ctc_sai_twamp[lchip]->twamp_reserved_ingress_acl_group_id; 

    acl_entry.mode = 1;
    acl_entry.key_type = CTC_ACL_KEY_FWD;
    if ((rc = ctcs_acl_add_entry(lchip, group_index, &acl_entry)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "acl add entry failed: %d\n", ctc_get_error_desc(rc));
        return rc;
    }

    status = ctc_sai_twamp_acl_build_param_field(p_twamp_attr, &param);
    sal_memcpy(&acl_entry, &param, sizeof(twamp_acl_param_t));

    if (p_twamp_attr->eloop_nexthop)
    {
        sal_memset(&field_action, 0, sizeof(field_action));

        field_action.type = CTC_ACL_FIELD_ACTION_REDIRECT;
        field_action.data0 = p_twamp_attr->eloop_nexthop;
        rc = ctcs_acl_add_action_field(lchip, entry_id, &field_action);
    }

    if ((rc = ctcs_acl_install_entry(lchip, entry_id)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "acl install entry failed: %d\n", ctc_get_error_desc(rc));
        goto error1;
    }

    return status;

error1:
    rc = ctcs_acl_remove_entry(lchip, entry_id);
    return rc;
}

sai_status_t
ctc_sai_twamp_acl_del(uint32_t entry_id, uint8 lchip)
{
    int32       rc = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;

    // refer to session id, do not alloc
    rc = ctcs_acl_uninstall_entry(lchip, entry_id);
    if (rc)
    {
        return SAI_STATUS_FAILURE;
    }

    // uninstall the entry, when disable the twamp session
    rc = ctcs_acl_remove_entry(lchip, entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    status = ctc_sai_twamp_acl_entry_id_dealloc(entry_id);

    return status;
}

sai_status_t
ctc_sai_twamp_global_acl_add(sai_object_id_t twamp_session_id, ctc_sai_twamp_t *p_twamp_attr)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32           rc = 0;
    uint32_t        entry_id = 0;
    uint32_t        session_id = 0;
    uint8           lchip = 0;
    ctc_acl_entry_t acl_entry;
    ctc_acl_oam_t   twamp_acl_oam;
    twamp_acl_param_t param;
    ctc_acl_field_action_t act_field;
    uint32_t        group_index = 0;

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);

    sal_memset(&acl_entry, 0, sizeof(acl_entry));
    sal_memset(&param, 0, sizeof(param));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(twamp_session_id, &lchip));
    status = ctc_sai_twamp_acl_build_param(p_twamp_attr, &param);
    sal_memcpy(&acl_entry, &param, sizeof(twamp_acl_param_t));

     // refer to session id, do not alloc
    ctc_sai_oid_get_twamp_session_id(twamp_session_id, &session_id);

    ctc_sai_twamp_acl_entry_id_alloc(&entry_id);

    // save the entry id
    p_twamp_attr->oam_acl_entry_id = entry_id;
    
    acl_entry.entry_id = p_twamp_attr->oam_acl_entry_id; 
    group_index = p_ctc_sai_twamp[lchip]->twamp_reserved_ingress_acl_group_id; 

    if ((rc = ctcs_acl_add_entry(lchip, group_index, &acl_entry)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "acl add entry failed: %d\n", ctc_get_error_desc(rc));
        return rc;
    }

    sal_memset(&act_field, 0, sizeof(ctc_acl_field_action_t));
    sal_memset(&twamp_acl_oam, 0, sizeof(ctc_acl_oam_t));

    act_field.type = CTC_ACL_FIELD_ACTION_OAM;
    twamp_acl_oam.oam_type = CTC_ACL_OAM_TYPE_TWAMP;
    twamp_acl_oam.lmep_index = p_twamp_attr->lmep_index;

    if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
    {
        twamp_acl_oam.packet_offset = 42;
        /*
        if ((p_twamp_attr->encap_type == SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI || p_twamp_attr->encap_type == SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_NNI ) && p_twamp_attr->role == SAI_TWAMP_SESSION_ROLE_REFLECTOR)
        {
            twamp_acl_oam.packet_offset = 42 - 14;
        }
        */
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
    {
        twamp_acl_oam.packet_offset = 42 + 20; 
    }

    act_field.ext_data = &twamp_acl_oam;
    rc = ctcs_acl_add_action_field(lchip, entry_id, &act_field);

    if ((rc = ctcs_acl_install_entry(lchip, entry_id)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "acl install entry failed: %d\n", ctc_get_error_desc(rc));
        goto error1;
    }

    return status;

error1:
    rc = ctcs_acl_remove_entry(lchip, acl_entry.entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    return status;
}

sai_status_t
ctc_sai_twamp_global_acl_del(uint32_t entry_id, uint8 lchip)
{
    int32       rc = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;

    rc = ctcs_acl_uninstall_entry(lchip, entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    // uninstall the entry, when disable the twamp session
    rc = ctcs_acl_remove_entry(lchip, entry_id);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    status = ctc_sai_twamp_acl_entry_id_dealloc(entry_id);

    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_twamp_global_acl_init(void)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_acl_group_info_t    acl_group;
    uint32_t    group_id = 0;
    int32       rc = 0;
    uint8       lchip = 0;
    uint32_t    group_index = 0;

    ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, &group_index);
    p_ctc_sai_twamp[lchip]->twamp_reserved_ingress_acl_group_id = group_index;     

    sal_memset(&acl_group, 0, sizeof(acl_group));
    acl_group.priority = TWAMP_PORT_ACL_LOOKUP_PRIORITY;
    acl_group.type     = CTC_ACL_GROUP_TYPE_NONE;
    acl_group.dir      = CTC_INGRESS;
    group_id           = p_ctc_sai_twamp[lchip]->twamp_reserved_ingress_acl_group_id;
    rc = ctcs_acl_create_group(lchip, group_id, &acl_group);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    rc = ctcs_acl_install_group(lchip, group_id, &acl_group);
    if (rc)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(rc));
        status = ctc_sai_mapping_error_ctc(rc);
    }

    return status;
}

sai_status_t
ctc_sai_twamp_acl_entry_id_alloc(uint32_t *acl_entry_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8           lchip = 0;
    uint32_t        entry_index = 0;

    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, &entry_index);
    *acl_entry_id = entry_index; 
    return status;
}

sai_status_t
ctc_sai_twamp_acl_entry_id_dealloc(uint32_t acl_entry_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8           lchip = 0;

    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, acl_entry_id);
    return status;
}



sai_status_t
ctc_sai_twamp_init_session_max(uint8 lchip)
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
_ctc_sai_twamp_build_db(uint8 lchip, sai_object_id_t session_id, ctc_sai_twamp_t** twamp_info)
{
    sai_status_t            status = SAI_STATUS_SUCCESS;
    ctc_sai_twamp_t         *pst_twamp = NULL;

    pst_twamp = ctc_sai_db_get_object_property(lchip, session_id);
    if (NULL != pst_twamp)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }

    pst_twamp = mem_malloc(MEM_OAM_MODULE, sizeof(ctc_sai_twamp_t));
    if (NULL == pst_twamp)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(pst_twamp, 0, sizeof(ctc_sai_twamp_t));
    status = ctc_sai_db_add_object_property(lchip, session_id, pst_twamp);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(pst_twamp);
    }

    *twamp_info = pst_twamp;

    return status;
}

static sai_status_t
_ctc_sai_twamp_remove_db(uint8 lchip, sai_object_id_t session_oid)
{
    sai_status_t            status = SAI_STATUS_SUCCESS;
    ctc_sai_twamp_t         *pst_twamp = NULL;

    pst_twamp = ctc_sai_db_get_object_property(lchip, session_oid);
    if (NULL == pst_twamp)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    status = ctc_sai_db_remove_object_property(lchip, session_oid);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "_ctc_sai_twamp_remove_db error!\n");
        return status;
    }

    mem_free(pst_twamp);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_twamp_mapping_npm_session(ctc_sai_twamp_t *p_twamp_attr, ctc_npm_cfg_t *p_npm_cfg, sai_object_id_t switch_id, uint8 *pkt)
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
 
    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);
    CTC_SAI_PTR_VALID_CHECK(p_npm_cfg);
    CTC_SAI_PTR_VALID_CHECK(pkt);

    sal_memcpy(tmp_pkt, pkt, sizeof(uint8)*103);

    if ((p_twamp_attr->packet_length < TWAMP_PACKET_BASE_LENGTH_IPV4) && SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family )
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        return status;
    }

    if ((p_twamp_attr->packet_length < TWAMP_PACKET_BASE_LENGTH_IPV6) && SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family )
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        return status;
    }
    
    p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_NHID_VALID;  
    p_npm_cfg->nh_id = p_twamp_attr->eloop_nexthop; 

    if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
    {
        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_TS_EN;
        p_npm_cfg->pkt_format.ts_offset = 46;

        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_SEQ_EN;
        p_npm_cfg->pkt_format.seq_num_offset = 42;
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
    {
        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_TS_EN;
        p_npm_cfg->pkt_format.ts_offset = 46 + 20;

        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_SEQ_EN;
        p_npm_cfg->pkt_format.seq_num_offset = 42 + 20;
    }

    p_npm_cfg->pkt_format.ipg = 20;

    if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
    {
        if (p_twamp_attr->udp_src_port)
        {
            udp_src_port = p_twamp_attr->udp_src_port & 0xFFFF;
             *((uint16*)(&tmp_pkt[34])) = sal_htons(udp_src_port);
        }

        if (p_twamp_attr->udp_dst_port)
        {
            udp_dst_port = p_twamp_attr->udp_dst_port & 0xFFFF;
             *((uint16*)(&tmp_pkt[36])) = sal_htons(udp_dst_port);
        }

        // for modify ip header ttl
        tmp_pkt[22] = p_twamp_attr->ttl;

        // for modify ip header tos    
        tmp_pkt[15] = p_twamp_attr->priority << 2;

        // for modify ip header length       
        ip_header_lenth = p_twamp_attr->packet_length - 14 - 4;
        *((uint16*)(&tmp_pkt[16])) = sal_htons(ip_header_lenth);
        
        // for modify udp header length
        udp_header_lenth = p_twamp_attr->packet_length - 34 - 4;
        *((uint16*)(&tmp_pkt[38])) = sal_htons(udp_header_lenth);


        // for modify the packet src ip
        sal_memcpy(&ipv4_addr_tmp, &p_twamp_attr->src_ip.addr.ip4, sizeof(sai_ip4_t));
         *((uint32*)(&tmp_pkt[26])) = ipv4_addr_tmp;

        // for modify the packet dst ip
        ipv4_addr_tmp = 0;
        sal_memcpy(&ipv4_addr_tmp, &p_twamp_attr->dst_ip.addr.ip4, sizeof(sai_ip4_t));
         *((uint32*)(&tmp_pkt[30])) = ipv4_addr_tmp;
            
        // for modify ip header checksum  
        status = _ctc_sai_calculate_ip_header_checsum(4, &checksum, tmp_pkt); 
        pkt_checksum = checksum & 0xFFFF;
        *((uint16*)(&tmp_pkt[24])) = sal_htons(pkt_checksum);        

        // for modify udp header checksum  
        status = _ctc_sai_calculate_udp_header_checsum(4, &checksum, p_twamp_attr->packet_length - 4, 26, 38, 34, 42, tmp_pkt); 
        pkt_checksum = checksum & 0xFFFF;
        *((uint16*)(&tmp_pkt[40])) = sal_htons(pkt_checksum); 
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
    {
        if (p_twamp_attr->udp_src_port)
        {
            udp_src_port = p_twamp_attr->udp_src_port & 0xFFFF;
             *((uint16*)(&tmp_pkt[54])) = sal_htons(udp_src_port);
        }

        if (p_twamp_attr->udp_dst_port)
        {
            udp_dst_port = p_twamp_attr->udp_dst_port & 0xFFFF;
             *((uint16*)(&tmp_pkt[56])) = sal_htons(udp_dst_port);
        }

        // for modify ipv6 header ttl
        tmp_pkt[21] = p_twamp_attr->ttl;
        
        // for modify ipv6 header tos
        tos = p_twamp_attr->priority << 2;
        tmp_pkt[14] = tmp_pkt[14] + (tos >> 4);        
        tmp_pkt[15] = tmp_pkt[15] + (tos << 4); 

        // for modify ip header length       
        ip_header_lenth = p_twamp_attr->packet_length - 54 - 4;
        *((uint16*)(&tmp_pkt[18])) = sal_htons(ip_header_lenth);
        
        // for modify udp header length
        udp_header_lenth = p_twamp_attr->packet_length - 54 - 4;
        *((uint16*)(&tmp_pkt[58])) = sal_htons(udp_header_lenth);

        // for modify the packet src ip 
        sal_memcpy(ipv6_sa_addr, &p_twamp_attr->src_ip.addr.ip6, sizeof(ipv6_addr_t));
        *((uint32*)(&tmp_pkt[22])) = ipv6_sa_addr[0];
        *((uint32*)(&tmp_pkt[26])) = ipv6_sa_addr[1];
        *((uint32*)(&tmp_pkt[30])) = ipv6_sa_addr[2];
        *((uint32*)(&tmp_pkt[34])) = ipv6_sa_addr[3]; 

        // for modify the packet dst ip  
        sal_memcpy(ipv6_da_addr, &p_twamp_attr->dst_ip.addr.ip6, sizeof(ipv6_addr_t));
        *((uint32*)(&tmp_pkt[38])) = ipv6_da_addr[0];
        *((uint32*)(&tmp_pkt[42])) = ipv6_da_addr[1];
        *((uint32*)(&tmp_pkt[46])) = ipv6_da_addr[2];
        *((uint32*)(&tmp_pkt[50])) = ipv6_da_addr[3]; 

        // for modify udp header checksum  
        status = _ctc_sai_calculate_udp_header_checsum(6, &checksum, p_twamp_attr->packet_length - 4, 22, 58, 54, 62, tmp_pkt); 
        pkt_checksum = checksum & 0xFFFF;
        *((uint16*)(&tmp_pkt[60])) = sal_htons(pkt_checksum); 
    }
                
    // for init the twamp test packet
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV4 == p_twamp_attr->dst_ip.addr_family)
    {
        status = _ctc_sai_twamp_test_ipv4_packet(p_twamp_attr, p_npm_cfg, tmp_pkt);
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->src_ip.addr_family || SAI_IP_ADDR_FAMILY_IPV6 == p_twamp_attr->dst_ip.addr_family)
    {
        status = _ctc_sai_twamp_test_ipv6_packet(p_twamp_attr, p_npm_cfg, tmp_pkt);
    }

    p_npm_cfg->rate = p_twamp_attr->tx_rate;

    if (SAI_TWAMP_PKT_TX_MODE_CONTINUOUS == p_twamp_attr->pkt_tx_mode)
    {
        p_npm_cfg->tx_mode = CTC_NPM_TX_MODE_CONTINUOUS;
        if (p_twamp_attr->pkt_duration)
        {
            p_npm_cfg->timeout = p_twamp_attr->pkt_duration;
        }
        else
        {
            p_npm_cfg->timeout = 0;
        }        
    }
    else if (SAI_TWAMP_PKT_TX_MODE_PACKET_NUM == p_twamp_attr->pkt_tx_mode)
    {
        p_npm_cfg->tx_mode = CTC_NPM_TX_MODE_PACKET_NUM;
        p_npm_cfg->packet_num = p_twamp_attr->pkt_cnt;
    }
    else if (SAI_TWAMP_PKT_TX_MODE_PERIOD == p_twamp_attr->pkt_tx_mode)
    {
        p_npm_cfg->tx_mode = CTC_NPM_TX_MODE_PERIOD;
        p_npm_cfg->tx_period = p_twamp_attr->period;
    }
    else
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        return status;           
    }

    if (p_twamp_attr->packet_length)
    {
        p_npm_cfg->pkt_format.frame_size_mode = 0;  //fix frame size
        p_npm_cfg->pkt_format.frame_size = p_twamp_attr->packet_length;

        // default to use the pattern 
        p_npm_cfg->pkt_format.pattern_type = CTC_NPM_PATTERN_TYPE_REPEAT;
        p_npm_cfg->pkt_format.repeat_pattern = 0x00;
    }

    // twamp sender need to record the stats
    p_npm_cfg->dm_stats_mode = 0; // default is two way delay stats

    // support the ntp timestamp format by default
    if (p_twamp_attr->timestamp_format == SAI_TWAMP_TIMESTAMP_FORMAT_NTP)
    {
        p_npm_cfg->flag |= CTC_NPM_CFG_FLAG_NTP_TS; 
    }

    return status;
}

static sai_status_t
ctc_sai_twamp_parser_session_attr(uint32_t attr_count, const sai_attribute_t *attr_list, ctc_sai_twamp_t *p_twamp_attr)
{
    sai_status_t            status = SAI_STATUS_SUCCESS;
    uint32_t                index = 0;
    const sai_attribute_value_t     *attr_value = NULL;
    sai_object_id_t   tmp_port_id = 0;
    ctc_object_id_t tmp_ctc_oid;
    uint32 i = 0;

    sal_memset(&tmp_port_id, 0, sizeof(sai_object_id_t));
    sal_memset(&tmp_ctc_oid, 0, sizeof(ctc_object_id_t));  
    

    CTC_SAI_PTR_VALID_CHECK(p_twamp_attr);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_SESSION_ROLE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->role = attr_value->s32;
    }    
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    } 

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->encap_type = attr_value->s32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    if ((p_twamp_attr->encap_type == SAI_TWAMP_ENCAPSULATION_TYPE_IP) || (p_twamp_attr->encap_type == SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI))
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TWAMP_PORT, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_twamp_attr->port_id = attr_value->oid;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }    
    }
    else
    {
        // Do not care twamp port
    }
    
 
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->receive_port_count = attr_value->objlist.count;

        if ( p_twamp_attr->receive_port_count == 0 )
        {
            CTC_SAI_LOG_ERROR(SAI_API_NPM, "receive port list can not be empty");
            return  SAI_STATUS_INVALID_PARAMETER;
        }
        
        for (i = 0; i < p_twamp_attr->receive_port_count; i++)
        {
            tmp_port_id = attr_value->objlist.list[i];
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, tmp_port_id, &tmp_ctc_oid);
            CTC_BMP_SET(p_twamp_attr->receive_port_bits, CTC_MAP_GPORT_TO_LPORT(tmp_ctc_oid.value));   
        }        
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_NPM, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    } 

    


    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->udp_src_port = attr_value->u32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }  

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->udp_dst_port = attr_value->u32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }  

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_SRC_IP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&p_twamp_attr->src_ip, &attr_value->ipaddr, sizeof(p_twamp_attr->src_ip));
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }  

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_DST_IP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&p_twamp_attr->dst_ip, &attr_value->ipaddr, sizeof(p_twamp_attr->dst_ip));
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TC, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->priority = attr_value->u8;
    }
    else
    {
        p_twamp_attr->priority = 0;
    } 

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->vrf_oid = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->hw_lookup = attr_value->booldata;
    }    
    else
    {
        p_twamp_attr->hw_lookup = true;
    }

    if (SAI_TWAMP_SESSION_ROLE_SENDER == p_twamp_attr->role)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TTL, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_twamp_attr->ttl = attr_value->u8;
        }    
        else
        {
            p_twamp_attr->ttl = 255;
        } 
        

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            p_twamp_attr->trans_enable = attr_value->booldata;
        }
        else
        {
            p_twamp_attr->trans_enable = false;
        }


        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_twamp_attr->packet_length = attr_value->u32;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TX_RATE, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_twamp_attr->tx_rate = attr_value->u32;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }     
        
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TWAMP_PKT_TX_MODE, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_twamp_attr->pkt_tx_mode = attr_value->s32;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
            return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        } 

        if(p_twamp_attr->pkt_tx_mode == SAI_TWAMP_PKT_TX_MODE_CONTINUOUS)
        {
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION, &attr_value, &index);
            if(SAI_STATUS_SUCCESS == status)
            {
                p_twamp_attr->pkt_duration = attr_value->u32;
            }
            else
            {
                CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
                return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }         
        }
        else if(p_twamp_attr->pkt_tx_mode == SAI_TWAMP_PKT_TX_MODE_PACKET_NUM)
        {   
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT, &attr_value, &index);
            if(SAI_STATUS_SUCCESS == status)
            {
                p_twamp_attr->pkt_cnt = attr_value->u32;
            }
            else
            {
                CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
                return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }                 
        }    
        else if(p_twamp_attr->pkt_tx_mode == SAI_TWAMP_PKT_TX_MODE_PERIOD)
        {
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD, &attr_value, &index);
            if(SAI_STATUS_SUCCESS == status)
            {
                p_twamp_attr->period = attr_value->u32;
            }
            else
            {
                CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
                return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }         
        }
        else 
        {
            return  SAI_STATUS_INVALID_PARAMETER;        
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_AUTH_MODE, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->auth_mode = attr_value->s32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    } 

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->user_nh_id = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TWAMP_MODE, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->session_mode = attr_value->s32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }   

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TWAMP_SESSION_ATTR_TIMESTAMP_FORMAT, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        p_twamp_attr->timestamp_format = attr_value->s32;
    }
    else
    {
        p_twamp_attr->timestamp_format = SAI_TWAMP_TIMESTAMP_FORMAT_NTP;
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_twamp_wb_sync_cb1(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_status_t ret = 0;
    ctc_wb_data_t wb_data;
    ctc_sai_twamp_master_wb_t twamp_master_wb;
    
    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    
    CTC_WB_INIT_DATA_T((&wb_data),ctc_sai_twamp_master_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_TWAMP_GLOBAL);
    twamp_master_wb.lchip = lchip;
    twamp_master_wb.twamp_reserved_ingress_acl_group_id = p_ctc_sai_twamp[lchip]->twamp_reserved_ingress_acl_group_id;

    sal_memcpy((uint8*)wb_data.buffer, (uint8*)&twamp_master_wb, sizeof(ctc_sai_twamp_master_wb_t));

    wb_data.valid_cnt = 1;
    CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);

done:
out:
    CTC_WB_FREE_BUFFER(wb_data.buffer);
    return status;
}


static sai_status_t
_ctc_sai_twamp_wb_reload_cb1(uint8 lchip)
{
    sai_status_t ret = 0;
    ctc_wb_query_t wb_query;
    ctc_sai_twamp_master_wb_t twamp_master_wb;
    uint32 entry_cnt = 0;

    sal_memset(&twamp_master_wb, 0, sizeof(ctc_sai_twamp_master_wb_t));

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    
    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_twamp_master_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_TWAMP_GLOBAL);
    CTC_SAI_CTC_ERROR_GOTO(ctc_wb_query_entry(&wb_query), ret, out);

    if (wb_query.valid_cnt != 0)
    {
        sal_memcpy((uint8*)&twamp_master_wb, (uint8*)(wb_query.buffer)+entry_cnt*(wb_query.key_len + wb_query.data_len),
            (wb_query.key_len+wb_query.data_len));

        p_ctc_sai_twamp[lchip]->twamp_reserved_ingress_acl_group_id = twamp_master_wb.twamp_reserved_ingress_acl_group_id;     
    }


    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, p_ctc_sai_twamp[lchip]->twamp_reserved_ingress_acl_group_id));

out:    
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }
            
    return SAI_STATUS_SUCCESS;
}



static sai_status_t
_ctc_sai_twamp_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_sai_twamp_t *p_db_twamp = (ctc_sai_twamp_t*)data;
    sai_object_id_t twamp_sai_oid = *(sai_object_id_t*)key;
    ctc_object_id_t twamp_ctc_oid;
    
    sal_memset(&twamp_ctc_oid, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TWAMP_SESSION, twamp_sai_oid, &twamp_ctc_oid));

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_TWAMP, twamp_ctc_oid.value));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_L3IF, p_db_twamp->l3if_id));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_twamp->iloop_nexthop));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_twamp->eloop_nexthop));    
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, p_db_twamp->oam_acl_entry_id));

    if (SAI_TWAMP_SESSION_ROLE_REFLECTOR == p_db_twamp->role)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_L3IF, p_db_twamp->oam_l3if_id));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_twamp->oam_iloop_nh_id));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_db_twamp->oam_eloop_nh_id));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, p_db_twamp->loop_acl_entry_id));        
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_twamp_unsupport_attr_check(ctc_sai_twamp_t *p_twamp_attr, uint8 lchip)

{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 chip_type = CTC_CHIP_TSINGMA;

    chip_type = ctcs_get_chip_type(lchip);
    if(CTC_CHIP_TSINGMA == chip_type)
    {
        if (TRUE != p_twamp_attr->hw_lookup)
        {
            status = SAI_STATUS_NOT_SUPPORTED;
            return status;
        }

        if (SAI_TWAMP_MODE_FULL != p_twamp_attr->session_mode)
        {
            status = SAI_STATUS_NOT_SUPPORTED;
            return status;
        }

        if (p_twamp_attr->user_nh_id)
        {
            status = SAI_STATUS_NOT_SUPPORTED;
            return status;
        }

        if (SAI_TWAMP_SESSION_AUTH_MODE_UNAUTHENTICATED != p_twamp_attr->auth_mode)
        {
            status = SAI_STATUS_NOT_SUPPORTED;
            return status;
        }    

        if ( SAI_TWAMP_TIMESTAMP_FORMAT_NTP != p_twamp_attr->timestamp_format)
        {
            status = SAI_STATUS_NOT_SUPPORTED;
            return status;
        }
    }

    return status;
}


#define ________SAI_API________

static sai_status_t
ctc_sai_twamp_create_twamp_session(sai_object_id_t *twamp_session_id,  sai_object_id_t switch_id, 
                        uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t            status = SAI_STATUS_SUCCESS;
    int32                   ret = 0;
    uint8                   lchip = 0;
    uint32_t                twamp_id = 0;
    sai_object_id_t         twamp_tmp_oid = 0;
    ctc_npm_cfg_t           npm_cfg;
    ctc_sai_twamp_t         twamp_attr;
    ctc_sai_twamp_t         *p_twamp_info = NULL;
    uint8_t                 session_id = 0;
    ctc_acl_property_t acl_prop;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;

    

    CTC_SAI_PTR_VALID_CHECK(twamp_session_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    ctc_sai_oid_get_lchip(switch_id, &lchip);

    ctcs_get_gchip_id(lchip, &gchip);
    
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_TWAMP, &twamp_id));
    twamp_tmp_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TWAMP_SESSION, lchip, 0, 0, twamp_id);

    sal_memset(&twamp_attr, 0, sizeof(ctc_sai_twamp_t));
    status = ctc_sai_twamp_parser_session_attr(attr_count, attr_list, &twamp_attr);
    if (CTC_SAI_ERROR(status))
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error1;
    }

    status = _ctc_sai_twamp_unsupport_attr_check(&twamp_attr, lchip);
    if (CTC_SAI_ERROR(status))
    {
        status = SAI_STATUS_NOT_SUPPORTED;
        goto error1;
    }

    if(twamp_oam_maid_ref_cnt == 0)
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_create_oam_maid(lchip),status, error1);
    }
    
    CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_create_oam_mep_index(&twamp_attr, switch_id, twamp_id),status, error2);
    CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_update_oam_mep(&twamp_attr, twamp_id, lchip),status, error3);

    if (TRUE == twamp_attr.hw_lookup)
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_create_e2iloop_nexthop_for_hw_lookup(&twamp_attr, switch_id),status, error3);
    }

    if (SAI_TWAMP_SESSION_ROLE_SENDER == twamp_attr.role)
    {

        // for sender receive port enable acl match to oam engine
        sal_memset(&npm_cfg, 0, sizeof(npm_cfg));
        sal_memset(&acl_prop, 0, sizeof(acl_prop));
        acl_prop.acl_en = 1;
        acl_prop.acl_priority = TWAMP_PORT_ACL_LOOKUP_PRIORITY;
        acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_L2_L3;

        if( twamp_attr.receive_port_count )
        {
        
            for (bit_cnt = 0; bit_cnt < sizeof(twamp_attr.receive_port_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(twamp_attr.receive_port_bits, bit_cnt))
                {
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &acl_prop),status, error4);    
                }
            }
        }


        twamp_attr.is_loop_swap_ip = 1;
        ret = ctc_sai_twamp_global_acl_add(twamp_tmp_oid, &twamp_attr);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error5;
        }


        if (SAI_IP_ADDR_FAMILY_IPV4 == twamp_attr.src_ip.addr_family) 
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_mapping_npm_session(&twamp_attr, &npm_cfg, switch_id, twamp_pkt_ipv4_header),status, error6);
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == twamp_attr.src_ip.addr_family) 
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_mapping_npm_session(&twamp_attr, &npm_cfg, switch_id, twamp_pkt_ipv6_header),status, error6);
        }

        session_id = twamp_id & 0xFF;
        npm_cfg.session_id = session_id;
        ret = ctcs_npm_set_config(lchip, &npm_cfg);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error6;
        }

        // just for temp test
        if (1 == SDK_WORK_PLATFORM)
        {
            ctc_sai_twamp_write_hardware_table(lchip); 
        }


        if(twamp_attr.trans_enable)
        {
            ret = ctcs_npm_set_transmit_en(lchip, session_id, twamp_attr.trans_enable);
            if (ret)
            {
                CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
                status = ctc_sai_mapping_error_ctc(ret);
                goto error6;
            }
        }
    }
    else if (SAI_TWAMP_SESSION_ROLE_REFLECTOR == twamp_attr.role)
    {
        sal_memset(&acl_prop, 0, sizeof(acl_prop));
        acl_prop.acl_en = 1;
        acl_prop.acl_priority = TWAMP_PORT_ACL_LOOKUP_PRIORITY;
        acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_FORWARD;

        if( twamp_attr.receive_port_count )
        {
        
            for (bit_cnt = 0; bit_cnt < sizeof(twamp_attr.receive_port_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(twamp_attr.receive_port_bits, bit_cnt))
                {
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &acl_prop),status, error4);    
                }
            }
        }


        sal_memset(&acl_prop, 0, sizeof(acl_prop));                    
        acl_prop.acl_en = 1;
        acl_prop.acl_priority = TWAMP_PORT_ACL_LOOKUP_PRIORITY;
        acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_L2_L3;

        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, twamp_attr.iloop_port, &acl_prop),status, error5);

        //twamp_attr.is_loop_swap_ip = 1;

        ret = ctc_sai_twamp_global_acl_add(twamp_tmp_oid, &twamp_attr);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error5;
        }

        //twamp_attr.is_loop_swap_ip = 0;

        ret = ctc_sai_twamp_acl_add(twamp_tmp_oid, &twamp_attr);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error6;
        }
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_build_db(lchip, twamp_tmp_oid, &p_twamp_info), status, error7);

    sal_memcpy(p_twamp_info, &twamp_attr, sizeof(ctc_sai_twamp_t));

    *twamp_session_id = twamp_tmp_oid;

    twamp_oam_maid_ref_cnt ++;

    return status;

error7:
    if (SAI_TWAMP_SESSION_ROLE_REFLECTOR == p_twamp_info->role)
    {
        ctc_sai_twamp_acl_del(p_twamp_info->loop_acl_entry_id, lchip);
    }
error6:
    ctc_sai_twamp_global_acl_del(twamp_attr.oam_acl_entry_id, lchip);    
error5:     
    acl_prop.acl_en = 0;
    acl_prop.acl_priority = TWAMP_PORT_ACL_LOOKUP_PRIORITY; 
    if( twamp_attr.receive_port_count )
    {
    
        for (bit_cnt = 0; bit_cnt < sizeof(twamp_attr.receive_port_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(twamp_attr.receive_port_bits, bit_cnt))
            {
               ctcs_port_set_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &acl_prop);
            }
        }
    }            
    ctcs_port_set_acl_property(lchip, twamp_attr.iloop_port, &acl_prop);     
error4:
    _ctc_sai_twamp_remove_e2iloop_nexthop_for_hw_lookup(&twamp_attr, lchip);    
error3:
    _ctc_sai_twamp_remove_oam_mep_index(&twamp_attr, twamp_tmp_oid);    
error2:    
    if(twamp_oam_maid_ref_cnt == 0)
    {    
        _ctc_sai_twamp_remove_oam_maid(lchip);
    }    
error1:
    ctc_sai_db_free_id(lchip, SAI_OBJECT_TYPE_TWAMP_SESSION, twamp_id);
    
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "Failed to create twamp session entry:%d\n", status);
    }

    return status;
}

static sai_status_t
ctc_sai_twamp_remove_twamp_session(sai_object_id_t twamp_session_oid)
{
    ctc_sai_twamp_t     *p_twamp_info = NULL;
    sai_status_t        status = SAI_STATUS_SUCCESS;
    uint8               lchip = 0;
    uint32              session_id = 0;
    uint8               session_id_tmp = 0;
    int32               ret = 0;
    ctc_acl_property_t acl_prop;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;


    

    CTC_SAI_LOG_ENTER(SAI_API_TWAMP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(twamp_session_oid, &lchip));

    ctcs_get_gchip_id(lchip, &gchip);
    
    p_twamp_info = ctc_sai_db_get_object_property(lchip, twamp_session_oid);
    if (NULL == p_twamp_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error1; 
    }


    status = ctc_sai_oid_get_twamp_session_id(twamp_session_oid, &session_id);
    session_id_tmp = session_id & 0xFF;
    
    if (SAI_TWAMP_SESSION_ROLE_SENDER == p_twamp_info->role)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_npm_set_transmit_en(lchip, session_id_tmp, 0), status, error1);

        sal_memset(&acl_prop, 0, sizeof(acl_prop));
        acl_prop.acl_en = 0;
        acl_prop.acl_priority = TWAMP_PORT_ACL_LOOKUP_PRIORITY;

        if( p_twamp_info->receive_port_count )
        {
        
            for (bit_cnt = 0; bit_cnt < sizeof(p_twamp_info->receive_port_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_twamp_info->receive_port_bits, bit_cnt))
                {
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &acl_prop),status, error1);    
                }
            }
        }
        

        ret = ctc_sai_twamp_global_acl_del(p_twamp_info->oam_acl_entry_id, lchip);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error1; 
        }
    }
    else if (SAI_TWAMP_SESSION_ROLE_REFLECTOR == p_twamp_info->role)
    {        
        sal_memset(&acl_prop, 0, sizeof(acl_prop));
        acl_prop.acl_en = 0;
        acl_prop.acl_priority = TWAMP_PORT_ACL_LOOKUP_PRIORITY;
        
        if( p_twamp_info->receive_port_count )
        {
        
            for (bit_cnt = 0; bit_cnt < sizeof(p_twamp_info->receive_port_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_twamp_info->receive_port_bits, bit_cnt))
                {
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &acl_prop),status, error1);    
                }
            }
        }


        ret = ctc_sai_twamp_acl_del(p_twamp_info->loop_acl_entry_id, lchip);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error1;
        }

        sal_memset(&acl_prop, 0, sizeof(acl_prop));
        acl_prop.acl_en = 0;
        acl_prop.acl_priority = TWAMP_PORT_ACL_LOOKUP_PRIORITY;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_acl_property(lchip, p_twamp_info->iloop_port, &acl_prop), status, error1);

        ret = ctc_sai_twamp_global_acl_del(p_twamp_info->oam_acl_entry_id, lchip);
        if (ret)
        {
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
            status = ctc_sai_mapping_error_ctc(ret);
            goto error1;
        }
    }

    ret = ctcs_npm_clear_stats(lchip, session_id_tmp);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
        goto error1; 
    }

    if (TRUE == p_twamp_info->hw_lookup)
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_remove_e2iloop_nexthop_for_hw_lookup(p_twamp_info, lchip), status, error1);
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_remove_oam_mep_index(p_twamp_info, twamp_session_oid),status, error1);

    if(twamp_oam_maid_ref_cnt == 1)
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_remove_oam_maid(lchip),status, error1);
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_twamp_remove_db(lchip, twamp_session_oid),status, error1);
    
    status = ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_TWAMP, session_id);

    twamp_oam_maid_ref_cnt --;

    return status;

error1:    
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "Failed to remove twamp session entry:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_twamp_get_twamp_session_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t        status = SAI_STATUS_SUCCESS;
    uint8               lchip = 0;
    ctc_sai_twamp_t     *p_twamp_info = NULL;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;
    uint32 port_num = 0;
    sai_object_id_t* receive_ports;
    

    CTC_SAI_LOG_ENTER(SAI_API_TWAMP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    ctcs_get_gchip_id(lchip, &gchip);
    
    p_twamp_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_twamp_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_TWAMP_SESSION_ATTR_TWAMP_PORT:
            attr->value.oid = p_twamp_info->port_id;
            break;

        case SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT:
            receive_ports =  mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*p_twamp_info->receive_port_count);
            if (NULL == receive_ports)
            {
                return SAI_STATUS_NO_MEMORY;
            }
            sal_memset(receive_ports, 0, sizeof(sai_object_id_t)*p_twamp_info->receive_port_count);

            
            for (bit_cnt = 0; bit_cnt < sizeof(p_twamp_info->receive_port_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_twamp_info->receive_port_bits, bit_cnt))
                {
                    receive_ports[port_num] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt));
                    port_num++;
                }
            }
            
            status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), receive_ports, port_num, &attr->value.objlist);
            mem_free(receive_ports);
            
            break;

        case SAI_TWAMP_SESSION_ATTR_SESSION_ROLE:
            attr->value.s32 = p_twamp_info->role;
            break;

        case SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT:
            attr->value.u32 = p_twamp_info->udp_src_port;
            break;

        case SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT:
            attr->value.u32 = p_twamp_info->udp_dst_port;
            break;

        case SAI_TWAMP_SESSION_ATTR_SRC_IP:
            sal_memcpy(&attr->value.ipaddr, &p_twamp_info->src_ip, sizeof(sai_ip_address_t));
            break;

        case SAI_TWAMP_SESSION_ATTR_DST_IP:
            sal_memcpy(&attr->value.ipaddr, &p_twamp_info->dst_ip, sizeof(sai_ip_address_t));
            break;

        case SAI_TWAMP_SESSION_ATTR_TC:
            attr->value.u8 = p_twamp_info->priority;
            break;

        case SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER:
            attr->value.oid = p_twamp_info->vrf_oid;
            break;

        case SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE:
            attr->value.s32 = p_twamp_info->encap_type;
            break;

        case SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
            attr->value.booldata = p_twamp_info->trans_enable;
            break;

        case SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID:
            attr->value.booldata = p_twamp_info->hw_lookup;
            break;

        case SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH:
            attr->value.u32 = p_twamp_info->packet_length;
            break;

        case SAI_TWAMP_SESSION_ATTR_AUTH_MODE:
            attr->value.s32 = p_twamp_info->auth_mode;
            break;

        case SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID:
            attr->value.oid = p_twamp_info->user_nh_id;
            break;

        case SAI_TWAMP_SESSION_ATTR_TWAMP_PKT_TX_MODE:
            attr->value.s32 = p_twamp_info->pkt_tx_mode;
            break;

        case SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD:
            attr->value.u32 = p_twamp_info->period;
            break;

        case SAI_TWAMP_SESSION_ATTR_TX_RATE:
            attr->value.u32 = p_twamp_info->tx_rate;
            break;

        case SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT:
            attr->value.u32 = p_twamp_info->pkt_cnt;
            break;

        case SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION:
            attr->value.u32 = p_twamp_info->pkt_duration;
            break;

        case SAI_TWAMP_SESSION_ATTR_TWAMP_MODE:
            attr->value.s32 = p_twamp_info->session_mode;
            break;

        case SAI_TWAMP_SESSION_ATTR_TIMESTAMP_FORMAT:
            attr->value.s32 = p_twamp_info->timestamp_format;
            break;
        
        default:
            CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "Get twamp attribute not implement\n");
            return  SAI_STATUS_NOT_IMPLEMENTED + attr_idx;
    }

    return status;
}

static sai_status_t 
ctc_sai_twamp_set_twamp_session_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    sai_status_t        status = SAI_STATUS_SUCCESS;
    ctc_sai_twamp_t     *p_twamp_info = NULL;
    uint8               lchip = 0;
    uint8               session_id_tmp = 0;
    uint32              session_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_TWAMP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_twamp_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);

    if (NULL == p_twamp_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (SAI_TWAMP_SESSION_ROLE_SENDER != p_twamp_info->role)
    {
        return  SAI_STATUS_INVALID_PARAMETER;
    }

    if (SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT != attr->id)
    {
        return  SAI_STATUS_INVALID_PARAMETER;
    }
    else
    {
        if (attr->value.booldata == p_twamp_info->trans_enable)
        {
            return  SAI_STATUS_SUCCESS;
        }
    }

    status = ctc_sai_oid_get_twamp_session_id(key->key.object_id, &session_id);
    session_id_tmp = session_id & 0xFF;

    CTC_SAI_CTC_ERROR_RETURN(ctcs_npm_set_transmit_en(lchip, session_id_tmp, attr->value.booldata));

    p_twamp_info->trans_enable = attr->value.booldata;

    return SAI_STATUS_SUCCESS;
}

static ctc_sai_attr_fn_entry_t  twamp_attr_fn_entries[] =
{
    { SAI_TWAMP_SESSION_ATTR_TWAMP_PORT,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    }, 
    { SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr 
    },    
    { SAI_TWAMP_SESSION_ATTR_SESSION_ROLE,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr 
    },
    { SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_SRC_IP,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_DST_IP,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_TC,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_AUTH_MODE,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_TWAMP_PKT_TX_MODE,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_TX_RATE,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_TWAMP_MODE,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    },
    { SAI_TWAMP_SESSION_ATTR_TIMESTAMP_FORMAT,
      ctc_sai_twamp_get_twamp_session_attr,
      ctc_sai_twamp_set_twamp_session_attr
    }    
};

sai_status_t
ctc_sai_twamp_set_twamp_attr(sai_object_id_t twamp_session_id, const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = twamp_session_id };
    uint8           lchip = 0;
    char            key_str[MAX_KEY_STR_LEN];
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_TWAMP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(twamp_session_id, &lchip));
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_TWAMP_SESSION, twamp_attr_fn_entries, attr);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "Failed to set stp attr:%d, status:%d\n", attr->id,status);
    }

    return status;
}

sai_status_t
ctc_sai_twamp_get_twamp_attr(sai_object_id_t twamp_session_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_object_key_t key = { .key.object_id = twamp_session_id};
    sai_status_t    status = SAI_STATUS_SUCCESS;
    char            key_str[MAX_KEY_STR_LEN];
    uint32_t        loop_index = 0;
    uint8           lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_TWAMP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(twamp_session_id, &lchip));

    while (loop_index < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str, SAI_OBJECT_TYPE_TWAMP_SESSION,
                                    loop_index, twamp_attr_fn_entries, &attr_list[loop_index]), status, out);
        loop_index ++;
    }

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "Failed to get twamp attr. status:%d, attr_id:%d\n", status, attr_list[loop_index].id);
    }

    return status;
}

int32
ctc_sai_twamp_time_delay_transfer(uint64 time, uint32* time_s, uint32* time_ms, uint32* time_us, uint32* time_ns)
{
    *time_s = time / 1000000000;
    *time_ms = (time - ((*time_s) * 1000000000)) / 1000000;
    *time_us = (time - ((*time_s) * 1000000000) - ((*time_ms) * 1000000)) / 1000;
    *time_ns = time - (*time_s) * 1000000000 - (*time_ms) * 1000000 - (*time_us) * 1000;

    return 0;
}

sai_status_t
ctc_sai_twamp_get_twamp_session_stats(sai_object_id_t twamp_session_id, 
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
    ctc_sai_twamp_t     *p_twamp_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_TWAMP);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);

    sal_memset(&npm_stats, 0, sizeof(ctc_npm_stats_t));
    
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(twamp_session_id, &lchip));
    p_twamp_info = ctc_sai_db_get_object_property(lchip, twamp_session_id);
    if (NULL == p_twamp_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(p_twamp_info->role != SAI_TWAMP_SESSION_ROLE_SENDER)
    {
        return SAI_STATUS_INVALID_PARAMETER;        
    }


    status = ctc_sai_oid_get_twamp_session_id(twamp_session_id, &tmp_session_id);
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
            case SAI_TWAMP_SESSION_STATS_RX_PACKETS:
                counters[stats_index] = npm_stats.rx_pkts;
                break;

            case SAI_TWAMP_SESSION_STATS_RX_BYTE:
                counters[stats_index] = npm_stats.rx_bytes;
                break;

            case SAI_TWAMP_SESSION_STATS_TX_PACKETS:
                counters[stats_index] = npm_stats.tx_pkts;
                break;

            case SAI_TWAMP_SESSION_STATS_TX_BYTE:
                counters[stats_index] = npm_stats.tx_bytes;
                break;

            case SAI_TWAMP_SESSION_STATS_DROP_PACKETS:
                counters[stats_index] = fl;
                break;

            case SAI_TWAMP_SESSION_STATS_MAX_LATENCY:
                counters[stats_index] = npm_stats.max_delay;
                break;

            case SAI_TWAMP_SESSION_STATS_MIN_LATENCY:
                counters[stats_index] = npm_stats.min_delay;
                break;

            case SAI_TWAMP_SESSION_STATS_AVG_LATENCY:
                counters[stats_index] = npm_stats.tx_pkts ? (npm_stats.total_delay / npm_stats.tx_pkts) : 0;
                break;

            case SAI_TWAMP_SESSION_STATS_MAX_JITTER:
                counters[stats_index] = npm_stats.max_jitter;
                break;

            case SAI_TWAMP_SESSION_STATS_MIN_JITTER:
                counters[stats_index] = npm_stats.min_jitter;
                break;
            case SAI_TWAMP_SESSION_STATS_AVG_JITTER:
                counters[stats_index] = npm_stats.tx_pkts ? (npm_stats.total_jitter / npm_stats.tx_pkts) : 0;
                break;

            case SAI_TWAMP_SESSION_STATS_FIRST_TS:
                counters[stats_index] = npm_stats.first_ts;
                break;

            case SAI_TWAMP_SESSION_STATS_LAST_TS:
                counters[stats_index] = npm_stats.last_ts;
                break;

            case SAI_TWAMP_SESSION_STATS_DURATION_TS:
                counters[stats_index] = duration_ts;
                break;

            default:
                CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "Get twamp stats not implement\n");
                return  SAI_STATUS_NOT_IMPLEMENTED;
        }
    }    

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_twamp_clear_twamp_session_stats( sai_object_id_t twamp_session_oid, uint32_t stats_count, const sai_stat_id_t *counter_ids)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    int32       ret = 0;
    uint8       lchip = 0;
    uint8       session_id = 0;
    uint32      session_id_tmp = 0;
    ctc_sai_twamp_t     *p_twamp_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_TWAMP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(twamp_session_oid, &lchip));
    p_twamp_info = ctc_sai_db_get_object_property(lchip, twamp_session_oid);
    if (NULL == p_twamp_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(p_twamp_info->role != SAI_TWAMP_SESSION_ROLE_SENDER)
    {
        return SAI_STATUS_INVALID_PARAMETER;        
    }

    status = ctc_sai_oid_get_twamp_session_id(twamp_session_oid, &session_id_tmp);
    session_id = session_id_tmp & 0xFF;
    
    ret = ctcs_npm_clear_stats(lchip, session_id);
    if (ret)
    {
        CTC_SAI_LOG_ERROR(SAI_API_TWAMP, "%% %s \n", ctc_get_error_desc(ret));
        status = ctc_sai_mapping_error_ctc(ret);
        return status;
    }

    return status;
}


const sai_twamp_api_t ctc_sai_twamp_api = {
    ctc_sai_twamp_create_twamp_session,
    ctc_sai_twamp_remove_twamp_session,
    ctc_sai_twamp_set_twamp_attr,
    ctc_sai_twamp_get_twamp_attr,
    ctc_sai_twamp_get_twamp_session_stats,
    NULL,
    ctc_sai_twamp_clear_twamp_session_stats,
};

sai_status_t
ctc_sai_twamp_api_init()
{
    ctc_sai_register_module_api(SAI_API_TWAMP, (void*)&ctc_sai_twamp_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_twamp_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_TWAMP;
    wb_info.data_len = sizeof(ctc_sai_twamp_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_twamp_wb_reload_cb;

    wb_info.wb_sync_cb1 = _ctc_sai_twamp_wb_sync_cb1;
    wb_info.wb_reload_cb1 = _ctc_sai_twamp_wb_reload_cb1;
    

    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TWAMP_SESSION, (void*)(&wb_info));

    if(NULL != p_ctc_sai_twamp[lchip])
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    p_ctc_sai_twamp[lchip] = mem_malloc(MEM_OAM_MODULE, sizeof(ctc_sai_twamp_master_t));
    if (NULL == p_ctc_sai_twamp[lchip])
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_ctc_sai_twamp[lchip], 0, sizeof(ctc_sai_twamp_master_t));


    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    ctc_sai_twamp_global_acl_init();
    ctc_sai_twamp_init_session_max(lchip);
    
    if (1 == SDK_WORK_PLATFORM)
    {
        ctc_sai_twamp_write_hardware_table(lchip); 
    } 
    
    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_twamp_db_deinit(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;


    if(NULL == p_ctc_sai_twamp[lchip])
    {
        return status;
    }
    
    if(NULL != p_ctc_sai_twamp[lchip])
    {
        mem_free(p_ctc_sai_twamp[lchip]);
    }

    return status;
}

