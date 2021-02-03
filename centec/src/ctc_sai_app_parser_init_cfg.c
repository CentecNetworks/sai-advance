
#include "sal.h"
//#include "ctc_app.h"
#include "api/include/ctc_api.h"
#include "ctc_sai_app_cfg_parse.h"
#include "ctc_sai_app_json.h"
#include "ctc_sai_app_cfg_chip_profile.h"
#include "ctc_sai_app_cfg_ftm_profile.h"
//#include "ctc_app_packet.h"
#include "sai.h"
#include "ctc_sai.h"


extern int32
_ctc_app_get_intr_cfg(ctc_intr_global_cfg_t* p_intr_cfg, ctc_init_chip_info_t* p_chip_info);

#define COUNTOF(_array_)    ((uint32)(sizeof((_array_)) / sizeof((_array_)[0])))

#define CTC_E_NONE 0
#define CTC_ERROR -1;

#define _MALLOC_ZERO(_type_, _ptr_, _size_)           \
        {                                                \
            if (_size_)                                  \
            {                                            \
                if(_ptr_ == NULL)  _ptr_= mem_malloc((_type_), (_size_));\
                if ((_ptr_)){                                \
                    sal_memset((_ptr_), 0, (_size_));        \
                }  else {                                    \
                    sal_printf("Error: No memory! Fun:%s() Line:%d \n",__FUNCTION__, __LINE__);\
                }                                            \
            }                                                \
        }


#define PARSE_ARRAY(pJson, p_array) \
    {\
        uint8 j = 0;\
        uint8 array_size_j = pJson->array_len;\
        cJSON* pSub_j = NULL;\
        for(j = 0; j < array_size_j; j++)\
        {\
            pSub_j=ctc_json_get_array_item(pJson, j);\
            if(pSub_j)\
            {\
                p_array[j] = pSub_j->value.number;\
            }\
        }\
    }

#define GET_PARSE_CFG_ARRAY(parma, field)  \
    p_tmp_json = ctc_json_get_object(p_json, #field); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_ARRAY) \
    {\
        PARSE_ARRAY(p_tmp_json, parma->field);\
    }

#define GET_PARSE_CFG_ARRAY2(parma, field)  \
    p_tmp_json = ctc_json_get_object(p_json, #field); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_ARRAY) \
    {\
        uint8 i = 0;\
        uint8 array_size = p_tmp_json->array_len;\
        cJSON* pSub = NULL;\
        for(i = 0; i < array_size; i++)\
        {\
            pSub=ctc_json_get_array_item(p_tmp_json, i);\
            if(pSub)\
            {\
                PARSE_ARRAY(pSub, parma->field[i]);\
            }\
        }\
    }

#define GET_PARSE_CFG_VALUE(parma, field)  \
    p_tmp_json = ctc_json_get_object(p_json, #field); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NUMBER) \
        parma->field = p_tmp_json->value.number;\
    else if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_STRING) \
        {\
        parma->field = sal_strtou32(p_tmp_json->value.string, NULL, 16);\
        }

#define GET_PARSE_CFG_PTR(parma, field)  \
    p_tmp_json = ctc_json_get_object(p_json, #field); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NONE) \
        parma->field = NULL;\
    else if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_STRING) \
        sal_memcpy(parma->field, p_tmp_json->value.string, sal_strlen(p_tmp_json->value.string));

#define GET_PARSE_CFG_PTR2(parma, field)  \
    p_tmp_json = ctc_json_get_object(p_json, #field); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NONE) \
        parma->field = NULL;\
    else if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_STRING) \
        sal_memcpy(&parma->field, p_tmp_json->value.string, sal_strlen(p_tmp_json->value.string));

#define FOR_EACH_OBJ_ARRAY(parma, field, i)    \
{\
     cJSON* p_arr_json = ctc_json_get_object(p_json, #field);\
     uint8 array_size = 0;\
    if(!p_arr_json || p_arr_json->type != APP_JSON_TYPE_ARRAY)\
    {\
        return 0;\
    }\
    array_size = p_arr_json->array_len;\
    for(i = 0; i < array_size; i++)\
    {\
        cJSON* p_json = ctc_json_get_array_item(p_arr_json, i);\

#define END_EACH_OBJ_ARRAY()  }\
}

#define GET_PARSE_CFG_OBJ(parma, field)    \
do{\
     cJSON* p_##field##_json = ctc_json_get_object(p_json, #field);\
    if(p_##field##_json && p_##field##_json->type == APP_JSON_TYPE_OBJECT)\
    {\
        cJSON* p_json = p_##field##_json;\


#define END_PARSE_CFG_OBJ()  }\
}while(0)

#define CFG_INIT_FLAG(string, bit) \
    p_tmp_json = ctc_json_get_object(p_json, string); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NUMBER && p_tmp_json->value.number) \
        CTC_SET_FLAG(flag, bit);

#define GET_PARSE_TCAM_KEY_INFO(parma) \
{\
    uint8 tbl_mem_id = 0;\
    p_tmp_json = ctc_json_get_object(p_json, "tbl_mem_id"); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NUMBER) \
    {\
        tbl_mem_id = p_tmp_json->value.number;\
        CTC_BIT_SET(parma->tcam_bitmap, tbl_mem_id); \
    }else\
        return 0;\
    p_tmp_json = ctc_json_get_object(p_json, "entry_offset"); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NUMBER) \
        parma->tcam_start_offset[tbl_mem_id] = p_tmp_json->value.number; \
    p_tmp_json = ctc_json_get_object(p_json, "entry_size"); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NUMBER) \
         parma->tcam_entry_num[tbl_mem_id] = p_tmp_json->value.number ; \
}

#define GET_PARSE_SRAM_TBL_INFO(parma)\
{\
    uint8 tbl_mem_id = 0;\
    p_tmp_json = ctc_json_get_object(p_json, "tbl_mem_id"); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NUMBER) \
    {\
        tbl_mem_id = p_tmp_json->value.number;\
        if(tbl_mem_id >= 32) \
            CTC_BIT_SET(parma->mem_high_bitmap, tbl_mem_id); \
        else \
            CTC_BIT_SET(parma->mem_bitmap, tbl_mem_id); \
    }else\
        return 0;\
    p_tmp_json = ctc_json_get_object(p_json, "entry_offset"); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NUMBER) \
        parma->mem_start_offset[tbl_mem_id] = p_tmp_json->value.number; \
    p_tmp_json = ctc_json_get_object(p_json, "entry_size"); \
    if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NUMBER) \
         parma->mem_entry_num[tbl_mem_id] = p_tmp_json->value.number ; \
}

