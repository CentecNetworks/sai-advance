#include "sal.h"
#include "api/include/ctc_api.h"
#include "ctc_sai_app_cfg_ftm_profile.h"
#include "ctc_sai_app_cfg_parse.h"

#define KEY_TCAM_NUM    27
ctc_key_name_size_pair_t g_key_pair[] =
{
    {(char*)"SCL0_160",CTC_FTM_KEY_TYPE_SCL0,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"SCL0_320",CTC_FTM_KEY_TYPE_SCL0,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"SCL0_640",CTC_FTM_KEY_TYPE_SCL0,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"SCL1_160",CTC_FTM_KEY_TYPE_SCL1,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"SCL1_320",CTC_FTM_KEY_TYPE_SCL1,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"SCL1_640",CTC_FTM_KEY_TYPE_SCL1,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"SCL2_160",CTC_FTM_KEY_TYPE_SCL2,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"SCL2_320",CTC_FTM_KEY_TYPE_SCL2,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"SCL2_640",CTC_FTM_KEY_TYPE_SCL2,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"SCL3_160",CTC_FTM_KEY_TYPE_SCL3,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"SCL3_320",CTC_FTM_KEY_TYPE_SCL3,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"SCL3_640",CTC_FTM_KEY_TYPE_SCL3,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL0_IPE_160",CTC_FTM_KEY_TYPE_ACL0,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL0_IPE_320",CTC_FTM_KEY_TYPE_ACL0,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL0_IPE_640",CTC_FTM_KEY_TYPE_ACL0,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL1_IPE_160",CTC_FTM_KEY_TYPE_ACL1,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL1_IPE_320",CTC_FTM_KEY_TYPE_ACL1,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL1_IPE_640",CTC_FTM_KEY_TYPE_ACL1,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL2_IPE_160",CTC_FTM_KEY_TYPE_ACL2,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL2_IPE_320",CTC_FTM_KEY_TYPE_ACL2,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL2_IPE_640",CTC_FTM_KEY_TYPE_ACL2,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL3_IPE_160",CTC_FTM_KEY_TYPE_ACL3,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL3_IPE_320",CTC_FTM_KEY_TYPE_ACL3,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL3_IPE_640",CTC_FTM_KEY_TYPE_ACL3,CTC_FTM_KEY_SIZE_640_BIT},

    {(char*)"ACL4_IPE_160",CTC_FTM_KEY_TYPE_ACL4,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL4_IPE_320",CTC_FTM_KEY_TYPE_ACL4,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL4_IPE_640",CTC_FTM_KEY_TYPE_ACL4,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL5_IPE_160",CTC_FTM_KEY_TYPE_ACL5,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL5_IPE_320",CTC_FTM_KEY_TYPE_ACL5,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL5_IPE_640",CTC_FTM_KEY_TYPE_ACL5,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL6_IPE_160",CTC_FTM_KEY_TYPE_ACL6,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL6_IPE_320",CTC_FTM_KEY_TYPE_ACL6,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL6_IPE_640",CTC_FTM_KEY_TYPE_ACL6,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL7_IPE_160",CTC_FTM_KEY_TYPE_ACL7,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL7_IPE_320",CTC_FTM_KEY_TYPE_ACL7,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL7_IPE_640",CTC_FTM_KEY_TYPE_ACL7,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL8_IPE_160",CTC_FTM_KEY_TYPE_ACL8,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL9_IPE_160",CTC_FTM_KEY_TYPE_ACL9,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL10_IPE_160",CTC_FTM_KEY_TYPE_ACL10,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL11_IPE_160",CTC_FTM_KEY_TYPE_ACL11,CTC_FTM_KEY_SIZE_160_BIT},

    {(char*)"ACL0_EPE_160",CTC_FTM_KEY_TYPE_ACL0_EGRESS,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL0_EPE_320",CTC_FTM_KEY_TYPE_ACL0_EGRESS,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL0_EPE_640",CTC_FTM_KEY_TYPE_ACL0_EGRESS,CTC_FTM_KEY_SIZE_640_BIT},

    {(char*)"ACL1_EPE_160",CTC_FTM_KEY_TYPE_ACL1_EGRESS,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL1_EPE_320",CTC_FTM_KEY_TYPE_ACL1_EGRESS,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL1_EPE_640",CTC_FTM_KEY_TYPE_ACL1_EGRESS,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL2_EPE_160",CTC_FTM_KEY_TYPE_ACL2_EGRESS,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"ACL2_EPE_320",CTC_FTM_KEY_TYPE_ACL2_EGRESS,CTC_FTM_KEY_SIZE_320_BIT},
    {(char*)"ACL2_EPE_640",CTC_FTM_KEY_TYPE_ACL2_EGRESS,CTC_FTM_KEY_SIZE_640_BIT},
    {(char*)"ACL3_EPE_160",CTC_FTM_KEY_TYPE_ACL3_EGRESS,CTC_FTM_KEY_SIZE_160_BIT},
    {(char*)"IPV6_UCAST_HALF_KEY", CTC_FTM_KEY_TYPE_IPV6_UCAST_HALF,             CTC_FTM_KEY_SIZE_INVALID},


    {(char*)"LPM0_40",CTC_FTM_KEY_TYPE_IPV4_UCAST,CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"LPM0_160",CTC_FTM_KEY_TYPE_IPV6_UCAST,CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"LPM1_3",CTC_FTM_KEY_TYPE_IPV4_NAT,CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"LPM1_4",CTC_FTM_KEY_TYPE_IPV6_NAT,CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"LPM1_1",CTC_FTM_KEY_TYPE_IPV4_PBR,CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"LPM1_2",CTC_FTM_KEY_TYPE_IPV6_PBR,CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_IPV6_KEY0",        CTC_FTM_KEY_TYPE_IPV6_ACL0,  CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_IPV6_KEY1",        CTC_FTM_KEY_TYPE_IPV6_ACL1,  CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_MAC_KEY0",         CTC_FTM_KEY_TYPE_ACL0,       CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_MAC_KEY1",         CTC_FTM_KEY_TYPE_ACL1,       CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_MAC_KEY2",         CTC_FTM_KEY_TYPE_ACL2,       CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_MAC_KEY3",         CTC_FTM_KEY_TYPE_ACL3,       CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_EPE_IPV6_KEY0",    CTC_FTM_KEY_TYPE_IPV6_ACL0_EGRESS,  CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_EPE_IPV6_KEY1",    CTC_FTM_KEY_TYPE_IPV6_ACL1_EGRESS,  CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_EPE_MAC_KEY0",     CTC_FTM_KEY_TYPE_ACL0_EGRESS,       CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_EPE_MAC_KEY1",     CTC_FTM_KEY_TYPE_ACL1_EGRESS,       CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_EPE_MAC_KEY2",     CTC_FTM_KEY_TYPE_ACL2_EGRESS,       CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"ACL_EPE_MAC_KEY3",     CTC_FTM_KEY_TYPE_ACL3_EGRESS,       CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"MAC_KEY",              CTC_FTM_KEY_TYPE_FDB,        CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV4_UCAST_ROUTE_KEY", CTC_FTM_KEY_TYPE_IPV4_UCAST, CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV4_MCAST_ROUTE_KEY", CTC_FTM_KEY_TYPE_IPV4_MCAST, CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV6_UCAST_ROUTE_KEY", CTC_FTM_KEY_TYPE_IPV6_UCAST, CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV6_MCAST_ROUTE_KEY", CTC_FTM_KEY_TYPE_IPV6_MCAST, CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV4_NAT_KEY",         CTC_FTM_KEY_TYPE_IPV4_NAT,   CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV6_NAT_KEY",         CTC_FTM_KEY_TYPE_IPV6_NAT,   CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV4_PBR_KEY",         CTC_FTM_KEY_TYPE_IPV4_PBR,   CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV6_PBR_KEY",         CTC_FTM_KEY_TYPE_IPV6_PBR,   CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"MAC_SCL_KEY",          CTC_FTM_KEY_TYPE_MAC_SCL,    CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV4_SCL_KEY",         CTC_FTM_KEY_TYPE_IPV4_SCL,   CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV6_SCL_KEY",         CTC_FTM_KEY_TYPE_IPV6_SCL,   CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"VLAN_SCL_KEY",         CTC_FTM_KEY_TYPE_VLAN_SCL,   CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV4_TUNNEL_KEY",      CTC_FTM_KEY_TYPE_IPV4_TUNNEL,CTC_FTM_KEY_SIZE_INVALID},
    {(char*)"IPV6_TUNNEL_KEY",      CTC_FTM_KEY_TYPE_IPV6_TUNNEL,CTC_FTM_KEY_SIZE_INVALID},
    {NULL, 0}
};

ctc_key_name_value_pair_t g_tbl_entry_num[] =
{
        {"", CTC_FTM_SPEC_INVALID},
        {"MAC", CTC_FTM_SPEC_MAC},
        {"IP_HOST", CTC_FTM_SPEC_IPUC_HOST},
        {"IP_LPM", CTC_FTM_SPEC_IPUC_LPM},
        {"IPMC", CTC_FTM_SPEC_IPMC},
        {"ACL", CTC_FTM_SPEC_ACL},
        {"Scl_Flow", CTC_FTM_SPEC_SCL_FLOW},
        {"Acl_Flow", CTC_FTM_SPEC_ACL_FLOW},
        {"Oam", CTC_FTM_SPEC_OAM},
        {"Scl", CTC_FTM_SPEC_SCL},
        {"Tunnel_Decp", CTC_FTM_SPEC_TUNNEL},
        {"Mpls", CTC_FTM_SPEC_MPLS},
        {"L2Mcast", CTC_FTM_SPEC_L2MC},
        {"Ipfix", CTC_FTM_SPEC_IPFIX},
        {"NAPT", CTC_FTM_SPEC_NAPT},
        {"Vlan_Xlate", CTC_FTM_SPEC_VLAN_XLATE},
        {"", CTC_FTM_SPEC_MAX}
};

#define SRAM_TBL_NUM    19
ctc_key_name_value_pair_t g_tbl_pair[] =
{
    {(char*)"LPM_PIPE0"     , CTC_FTM_TBL_TYPE_LPM_PIPE0,},
    {(char*)"LPM_PIPE1"     , CTC_FTM_TBL_TYPE_LPM_PIPE1,},
    {(char*)"NEXTHOP"       , CTC_FTM_TBL_TYPE_NEXTHOP  ,},
    {(char*)"FWD"           , CTC_FTM_TBL_TYPE_FWD      ,},
    {(char*)"MET"           , CTC_FTM_TBL_TYPE_MET      ,},
    {(char*)"EDIT"          , CTC_FTM_TBL_TYPE_EDIT     ,},
    {(char*)"OAM_MEP"       , CTC_FTM_TBL_TYPE_OAM_MEP  ,},
    {(char*)"STATS"         , CTC_FTM_TBL_TYPE_STATS    ,},
    {(char*)"LM"            , CTC_FTM_TBL_TYPE_LM       ,},
    {(char*)"SCL_HASH_KEY" , CTC_FTM_TBL_TYPE_SCL_HASH_KEY ,},
    {(char*)"SCL_HASH_AD"   , CTC_FTM_TBL_TYPE_SCL_HASH_AD  ,},
    {(char*)"SCL1_HASH_KEY" , CTC_FTM_TBL_TYPE_SCL1_HASH_KEY ,},
    {(char*)"SCL1_HASH_AD"   , CTC_FTM_TBL_TYPE_SCL1_HASH_AD  ,},
    {(char*)"FIB0_HASH_KEY" , CTC_FTM_TBL_TYPE_FIB0_HASH_KEY,},
    {(char*)"DSMAC_AD"      , CTC_FTM_TBL_TYPE_DSMAC_AD ,},
    {(char*)"FIB1_HASH_KEY" , CTC_FTM_TBL_TYPE_FIB1_HASH_KEY  ,},
    {(char*)"DSIP_AD"       , CTC_FTM_TBL_TYPE_DSIP_AD        ,},
    {(char*)"XCOAM_HASH_KEY", CTC_FTM_TBL_TYPE_XCOAM_HASH_KEY ,},
    {(char*)"FLOW_HASH_KEY" , CTC_FTM_TBL_TYPE_FLOW_HASH_KEY  ,},
    {(char*)"FLOW_AD"       , CTC_FTM_TBL_TYPE_FLOW_AD        ,},
    {(char*)"IPFIX_HASH_KEY", CTC_FTM_TBL_TYPE_IPFIX_HASH_KEY ,},
    {(char*)"IPFIX_AD"      , CTC_FTM_TBL_TYPE_IPFIX_AD       ,},
    {(char*)"OAM_APS"       , CTC_FTM_TBL_TYPE_OAM_APS        ,},
    {(char*)"FIB_HASH_AD",          CTC_FTM_TBL_TYPE_FIB_HASH_AD},
    {(char*)"LPM_LKP_KEY1",         CTC_FTM_TBL_TYPE_LPM_PIPE1},
    {(char*)"LPM_LKP_KEY2",         CTC_FTM_TBL_TYPE_LPM_PIPE2},
    {(char*)"LPM_LKP_KEY0",         CTC_FTM_TBL_TYPE_LPM_PIPE0},
    {(char*)"LPM_LKP_KEY3",         CTC_FTM_TBL_TYPE_LPM_PIPE3},
    {(char*)"LPM_HASH_KEY",         CTC_FTM_TBL_TYPE_LPM_HASH_KEY},
    {(char*)"FIB_HASH_KEY",         CTC_FTM_TBL_TYPE_FIB_HASH_KEY},
    {(char*)"MPLS",                 CTC_FTM_TBL_TYPE_MPLS},
    {(char*)"LM_STATS",             CTC_FTM_TBL_TYPE_LM},
    {(char*)"L2_EDIT",             CTC_FTM_TBL_TYPE_L2_EDIT},
    {(char*)"ANT_FLOW",             CTC_FTM_TBL_TYPE_ANT_FLOW},
    {(char*)"ANT_FLOW2",             CTC_FTM_TBL_TYPE_ANT_FLOW2},
    {(char*)"MPLS_AD",             CTC_FTM_TBL_TYPE_MPLS_AD},
    {(char*)"GEM_LOOKUP_KEY",             CTC_FTM_TBL_TYPE_GEM_LKUP_KEY},

    {(char*)"EGRESS_SCL0",             CTC_FTM_TBL_TYPE_EGR_SCL0},
    {(char*)"EGRESS_SCL1",             CTC_FTM_TBL_TYPE_EGR_SCL1},
    {NULL, 0},
};

#define FTM_PROFILE_RESULT_NUM  12

/*--------------------------------Define--------------------------------------*/

int32
ctc_app_read_ftm_profile_global_info(ctc_app_parse_file_t* pfile,
                        ctc_ftm_profile_info_t* profile_info)
{
    uint8  result_num = 0;
    int32 result = 0;
    const char* field_sub = NULL;

    result_num = 1;
    ctc_app_parse_file(pfile,
                   "GLB_MULT_GRP_NUM",
                   field_sub,
                   &profile_info->misc_info.mcast_group_number,
                   &result_num);

    result_num = 1;
    ctc_app_parse_file(pfile,
                   "GLB_NH_TBL_SIZE",
                   field_sub,
                   &profile_info->misc_info.glb_nexthop_number,
                   &result_num);

    result_num = 1;
    ctc_app_parse_file(pfile,
                   "VSI_NUM",
                   field_sub,
                   &result,
                   &result_num);
    profile_info->misc_info.vsi_number = (int16)result;

    result_num = 1;
    ctc_app_parse_file(pfile,
                   "ECMP_NUM",
                   field_sub,
                   &result,
                   &result_num);

    profile_info->misc_info.ecmp_number = (int16)result;

    result_num = 1;
    result = 0;
    ctc_app_parse_file(pfile,
                   "COUPLE_MODE",
                   field_sub,
                   &result,
                   &result_num);
    if (result)
    {
        CTC_SET_FLAG(profile_info->flag, CTC_FTM_FLAG_COUPLE_EN);
    }


    result_num = 1;
    ctc_app_parse_file(pfile,
                   "IP_ROUTE_MODE",
                   field_sub,
                   &result,
                   &result_num);
    profile_info->misc_info.ip_route_mode= (int16)result;


    result_num = 1;
    ctc_app_parse_file(pfile,
                   "SCL_MODE",
                   field_sub,
                   &result,
                   &result_num);
    profile_info->misc_info.scl_mode= (int16)result;


    return CTC_E_NONE;
}

int32
ctc_app_read_ftm_profile_tbl_info(ctc_app_parse_file_t* pfile,
                        ctc_ftm_profile_info_t* profile_info)
{
    uint32  count = 0;
    uint32  inner_count = 0;
    int32   ret;
    uint32  tbl_index = 0;
    int32   arr_entry_size[FTM_PROFILE_RESULT_NUM];
    int32   arr_mem_tbl_id[FTM_PROFILE_RESULT_NUM];
    int32   arr_entry_off[FTM_PROFILE_RESULT_NUM];
    uint8   result_num = 0;
    ctc_ftm_tbl_info_t * p_tbl_info = NULL;

    for(count = 0; count < sizeof(g_tbl_pair)/sizeof(g_tbl_pair[0]); ++count)
    {
        sal_memset(arr_entry_size, 0, sizeof(arr_entry_size));
        sal_memset(arr_mem_tbl_id, 0, sizeof(arr_mem_tbl_id));
        sal_memset(arr_entry_off, 0, sizeof(arr_entry_off));
        result_num = FTM_PROFILE_RESULT_NUM;
        ret = ctc_app_parse_file(pfile,
                       g_tbl_pair[count].key_name,
                       "ENTRY_SIZE",
                       arr_entry_size,
                       &result_num);
        if ((CTC_E_NONE != ret))
        {
            continue;
        }
        ret = ctc_app_parse_file(pfile,
                       g_tbl_pair[count].key_name,
                       "ENTRY_OFFSET",
                       arr_entry_off,
                       &result_num);
        ret = ctc_app_parse_file(pfile,
                       g_tbl_pair[count].key_name,
                       "TBL_MEM_ID",
                       arr_mem_tbl_id,
                       &result_num);
        p_tbl_info = &profile_info->tbl_info[tbl_index];
        p_tbl_info->tbl_id = g_tbl_pair[count].key_value;
        for(inner_count = 0; inner_count < result_num; ++inner_count)
        {
            if(arr_mem_tbl_id[inner_count] >= 32)
            {
                CTC_BIT_SET(p_tbl_info->mem_high_bitmap, (arr_mem_tbl_id[inner_count]-32));
            }
            else
            {
                CTC_BIT_SET(p_tbl_info->mem_bitmap, arr_mem_tbl_id[inner_count]);
            }
            p_tbl_info->mem_entry_num[arr_mem_tbl_id[inner_count]] = arr_entry_size[inner_count];
            p_tbl_info->mem_start_offset[arr_mem_tbl_id[inner_count]] = arr_entry_off[inner_count];
        }
        ++tbl_index;

    }
    profile_info->tbl_info_size = tbl_index;
    return CTC_E_NONE;
}

int32
ctc_app_read_ftm_profile_tcam_info(ctc_app_parse_file_t* pfile,
                        ctc_ftm_profile_info_t* profile_info)
{
    uint32  count = 0;
    uint32  inner_count = 0;
    int32   ret;
    uint32  key_index = 0;
    int32   arr_entry_size[FTM_PROFILE_RESULT_NUM];
    int32   arr_mem_tbl_id[FTM_PROFILE_RESULT_NUM];
    int32   arr_entry_off[FTM_PROFILE_RESULT_NUM];
    int32   arr_entry_key_size[FTM_PROFILE_RESULT_NUM];
    uint8   result_num = 0;
    uint8   mem_loop = 0;
    int32   total_size = 0;
    ctc_ftm_key_info_t * p_key_info = NULL;

    for(count = 0; count < sizeof(g_key_pair)/sizeof(g_key_pair[0]); ++count)
    {
        sal_memset(arr_entry_size, 0, sizeof(arr_entry_size));
        sal_memset(arr_mem_tbl_id, 0, sizeof(arr_mem_tbl_id));
        sal_memset(arr_entry_off, 0, sizeof(arr_entry_off));
        sal_memset(arr_entry_key_size, 0, sizeof(arr_entry_key_size));
        result_num = FTM_PROFILE_RESULT_NUM;
        ret = ctc_app_parse_file(pfile,
                       g_key_pair[count].key_name,
                       "ENTRY_SIZE",
                       arr_entry_size,
                       &result_num);
        if ((CTC_E_NONE != ret))
        {
            continue;
        }
        ret = ctc_app_parse_file(pfile,
                       g_key_pair[count].key_name,
                       "ENTRY_OFFSET",
                       arr_entry_off,
                       &result_num);
        ret = ctc_app_parse_file(pfile,
                       g_key_pair[count].key_name,
                       "TBL_MEM_ID",
                       arr_mem_tbl_id,
                       &result_num);

        mem_loop = result_num;

        ret = ctc_app_parse_file(pfile,
                       g_key_pair[count].key_name,
                       "KEY_SIZE",
                       arr_entry_key_size,
                       &result_num);
        p_key_info = &profile_info->key_info[key_index];
        p_key_info->key_id= g_key_pair[count].key_value;

        if((CTC_E_NONE == ret) && (0 != result_num))
        {
            p_key_info->key_size = arr_entry_key_size[0];
        }
        else
        {
            p_key_info->key_size = g_key_pair[count].key_size;
        }

        p_key_info->key_media = 0;
        p_key_info->max_key_index = arr_entry_size[0];

        for(inner_count = 0; inner_count < mem_loop; ++inner_count)
        {
            CTC_BIT_SET(p_key_info->tcam_bitmap, arr_mem_tbl_id[inner_count]);
            p_key_info->tcam_entry_num[arr_mem_tbl_id[inner_count]] = arr_entry_size[inner_count];
            p_key_info->tcam_start_offset[arr_mem_tbl_id[inner_count]] = arr_entry_off[inner_count];
            total_size = total_size + arr_entry_size[inner_count];
        }
        ++key_index;
    }

    profile_info->key_info_size = key_index;

    return CTC_E_NONE;
}

int32
ctc_app_read_ftm_profile_spcecs(ctc_app_parse_file_t* pfile,
                        ctc_ftm_profile_info_t* profile_info)
{
    uint8 i = 0;
    uint8 result_num = 0;

    for(i = 0; i < CTC_FTM_SPEC_MAX; ++i)
    {
        result_num = 1;
        ctc_app_parse_file(pfile,
                   g_tbl_entry_num[i].key_name,
                   NULL,
                   &profile_info->misc_info.profile_specs[g_tbl_entry_num[i].key_value],
                   &result_num);
    }

    return CTC_E_NONE;
}

int32
ctc_app_read_ftm_profile(const int8* file_name,
                     ctc_ftm_profile_info_t* profile_info)
{
    int32   ret;
    ctc_app_parse_file_t file;

    CTC_PTR_VALID_CHECK(file_name);
    CTC_PTR_VALID_CHECK(profile_info);

    ret = ctc_app_parse_open_file((const char*)file_name, &file);
    if (ret != CTC_E_NONE)
    {
        return ret;
    }

    ctc_app_read_ftm_profile_global_info(&file, profile_info);

    ctc_app_read_ftm_profile_tbl_info(&file, profile_info);

    ctc_app_read_ftm_profile_tcam_info(&file, profile_info);

    ctc_app_read_ftm_profile_spcecs(&file, profile_info);

    ctc_app_parse_close_file(&file);
    return CTC_E_NONE;
}


