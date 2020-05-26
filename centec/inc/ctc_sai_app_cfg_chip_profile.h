/**
 @file ctc_app_cfg_chip_profile.h

 @author  Copyright (C) 2011 Centec Networks Inc.  All rights reserved.

 @date 2010-7-5

 @version v2.0

  This file contains chip profile related data structure.
*/

#ifndef _CTC_APP_CFG_CHIP_PROFILE_H
#define _CTC_APP_CFG_CHIP_PROFILE_H
#ifdef __cplusplus
extern "C" {
#endif
#include "ctc_const.h"
#include "ctc_init.h"





struct ctc_phy_info_s
{
    uint8 mdio_bus;
    uint8 phy_addr;
};
typedef struct ctc_phy_info_s ctc_phy_info_t;

struct ctc_init_chip_info_s
{
    uint8 gchip[CTC_MAX_LOCAL_CHIP_NUM];
    uint8 local_chip_num;

    uint8 queue_num_per_network_port;
    uint8 queue_num_per_static_int_port;
    uint8 queue_num_per_fabric;
    uint8 max_internal_port_id;

    uint8 queue_num_per_internal_port;
    uint8 queue_num_per_ingress_service;
    uint8 queue_num_per_egress_service;

    uint8 profile_type;
    uint8 nh_dedit_mode;
    uint8 fdb_hw_learning_mode;

    uint16 policer_num;
    uint16 ingress_vlan_policer_num;
    uint16 egress_vlan_policer_num;
    uint32 logic_port_num;

    uint32 ext_nexthop_num;
    uint16 mpls_tunnel_num;
    uint32 mpls_entry_num[4];

    uint8 stats_queue_deq_en;
    uint8 stats_queue_drop_en;
    uint8 stats_flow_policer_en;
    uint8 stats_vlan_en;
    uint8 stats_port_en;
    uint8 stats_ecmp_en;

    uint8 stats_vrf_en;
    uint8 port_phy_mapping_en;
    uint8 cut_through_speed;
    uint8 bfd_vccv_with_ip_en;

    uint16 bfd_mep_num;
    uint16 stats_policer_num;
    uint16 max_fid_num;
    uint16 rsv_1;

    uint8 interrupt_mode;
    uint8  bpe_br_pe_en;
    uint16 bpe_br_port_base;

    uint16 bpe_br_uc_max_ecid;
    uint16 bpe_br_mc_max_ecid;

    uint16 cpu_port;
    uint8 cpu_port_en;
    uint8 ecc_recover_en;

    uint8 tcam_scan_en;
    uint8 queue_num_for_cpu_reason;
    uint8 cpu_que_shp_profile_num;
    uint8 stp_mode;
    uint8 fabric_mode;
    uint8 stacking_version;
    uint8 stacking_mode;
    uint8 trie_sort_en;
    uint8 lag_gb_gg_interconnect_en;
    uint8 rsv;

    uint32 init_flag;
    uint32 cut_through_bitmap;
};
typedef struct ctc_init_chip_info_s ctc_init_chip_info_t;

extern int32
ctc_app_get_chip_profile(uint8* fname, ctc_init_cfg_t * p_init_config, ctc_init_chip_info_t* p_chip_info);


extern int32
ctc_app_set_phy_mapping(uint8* fname, ctc_init_cfg_t * p_init_config, ctc_init_chip_info_t* p_chip_info);

#ifdef __cplusplus
}
#endif

#endif