void
_ctc_app_parse_init_flag(cJSON* pJson, uint32* p_flag)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    uint32 flag = 0;

    CFG_INIT_FLAG("mpls", CTC_INIT_MODULE_MPLS);
    CFG_INIT_FLAG("aps", CTC_INIT_MODULE_APS);
    CFG_INIT_FLAG("oam", CTC_INIT_MODULE_OAM);
    CFG_INIT_FLAG("ptp", CTC_INIT_MODULE_PTP);
    CFG_INIT_FLAG("synce", CTC_INIT_MODULE_SYNCE);
    CFG_INIT_FLAG("stacking", CTC_INIT_MODULE_STACKING);
    CFG_INIT_FLAG("bpe", CTC_INIT_MODULE_BPE);
    CFG_INIT_FLAG("ipfix", CTC_INIT_MODULE_IPFIX);
    CFG_INIT_FLAG("monitor", CTC_INIT_MODULE_MONITOR);
    CFG_INIT_FLAG("overlay", CTC_INIT_MODULE_OVERLAY);
    CFG_INIT_FLAG("efd", CTC_INIT_MODULE_EFD);
    CFG_INIT_FLAG("fcoe", CTC_INIT_MODULE_FCOE);
    CFG_INIT_FLAG("trill", CTC_INIT_MODULE_TRILL);
    CFG_INIT_FLAG("wlan", CTC_INIT_MODULE_WLAN);
    CFG_INIT_FLAG("npm", CTC_INIT_MODULE_NPM);
    CFG_INIT_FLAG("dot1ae", CTC_INIT_MODULE_DOT1AE);
    CFG_INIT_FLAG("srv6", CTC_INIT_MODULE_SRV6);
    CFG_INIT_FLAG("dtel", CTC_INIT_MODULE_DTEL);
    CFG_INIT_FLAG("sc_oam", CTC_INIT_MODULE_SC_OAM);
    CFG_INIT_FLAG("flexe", CTC_INIT_MODULE_FLEXE);

    *p_flag = flag;
}


uint32
_ctc_app_parser_acl_cfg(cJSON* pJson, ctc_acl_global_cfg_t* pacl_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pacl_cfg, arp_use_ipv6);
    GET_PARSE_CFG_VALUE(pacl_cfg, trill_use_ipv6);
    GET_PARSE_CFG_VALUE(pacl_cfg, hash_ipv4_key_flag);
    GET_PARSE_CFG_VALUE(pacl_cfg, egress_port_service_acl_en);
    GET_PARSE_CFG_VALUE(pacl_cfg, ingress_vlan_service_acl_en);
    GET_PARSE_CFG_VALUE(pacl_cfg, merge_mac_ip);
    GET_PARSE_CFG_VALUE(pacl_cfg, priority_bitmap_of_stats);
    GET_PARSE_CFG_VALUE(pacl_cfg, hash_mac_key_flag);
    GET_PARSE_CFG_VALUE(pacl_cfg, non_ipv4_mpls_use_ipv6);
    GET_PARSE_CFG_VALUE(pacl_cfg, white_list_en);
    GET_PARSE_CFG_VALUE(pacl_cfg, ingress_use_mapped_vlan);
    GET_PARSE_CFG_VALUE(pacl_cfg, ingress_port_service_acl_en);
    GET_PARSE_CFG_VALUE(pacl_cfg, egress_vlan_service_acl_en);
    GET_PARSE_CFG_VALUE(pacl_cfg, hash_acl_en);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_bpe_cfg(cJSON* pJson, ctc_bpe_global_cfg_t* pbpe_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pbpe_cfg, is_port_extender);
    GET_PARSE_CFG_VALUE(pbpe_cfg, port_base);
    GET_PARSE_CFG_VALUE(pbpe_cfg, max_mc_ecid_id);
    GET_PARSE_CFG_VALUE(pbpe_cfg, intlk_mode);
    GET_PARSE_CFG_VALUE(pbpe_cfg, max_uc_ecid_id);
    GET_PARSE_CFG_VALUE(pbpe_cfg, logic_port_en);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_diag_cfg(cJSON* pJson, ctc_diag_global_cfg_t* pdiag_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pdiag_cfg, rsv);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_vlan_cfg(cJSON* pJson, ctc_vlan_global_cfg_t* pvlan_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pvlan_cfg, vlanptr_mode);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_dma_cfg(cJSON* pJson, ctc_dma_global_cfg_t* pdma_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    uint8 i = 0;
    GET_PARSE_CFG_VALUE(pdma_cfg, table_w_desc_num);
    //GET_PARSE_CFG_ARRAY2(pdma_cfg, pkt_tx_ext);
    GET_PARSE_CFG_VALUE(pdma_cfg, func_en_bitmap);
    GET_PARSE_CFG_VALUE(pdma_cfg, pkt_rx_chan_num);
    //GET_PARSE_CFG_ARRAY2(pdma_cfg, pkt_rx);
    GET_PARSE_CFG_VALUE(pdma_cfg, pkt_rx_size_per_desc);
    GET_PARSE_CFG_VALUE(pdma_cfg, hw_learning_sync_en);
    GET_PARSE_CFG_VALUE(pdma_cfg, table_r_desc_num);
    GET_PARSE_CFG_VALUE(pdma_cfg, pkt_tx_desc_num);

    GET_PARSE_CFG_OBJ(pdma_cfg, stats)
        ctc_dma_chan_cfg_t* p_stats = &pdma_cfg->stats;
        GET_PARSE_CFG_VALUE(p_stats, desc_num);
        GET_PARSE_CFG_VALUE(p_stats, priority);
        GET_PARSE_CFG_VALUE(p_stats, dmasel);
        GET_PARSE_CFG_VALUE(p_stats, data);
        GET_PARSE_CFG_VALUE(p_stats, pkt_knet_en);
    END_PARSE_CFG_OBJ();

    GET_PARSE_CFG_OBJ(pdma_cfg, learning)
        ctc_dma_chan_cfg_t* p_learning = &pdma_cfg->learning;
        GET_PARSE_CFG_VALUE(p_learning, desc_num);
        GET_PARSE_CFG_VALUE(p_learning, priority);
        GET_PARSE_CFG_VALUE(p_learning, dmasel);
        GET_PARSE_CFG_VALUE(p_learning, data);
        GET_PARSE_CFG_VALUE(p_learning, pkt_knet_en);
    END_PARSE_CFG_OBJ();

     GET_PARSE_CFG_OBJ(pdma_cfg, ipfix)
        ctc_dma_chan_cfg_t* p_ipfix = &pdma_cfg->ipfix;
        GET_PARSE_CFG_VALUE(p_ipfix, desc_num);
        GET_PARSE_CFG_VALUE(p_ipfix, priority);
        GET_PARSE_CFG_VALUE(p_ipfix, dmasel);
        GET_PARSE_CFG_VALUE(p_ipfix, data);
        GET_PARSE_CFG_VALUE(p_ipfix, pkt_knet_en);
    END_PARSE_CFG_OBJ();

     GET_PARSE_CFG_OBJ(pdma_cfg, pkt_tx)
        ctc_dma_chan_cfg_t* p_pkt_tx = &pdma_cfg->pkt_tx;
        GET_PARSE_CFG_VALUE(p_pkt_tx, desc_num);
        GET_PARSE_CFG_VALUE(p_pkt_tx, priority);
        GET_PARSE_CFG_VALUE(p_pkt_tx, dmasel);
        GET_PARSE_CFG_VALUE(p_pkt_tx, data);
        GET_PARSE_CFG_VALUE(p_pkt_tx, pkt_knet_en);
    END_PARSE_CFG_OBJ();

    FOR_EACH_OBJ_ARRAY(pdma_cfg, pkt_rx, i)
        ctc_dma_chan_cfg_t* p_pkt_rx = &(pdma_cfg->pkt_rx[i]);
        GET_PARSE_CFG_VALUE(p_pkt_rx, desc_num);
        GET_PARSE_CFG_VALUE(p_pkt_rx, priority);
        GET_PARSE_CFG_VALUE(p_pkt_rx, dmasel);
        GET_PARSE_CFG_VALUE(p_pkt_rx, data);
        GET_PARSE_CFG_VALUE(p_pkt_rx, pkt_knet_en);
    END_EACH_OBJ_ARRAY();

    FOR_EACH_OBJ_ARRAY(pdma_cfg, pkt_tx_ext, i)
        ctc_dma_chan_cfg_t* p_pkt_tx_ext = &(pdma_cfg->pkt_tx_ext[i]);
        GET_PARSE_CFG_VALUE(p_pkt_tx_ext, desc_num);
        GET_PARSE_CFG_VALUE(p_pkt_tx_ext, priority);
        GET_PARSE_CFG_VALUE(p_pkt_tx_ext, dmasel);
        GET_PARSE_CFG_VALUE(p_pkt_tx_ext, data);
        GET_PARSE_CFG_VALUE(p_pkt_tx_ext, pkt_knet_en);
    END_EACH_OBJ_ARRAY();

    return CTC_E_NONE;
}

uint32
_ctc_app_parser_intr_cfg(cJSON* pJson, ctc_intr_global_cfg_t* pintr_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    ctc_init_chip_info_t chip_info;
    sal_memset(&chip_info, 0, sizeof(ctc_init_chip_info_t));

    GET_PARSE_CFG_VALUE(pintr_cfg, intr_mode);
    chip_info.interrupt_mode = pintr_cfg->intr_mode;
    _ctc_app_get_intr_cfg(pintr_cfg, &chip_info);

    if(pintr_cfg->intr_mode == 0)
    {
        GET_PARSE_CFG_VALUE(pintr_cfg->p_group, irq);
    }

    return CTC_E_NONE;
}

uint32
_ctc_app_parser_ipfix_cfg(cJSON* pJson, ctc_ipfix_global_cfg_t* pipfix_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pipfix_cfg, aging_interval);
    GET_PARSE_CFG_VALUE(pipfix_cfg, new_flow_export_en);
    GET_PARSE_CFG_VALUE(pipfix_cfg, conflict_export);
    GET_PARSE_CFG_VALUE(pipfix_cfg, latency_type);
    GET_PARSE_CFG_VALUE(pipfix_cfg, threshold);
    GET_PARSE_CFG_VALUE(pipfix_cfg, dest_port_type);
    GET_PARSE_CFG_VALUE(pipfix_cfg, ignore_drop_reason);
    GET_PARSE_CFG_VALUE(pipfix_cfg, times_interval);
    GET_PARSE_CFG_VALUE(pipfix_cfg, jitter_thrd);
    GET_PARSE_CFG_VALUE(pipfix_cfg, bytes_cnt);
    GET_PARSE_CFG_VALUE(pipfix_cfg, pkt_cnt);
    GET_PARSE_CFG_VALUE(pipfix_cfg, drop_pkt_cnt);
    GET_PARSE_CFG_VALUE(pipfix_cfg, mirror_pkt_enable);
    GET_PARSE_CFG_VALUE(pipfix_cfg, tcp_end_detect_en);
    GET_PARSE_CFG_VALUE(pipfix_cfg, max_export_entry_num);
    GET_PARSE_CFG_VALUE(pipfix_cfg, latency_thrd);
    GET_PARSE_CFG_VALUE(pipfix_cfg, unkown_pkt_dest_type);
    GET_PARSE_CFG_VALUE(pipfix_cfg, conflict_cnt);
    GET_PARSE_CFG_VALUE(pipfix_cfg, export_interval);
    GET_PARSE_CFG_VALUE(pipfix_cfg, queue_drop_en);
    GET_PARSE_CFG_VALUE(pipfix_cfg, sample_mode);
    GET_PARSE_CFG_VALUE(pipfix_cfg, latency_ewma_weight);
    GET_PARSE_CFG_VALUE(pipfix_cfg, sw_learning_en);
    GET_PARSE_CFG_VALUE(pipfix_cfg, jitter_ewma_weight);
    GET_PARSE_CFG_VALUE(pipfix_cfg, egs_ipfix_disable);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_l2_fdb_cfg(cJSON* pJson, ctc_l2_fdb_global_cfg_t* pl2_fdb_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pl2_fdb_cfg, hw_learn_en);
    GET_PARSE_CFG_VALUE(pl2_fdb_cfg, flush_fdb_cnt_per_loop);
    GET_PARSE_CFG_VALUE(pl2_fdb_cfg, static_fdb_limit_en);
    GET_PARSE_CFG_VALUE(pl2_fdb_cfg, logic_port_num);
    GET_PARSE_CFG_VALUE(pl2_fdb_cfg, stp_mode);
    GET_PARSE_CFG_VALUE(pl2_fdb_cfg, default_entry_rsv_num);
    GET_PARSE_CFG_VALUE(pl2_fdb_cfg, trie_sort_en);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_l3if_cfg(cJSON* pJson, ctc_l3if_global_cfg_t* pl3if_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pl3if_cfg, ipv6_vrf_en);
    GET_PARSE_CFG_VALUE(pl3if_cfg, keep_ivlan_en);
    GET_PARSE_CFG_VALUE(pl3if_cfg, max_vrfid_num);
    GET_PARSE_CFG_VALUE(pl3if_cfg, ipv4_vrf_en);
    GET_PARSE_CFG_VALUE(pl3if_cfg, rtmac_mode);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_learn_aging_cfg(cJSON* pJson, ctc_learn_aging_global_cfg_t* plearn_aging_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(plearn_aging_cfg, scl_aging_en);
    GET_PARSE_CFG_VALUE(plearn_aging_cfg, mac_aging_dis);
    GET_PARSE_CFG_VALUE(plearn_aging_cfg, hw_mac_aging_en);
    GET_PARSE_CFG_VALUE(plearn_aging_cfg, hw_mac_learn_en);
    GET_PARSE_CFG_VALUE(plearn_aging_cfg, hw_scl_aging_en);
    GET_PARSE_CFG_VALUE(plearn_aging_cfg, ipmc_aging_en);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_linkagg_cfg(cJSON* pJson, ctc_linkagg_global_cfg_t* plinkagg_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    //GET_PARSE_CFG_ARRAY(plinkagg_cfg, rsv0);
    GET_PARSE_CFG_VALUE(plinkagg_cfg, bind_gport_disable);
    GET_PARSE_CFG_VALUE(plinkagg_cfg, linkagg_mode);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_nh_cfg(cJSON* pJson, ctc_nh_global_cfg_t* pnh_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pnh_cfg, max_ecmp);
    GET_PARSE_CFG_VALUE(pnh_cfg, max_external_nhid);
    GET_PARSE_CFG_VALUE(pnh_cfg, max_tunnel_id);
    GET_PARSE_CFG_VALUE(pnh_cfg, acl_redirect_fwd_ptr_num);
    GET_PARSE_CFG_VALUE(pnh_cfg, nh_edit_mode);
    //GET_PARSE_CFG_ARRAY(pnh_cfg, rsv);
    GET_PARSE_CFG_VALUE(pnh_cfg, h_ecmp_en);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_npm_cfg(cJSON* pJson, ctc_npm_global_cfg_t* pnpm_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    //GET_PARSE_CFG_ARRAY(pnpm_cfg, rsv);
    GET_PARSE_CFG_ARRAY(pnpm_cfg, emix_size);
    GET_PARSE_CFG_VALUE(pnpm_cfg, session_mode);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_overlay_tunnel_cfg(cJSON* pJson, ctc_overlay_tunnel_global_cfg_t* poverlay_tunnel_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(poverlay_tunnel_cfg, nvgre_mode);
    GET_PARSE_CFG_VALUE(poverlay_tunnel_cfg, vxlan_mode);
    GET_PARSE_CFG_VALUE(poverlay_tunnel_cfg, vni_mapping_mode);
    GET_PARSE_CFG_VALUE(poverlay_tunnel_cfg, cloud_sec_en);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_pkt_cfg(cJSON* pJson, ctc_pkt_global_cfg_t* ppkt_cfg)
{
//SAI mark
#if 0
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(ppkt_cfg, raw_mode_en);
    ppkt_cfg->rx_cb         = ctc_app_packet_sample_rx;
#ifdef _SAL_LINUX_UM
    ppkt_cfg->socket_tx_cb = ctc_app_packet_sample_tx;
#endif
#endif
    return CTC_E_NONE;
}


uint32
_ctc_app_parser_parser_cfg(cJSON* pJson, ctc_parser_global_cfg_t* pparser_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pparser_cfg, lb_hash_mode);
    GET_PARSE_CFG_ARRAY(pparser_cfg, dlb_efd_tunnel_hash_mode);
    GET_PARSE_CFG_VALUE(pparser_cfg, ecmp_hash_type);
    GET_PARSE_CFG_VALUE(pparser_cfg, linkagg_hash_type);
    GET_PARSE_CFG_ARRAY(pparser_cfg, ecmp_tunnel_hash_mode);
    GET_PARSE_CFG_VALUE(pparser_cfg, symmetric_hash_en);
    GET_PARSE_CFG_ARRAY(pparser_cfg, linkagg_tunnel_hash_mode);
    GET_PARSE_CFG_VALUE(pparser_cfg, small_frag_offset);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_port_cfg(cJSON* pJson, ctc_port_global_cfg_t* pport_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pport_cfg, use_isolation_id);
    GET_PARSE_CFG_VALUE(pport_cfg, default_logic_port_en);
    GET_PARSE_CFG_VALUE(pport_cfg, isolation_group_mode);
    GET_PARSE_CFG_VALUE(pport_cfg, rsv0);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_srv6_cfg(cJSON* pJson, ctc_srv6_global_cfg_t* psrv6_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(psrv6_cfg, usid_prefix_len);
    GET_PARSE_CFG_VALUE(psrv6_cfg, sid_format_bmp);
    GET_PARSE_CFG_VALUE(psrv6_cfg, gsid_prefix_len);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_stats_cfg(cJSON* pJson, ctc_stats_global_cfg_t* pstats_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pstats_cfg, query_mode);
    GET_PARSE_CFG_VALUE(pstats_cfg, stats_bitmap);
    GET_PARSE_CFG_VALUE(pstats_cfg, policer_stats_num);
    GET_PARSE_CFG_VALUE(pstats_cfg, mac_timer);
    GET_PARSE_CFG_VALUE(pstats_cfg, stats_mode);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_wlan_cfg(cJSON* pJson, ctc_wlan_global_cfg_t* pwlan_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pwlan_cfg, default_client_action);
    GET_PARSE_CFG_VALUE(pwlan_cfg, fc_swap_enable);
    GET_PARSE_CFG_VALUE(pwlan_cfg, default_client_vlan_id);
    GET_PARSE_CFG_VALUE(pwlan_cfg, udp_dest_port0);
    GET_PARSE_CFG_VALUE(pwlan_cfg, udp_dest_port1);
    GET_PARSE_CFG_VALUE(pwlan_cfg, dtls_version);
    GET_PARSE_CFG_VALUE(pwlan_cfg, control_pkt_decrypt_en);
    GET_PARSE_CFG_ARRAY(pwlan_cfg, rsv);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_ipuc_cfg(cJSON* pJson, ctc_ipuc_global_cfg_t* pipuc_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pipuc_cfg, host_use_lpm);
    GET_PARSE_CFG_VALUE(pipuc_cfg, prefix64_mode);
    GET_PARSE_CFG_VALUE(pipuc_cfg, default_route_mode);
    GET_PARSE_CFG_VALUE(pipuc_cfg, arc_disable);
    GET_PARSE_CFG_VALUE(pipuc_cfg, rpf_check_port);
    GET_PARSE_CFG_VALUE(pipuc_cfg, use_hash8);
    GET_PARSE_CFG_PTR2(pipuc_cfg, callback);
    GET_PARSE_CFG_PTR(pipuc_cfg, user_data);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_chip_cfg(cJSON* pJson, ctc_chip_global_cfg_t* pchip_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pchip_cfg, lchip);
    GET_PARSE_CFG_VALUE(pchip_cfg, cpu_port_en);
    GET_PARSE_CFG_VALUE(pchip_cfg, gb_gg_interconnect_en);
    GET_PARSE_CFG_VALUE(pchip_cfg, rchain_en);
    GET_PARSE_CFG_VALUE(pchip_cfg, rchain_gchip);
    GET_PARSE_CFG_VALUE(pchip_cfg, tpid);
    GET_PARSE_CFG_VALUE(pchip_cfg, vlanid);
    GET_PARSE_CFG_VALUE(pchip_cfg, cpu_port);
    GET_PARSE_CFG_VALUE(pchip_cfg, cut_through_en);
    GET_PARSE_CFG_VALUE(pchip_cfg, cut_through_speed);
    GET_PARSE_CFG_VALUE(pchip_cfg, cut_through_speed_bitmap);
    GET_PARSE_CFG_VALUE(pchip_cfg, ecc_recover_en);
    GET_PARSE_CFG_VALUE(pchip_cfg, tcam_scan_en);
    GET_PARSE_CFG_VALUE(pchip_cfg, sdb_en);
    GET_PARSE_CFG_VALUE(pchip_cfg, sdb_type);
    GET_PARSE_CFG_VALUE(pchip_cfg, sdb_mem_addr);
    GET_PARSE_CFG_VALUE(pchip_cfg, sdb_mem_size);
    GET_PARSE_CFG_VALUE(pchip_cfg, alpm_affinity_mask);
    GET_PARSE_CFG_VALUE(pchip_cfg, normal_affinity_mask);
    GET_PARSE_CFG_VALUE(pchip_cfg, wb_dm_mem_size);

    GET_PARSE_CFG_ARRAY(pchip_cfg, cpu_mac_sa);
    GET_PARSE_CFG_ARRAY2(pchip_cfg, cpu_mac_da);

    return CTC_E_NONE;
}

uint32
_ctc_app_parser_qos_cfg(cJSON* pJson, ctc_qos_global_cfg_t* pqos_cfg)
{
    cJSON* p_resrc_pool_obj = NULL;
    cJSON* p_policer_level_obj = NULL;
    cJSON* p_tmp_json = NULL;
    cJSON* p_json = pJson;

    GET_PARSE_CFG_VALUE(pqos_cfg, queue_num_per_network_port);
    GET_PARSE_CFG_VALUE(pqos_cfg, queue_num_per_internal_port);
    GET_PARSE_CFG_VALUE(pqos_cfg, queue_num_per_cpu_reason_group);
    GET_PARSE_CFG_VALUE(pqos_cfg, queue_aging_time);
    GET_PARSE_CFG_VALUE(pqos_cfg, max_cos_level);
    GET_PARSE_CFG_VALUE(pqos_cfg, policer_num);
    GET_PARSE_CFG_VALUE(pqos_cfg, queue_num_for_cpu_reason);
    GET_PARSE_CFG_VALUE(pqos_cfg, cpu_queue_shape_profile_num);
    GET_PARSE_CFG_VALUE(pqos_cfg, ingress_vlan_policer_num);
    GET_PARSE_CFG_VALUE(pqos_cfg, egress_vlan_policer_num);
    GET_PARSE_CFG_VALUE(pqos_cfg, policer_merge_mode);
    GET_PARSE_CFG_VALUE(pqos_cfg, service_queue_mode);
    GET_PARSE_CFG_VALUE(pqos_cfg, queue_num_per_ingress_service);
    GET_PARSE_CFG_VALUE(pqos_cfg, priority_mode);
    GET_PARSE_CFG_VALUE(pqos_cfg, policer_svc_mode);
    GET_PARSE_CFG_VALUE(pqos_cfg, igs_macro_policer_num);
    GET_PARSE_CFG_VALUE(pqos_cfg, egs_macro_policer_num);


    p_resrc_pool_obj = ctc_json_get_object(pJson, "resrc_pool");
    if(p_resrc_pool_obj && p_resrc_pool_obj->type == APP_JSON_TYPE_OBJECT)
    {
        ctc_qos_resrc_pool_cfg_t* presrc_pool = &(pqos_cfg->resrc_pool);
        uint8 i = 0, j = 0;
        p_json = p_resrc_pool_obj;
        GET_PARSE_CFG_ARRAY(presrc_pool, igs_pool_size);
        GET_PARSE_CFG_ARRAY(presrc_pool, egs_pool_size);
        GET_PARSE_CFG_VALUE(presrc_pool, igs_pool_mode);
        GET_PARSE_CFG_VALUE(presrc_pool, egs_pool_mode);

        FOR_EACH_OBJ_ARRAY(presrc_pool, drop_profile, i)
            ctc_qos_resrc_drop_profile_t* p_drop_profile = &(presrc_pool->drop_profile[i]);
            GET_PARSE_CFG_VALUE(p_drop_profile, congest_level_num);
            GET_PARSE_CFG_ARRAY(p_drop_profile, congest_threshold);

            FOR_EACH_OBJ_ARRAY(p_drop_profile, queue_drop, j)
                ctc_qos_queue_drop_t* p_queue_drop = &(p_drop_profile->queue_drop[j]);
                GET_PARSE_CFG_VALUE(p_queue_drop, mode);
                GET_PARSE_CFG_VALUE(p_queue_drop, is_coexist);
                GET_PARSE_CFG_VALUE(p_queue_drop, ecn_mark_th);
                GET_PARSE_CFG_VALUE(p_queue_drop, is_dynamic);
                GET_PARSE_CFG_ARRAY(p_queue_drop, min_th);
                GET_PARSE_CFG_ARRAY(p_queue_drop, max_th);
                GET_PARSE_CFG_ARRAY(p_queue_drop, drop_prob);
                GET_PARSE_CFG_ARRAY(p_queue_drop, ecn_th);
                GET_PARSE_CFG_ARRAY(p_queue_drop, drop_factor);
            END_EACH_OBJ_ARRAY();
        END_EACH_OBJ_ARRAY();
    }

    p_policer_level_obj = ctc_json_get_object(pJson, "policer_level");
    if(p_policer_level_obj)
    {
        cJSON* p_json = p_policer_level_obj;
        ctc_qos_policer_level_select_t*  p_policer_level = &(pqos_cfg->policer_level);
        GET_PARSE_CFG_VALUE(p_policer_level, ingress_port_level);
        GET_PARSE_CFG_VALUE(p_policer_level, ingress_vlan_level);
        GET_PARSE_CFG_VALUE(p_policer_level, egress_port_level);
        GET_PARSE_CFG_VALUE(p_policer_level, egress_vlan_level);
    }

    return 0;
}

uint32
_ctc_app_parser_stacking_cfg(cJSON* pJson, ctc_stacking_glb_cfg_t* pstacking_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pstacking_cfg, trunk_mode);
    GET_PARSE_CFG_VALUE(pstacking_cfg, fabric_mode);
    GET_PARSE_CFG_VALUE(pstacking_cfg, version);
    GET_PARSE_CFG_VALUE(pstacking_cfg, learning_mode);
    GET_PARSE_CFG_VALUE(pstacking_cfg, src_port_mode);
    GET_PARSE_CFG_VALUE(pstacking_cfg, mcast_mode);

    GET_PARSE_CFG_OBJ(pstacking_cfg, hdr_glb)
        ctc_stacking_hdr_glb_t* p_hdr_glb = &pstacking_cfg->hdr_glb;
        GET_PARSE_CFG_VALUE(p_hdr_glb, mac_da_chk_en);
        GET_PARSE_CFG_VALUE(p_hdr_glb, ether_type_chk_en);
        GET_PARSE_CFG_VALUE(p_hdr_glb, cos);
        GET_PARSE_CFG_VALUE(p_hdr_glb, ip_protocol);
        GET_PARSE_CFG_VALUE(p_hdr_glb, vlan_tpid);
        GET_PARSE_CFG_VALUE(p_hdr_glb, ether_type);
        GET_PARSE_CFG_VALUE(p_hdr_glb, ip_ttl);
        GET_PARSE_CFG_VALUE(p_hdr_glb, ip_dscp);
        GET_PARSE_CFG_VALUE(p_hdr_glb, udp_en);
        //GET_PARSE_CFG_VALUE(p_hdr_glb, ipsa);
        GET_PARSE_CFG_VALUE(p_hdr_glb, ip_dscp);
        GET_PARSE_CFG_VALUE(p_hdr_glb, udp_src_port);
        GET_PARSE_CFG_VALUE(p_hdr_glb, udp_dest_port);
    END_PARSE_CFG_OBJ();

    GET_PARSE_CFG_OBJ(pstacking_cfg, connect_glb)
        ctc_stacking_inter_connect_glb_t* p_connect_glb = &pstacking_cfg->connect_glb;
        GET_PARSE_CFG_VALUE(p_connect_glb, mode);
        GET_PARSE_CFG_VALUE(p_connect_glb, member_num);
        GET_PARSE_CFG_ARRAY2(p_connect_glb, member_port);
    END_PARSE_CFG_OBJ();

    return CTC_E_NONE;
}

uint32
_ctc_app_parser_oam_cfg(cJSON* pJson, ctc_oam_global_t* poam_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(poam_cfg, tp_section_oam_based_l3if);
    GET_PARSE_CFG_VALUE(poam_cfg, tp_csf_clear);
    GET_PARSE_CFG_VALUE(poam_cfg, mep_index_alloc_by_sdk);
    GET_PARSE_CFG_VALUE(poam_cfg, tp_csf_fdi);
    GET_PARSE_CFG_VALUE(poam_cfg, tp_csf_ach_chan_type);
    GET_PARSE_CFG_VALUE(poam_cfg, tp_bfd_333ms);
    GET_PARSE_CFG_VALUE(poam_cfg, mpls_pw_vccv_with_ip_en);
    GET_PARSE_CFG_VALUE(poam_cfg, tp_csf_los);
    GET_PARSE_CFG_VALUE(poam_cfg, maid_len_format);
    GET_PARSE_CFG_VALUE(poam_cfg, mep_1ms_num);
    GET_PARSE_CFG_VALUE(poam_cfg, tp_csf_rdi);
    GET_PARSE_CFG_VALUE(poam_cfg, tp_y1731_ach_chan_type);
    return CTC_E_NONE;
}

uint32
_ctc_app_parser_ptp_cfg(cJSON* pJson, ctc_ptp_global_config_t* pptp_cfg)
{
    cJSON* p_json = pJson;
    cJSON* p_tmp_json = NULL;
    GET_PARSE_CFG_VALUE(pptp_cfg, delay_request_process_en);
    GET_PARSE_CFG_VALUE(pptp_cfg, sync_copy_to_cpu_en);
    GET_PARSE_CFG_VALUE(pptp_cfg, management_copy_to_cpu_en);
    GET_PARSE_CFG_VALUE(pptp_cfg, port_based_ptp_en);
    GET_PARSE_CFG_VALUE(pptp_cfg, ptp_ucast_en);
    GET_PARSE_CFG_VALUE(pptp_cfg, use_internal_clock_en);
    GET_PARSE_CFG_VALUE(pptp_cfg, signaling_copy_to_cpu_en);
    GET_PARSE_CFG_VALUE(pptp_cfg, cache_aging_time);
    GET_PARSE_CFG_VALUE(pptp_cfg, intf_selected);
    return CTC_E_NONE;
}

uint32
ctc_app_get_json_profile(uint8 lchip, char* mem_buf, ctc_init_cfg_t* p_init_config)
{
    cJSON* pJson = NULL;
    cJSON* pObj = NULL;
    cJSON* p_json = NULL;
    cJSON* p_tmp_json = NULL;

    if(ctc_json_parse((const char *)mem_buf, &pJson))
    {
        ctc_json_free(pJson);
        return CTC_ERROR;
    }
    CTC_SAI_LOG_DEBUG(SAI_API_SWITCH, "Use json profile to initialize \n");
    p_json = pJson;
    //GET_PARSE_CFG_VALUE(p_init_config, init_flag);
    GET_PARSE_CFG_VALUE(p_init_config, local_chip_num);
    GET_PARSE_CFG_VALUE(p_init_config, port_phy_mapping_en);
    GET_PARSE_CFG_ARRAY(p_init_config, gchip);

    pObj = ctc_json_get_object(pJson, "init_config");
    if(pObj && pObj->type == APP_JSON_TYPE_ARRAY)
    {
        lchip = p_json->array_len > lchip ? lchip : 0;
        pJson = ctc_json_get_array_item(pObj, lchip);
        if(!pJson)
        {
            ctc_json_free(p_json);
            return CTC_ERROR;
        }
    }
    else
    {
        ctc_json_free(p_json);
        return CTC_ERROR;
    }

    pObj = ctc_json_get_object(pJson, "init_feature");
    if(pObj)
    {
        _ctc_app_parse_init_flag(pObj, &p_init_config->init_flag);
    }

    pObj = ctc_json_get_object(pJson, "acl_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_acl_cfg, sizeof(ctc_acl_global_cfg_t));
        _ctc_app_parser_acl_cfg(pObj, p_init_config->p_acl_cfg);
    }

    pObj = ctc_json_get_object(pJson, "bpe_cfg");
    if(pObj )
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_bpe_cfg, sizeof(ctc_bpe_global_cfg_t));
        _ctc_app_parser_bpe_cfg(pObj, p_init_config->p_bpe_cfg);
    }

    /*
    pObj = ctc_json_get_object(pJson, "datapath_cfg");
    if(pObj)
    {
        //_ctc_app_parser_datapath_cfg(pObj, p_init_config->p_datapath_cfg);
    }
    */

    pObj = ctc_json_get_object(pJson, "diag_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_diag_cfg, sizeof(ctc_diag_global_cfg_t));
        _ctc_app_parser_diag_cfg(pObj, p_init_config->p_diag_cfg);
    }

    pObj = ctc_json_get_object(pJson, "vlan_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_vlan_cfg, sizeof(ctc_vlan_global_cfg_t));
        _ctc_app_parser_vlan_cfg(pObj, p_init_config->p_vlan_cfg);
    }

    pObj = ctc_json_get_object(pJson, "learning_aging_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_learning_aging_cfg, sizeof(ctc_learn_aging_global_cfg_t));
        _ctc_app_parser_learn_aging_cfg(pObj, p_init_config->p_learning_aging_cfg);
    }

    pObj = ctc_json_get_object(pJson, "dma_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_dma_cfg, sizeof(ctc_dma_global_cfg_t));
        _ctc_app_parser_dma_cfg(pObj, p_init_config->p_dma_cfg);
    }

    pObj = ctc_json_get_object(pJson, "intr_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_intr_cfg, sizeof(ctc_intr_global_cfg_t));
        _ctc_app_parser_intr_cfg(pObj, p_init_config->p_intr_cfg);
    }

    pObj = ctc_json_get_object(pJson, "ipfix_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_ipifx_cfg, sizeof(ctc_ipfix_global_cfg_t));
        _ctc_app_parser_ipfix_cfg(pObj, p_init_config->p_ipifx_cfg);
    }

    pObj = ctc_json_get_object(pJson, "l2_fdb_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_l2_fdb_cfg, sizeof(ctc_l2_fdb_global_cfg_t));
        _ctc_app_parser_l2_fdb_cfg(pObj, p_init_config->p_l2_fdb_cfg);
    }

    pObj = ctc_json_get_object(pJson, "l3if_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_l3if_cfg, sizeof(ctc_l3if_global_cfg_t));
        _ctc_app_parser_l3if_cfg(pObj, p_init_config->p_l3if_cfg);
    }

    pObj = ctc_json_get_object(pJson, "learning_aging_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_learning_aging_cfg, sizeof(ctc_learn_aging_global_cfg_t));
        _ctc_app_parser_learn_aging_cfg(pObj, p_init_config->p_learning_aging_cfg);
    }

    pObj = ctc_json_get_object(pJson, "linkagg_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_linkagg_cfg, sizeof(ctc_linkagg_global_cfg_t));
        _ctc_app_parser_linkagg_cfg(pObj, p_init_config->p_linkagg_cfg);
    }
    
    pObj = ctc_json_get_object(pJson, "nh_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_nh_cfg, sizeof(ctc_nh_global_cfg_t));
        _ctc_app_parser_nh_cfg(pObj, p_init_config->p_nh_cfg);
    }

    pObj = ctc_json_get_object(pJson, "npm_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_npm_cfg, sizeof(ctc_npm_global_cfg_t));
        _ctc_app_parser_npm_cfg(pObj, p_init_config->p_npm_cfg);
    }

    pObj = ctc_json_get_object(pJson, "overlay_tunnel_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_overlay_cfg, sizeof(ctc_overlay_tunnel_global_cfg_t));
        _ctc_app_parser_overlay_tunnel_cfg(pObj, p_init_config->p_overlay_cfg);
    }

    pObj = ctc_json_get_object(pJson, "pkt_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_pkt_cfg, sizeof(ctc_pkt_global_cfg_t));
        _ctc_app_parser_pkt_cfg(pObj, p_init_config->p_pkt_cfg);
    }

    pObj = ctc_json_get_object(pJson, "parser_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_parser_cfg, sizeof(ctc_parser_global_cfg_t));
        _ctc_app_parser_parser_cfg(pObj, p_init_config->p_parser_cfg);
    }

    pObj = ctc_json_get_object(pJson, "port_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_port_cfg, sizeof(ctc_port_global_cfg_t));
        _ctc_app_parser_port_cfg(pObj, p_init_config->p_port_cfg);
    }

    pObj = ctc_json_get_object(pJson, "srv6_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_srv6_cfg, sizeof(ctc_srv6_global_cfg_t));
        _ctc_app_parser_srv6_cfg(pObj, p_init_config->p_srv6_cfg);
    }

    pObj = ctc_json_get_object(pJson, "stats_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_stats_cfg, sizeof(ctc_stats_global_cfg_t));
        _ctc_app_parser_stats_cfg(pObj, p_init_config->p_stats_cfg);
    }

    pObj = ctc_json_get_object(pJson, "wlan_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_wlan_cfg, sizeof(ctc_wlan_global_cfg_t));
        _ctc_app_parser_wlan_cfg(pObj, p_init_config->p_wlan_cfg);
    }

    pObj = ctc_json_get_object(pJson, "chip_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_chip_cfg, sizeof(ctc_chip_global_cfg_t));
        _ctc_app_parser_chip_cfg(pObj, p_init_config->p_chip_cfg);
    }

    pObj = ctc_json_get_object(pJson, "qos_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_qos_cfg, sizeof(ctc_qos_global_cfg_t));
        _ctc_app_parser_qos_cfg(pObj, p_init_config->p_qos_cfg);
    }

    pObj = ctc_json_get_object(pJson, "ipuc_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_ipuc_cfg, sizeof(ctc_ipuc_global_cfg_t));
        _ctc_app_parser_ipuc_cfg(pObj, p_init_config->p_ipuc_cfg);
    }

    pObj = ctc_json_get_object(pJson, "stacking_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_stacking_cfg, sizeof(ctc_stacking_glb_cfg_t));
        _ctc_app_parser_stacking_cfg(pObj, p_init_config->p_stacking_cfg);
    }

    pObj = ctc_json_get_object(pJson, "oam_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_oam_cfg, sizeof(ctc_oam_global_t));
        _ctc_app_parser_oam_cfg(pObj, p_init_config->p_oam_cfg);
    }

    pObj = ctc_json_get_object(pJson, "ptp_cfg");
    if(pObj)
    {
        _MALLOC_ZERO(MEM_APP_MODULE, p_init_config->p_ptp_cfg, sizeof(ctc_ptp_global_config_t));
        _ctc_app_parser_ptp_cfg(pObj, p_init_config->p_ptp_cfg);
    }

    ctc_json_free(p_json);
    return CTC_E_NONE;
}

ctc_key_name_value_pair_t ftm_specs_pair[] = {
        {"mac" ,        CTC_FTM_SPEC_MAC},
        {"ip_host" ,    CTC_FTM_SPEC_IPUC_HOST},
        {"ip_lpm" ,     CTC_FTM_SPEC_IPUC_LPM},
        {"ipmc" ,       CTC_FTM_SPEC_IPMC},
        {"acl" ,        CTC_FTM_SPEC_ACL},
        {"scl_flow",    CTC_FTM_SPEC_SCL_FLOW},
        {"acl_flow",    CTC_FTM_SPEC_ACL_FLOW},
        {"oam" ,        CTC_FTM_SPEC_OAM},
        {"scl" ,        CTC_FTM_SPEC_SCL},
        {"tunnel_decp" ,CTC_FTM_SPEC_TUNNEL},
        {"mpls" ,       CTC_FTM_SPEC_MPLS},
        {"l2mcast" ,    CTC_FTM_SPEC_L2MC},
        {"ipfix" ,      CTC_FTM_SPEC_IPFIX},
        {"napt" ,       CTC_FTM_SPEC_NAPT},
        {"vlan_xlate",  CTC_FTM_SPEC_VLAN_XLATE},
        {"scl_group",   CTC_FTM_SPEC_SCL_GROUP},
        {"acl_group",   CTC_FTM_SPEC_ACL_GROUP},
        {"rchip_port",  CTC_FTM_SPEC_RCHIP_PORT},
        {"static_fdb",  CTC_FTM_SPEC_STATIC_FDB},
        {"ipuc_lpmv6",  CTC_FTM_SPEC_IPUC_LPMv6},
        {"ipuc_nd",     CTC_FTM_SPEC_IPUC_ND}
};

int32
ctc_app_get_mem_profile(uint8        lchip, char* mem_buff, ctc_ftm_profile_info_t* p_mem_config)
{
    cJSON* pJson = NULL;
    cJSON* p_json = NULL;
    cJSON* p_tmp_json = NULL;
    ctc_ftm_misc_info_t* p_misc_info = &(p_mem_config->misc_info);
    ctc_ftm_key_info_t* p_tcam_key = p_mem_config->key_info;
    ctc_ftm_tbl_info_t* p_tbl = p_mem_config->tbl_info;
    uint32 cnt = 0;
    uint32 i = 0;
    uint32 tcam_arry = 0;
    uint32 tbl_arry = 0;
    uint32 flag = 0;
    uint32  tbl_index = 0;
    uint32  key_index = 0;
    ctc_key_name_size_pair_t* p_key_pair = NULL;
    ctc_key_name_value_pair_t* p_tbl_pair = NULL;

    if(ctc_json_parse((const char *)mem_buff, &pJson))
    {
        return CTC_ERROR;
    }
    CTC_SAI_LOG_DEBUG(SAI_API_SWITCH, "Use json mem_profile to initialize \n");
    p_json = ctc_json_get_object(pJson, "mem_profile");
    if(p_json && p_json->type == APP_JSON_TYPE_ARRAY)
    {
        lchip = p_json->array_len > lchip ? lchip : 0;
        p_json = ctc_json_get_array_item(p_json, lchip);
    }
    else
    {
        ctc_json_free(pJson);
        return CTC_ERROR;
    }
    p_mem_config->flag = flag;
    GET_PARSE_CFG_OBJ(p_misc_info, global);
        GET_PARSE_CFG_VALUE(p_misc_info, mcast_group_number);
        GET_PARSE_CFG_VALUE(p_misc_info, glb_nexthop_number);
        GET_PARSE_CFG_VALUE(p_misc_info, ip_route_mode);
        GET_PARSE_CFG_VALUE(p_mem_config, version);
        //GET_PARSE_CFG_ARRAY(p_misc_info, profile_specs);
        GET_PARSE_CFG_OBJ(p_misc_info, profile_specs);
            for(i = 0; i < sizeof(ftm_specs_pair)/sizeof(ctc_key_name_value_pair_t); i++)
            {
                p_tmp_json = ctc_json_get_object(p_json, ftm_specs_pair[i].key_name);
                if(p_tmp_json && p_tmp_json->type == APP_JSON_TYPE_NUMBER)
                {
                    p_misc_info->profile_specs[ftm_specs_pair[i].key_value] = p_tmp_json->value.number;
                }
            }
        END_PARSE_CFG_OBJ();
    END_PARSE_CFG_OBJ();

    p_key_pair = ctc_app_get_ftm_tcam_pair(&tcam_arry);
    GET_PARSE_CFG_OBJ(p_tcam_key, tcam)
        for(cnt = 0; cnt < (tcam_arry-1); ++cnt)
        {
            cJSON* p_arr_json = ctc_json_get_object(p_json, p_key_pair[cnt].key_name);
            uint8 array_size = 0;
            if(!p_arr_json || p_arr_json->type != APP_JSON_TYPE_ARRAY)
            {
                continue;
            }
            array_size = p_arr_json->array_len;
            for(i = 0; i < array_size; i++)
            {
                cJSON* p_json = ctc_json_get_array_item(p_arr_json, i);
                GET_PARSE_TCAM_KEY_INFO(p_tcam_key);
            }
            p_tcam_key->key_id= p_key_pair[cnt].key_value;
            p_tcam_key->key_size = p_key_pair[cnt].key_size;
            p_tcam_key->key_media = 0;
            p_tcam_key->max_key_index = p_tcam_key->tcam_entry_num[0];
            p_tcam_key++;
            key_index++;
        }
    END_PARSE_CFG_OBJ();
    p_mem_config->key_info_size = key_index;

    p_tbl_pair = ctc_app_get_ftm_tbl_pair(&tbl_arry);
    GET_PARSE_CFG_OBJ(p_tbl, sram)
        for(cnt = 0; cnt < (tbl_arry-1); ++cnt)
        {
            cJSON* p_arr_json = ctc_json_get_object(p_json, p_tbl_pair[cnt].key_name);
            uint8 array_size = 0;
            if(!p_arr_json || p_arr_json->type != APP_JSON_TYPE_ARRAY)
            {
                continue;
            }
            array_size = p_arr_json->array_len;
            for(i = 0; i < array_size; i++)
            {
                cJSON* p_json = ctc_json_get_array_item(p_arr_json, i);
                GET_PARSE_SRAM_TBL_INFO(p_tbl);
            }
            p_tbl->tbl_id= p_tbl_pair[cnt].key_value;
            p_tbl++;
            tbl_index++;
        }
    END_PARSE_CFG_OBJ();
    p_mem_config->tbl_info_size = tbl_index;

    ctc_json_free(pJson);
    return CTC_E_NONE;
}



