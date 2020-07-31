/**
 @file ctc_sai_npm.h

 @author  Copyright (C) 2020 Centec Networks Inc.  All rights reserved.

 @date 2020-06-01

 @version v2.0


\p
This module defines SAI NPM.
\b
\p
 The NPM Module APIs supported by centec devices:
\p
\b
\t  |   API                                                |       SUPPORT CHIPS LIST       |
\t  |  create_npm_session                                  |            CTC7132             |
\t  |  remove_npm_session                                  |            CTC7132             |
\t  |  set_npm_session_attribute                           |            CTC7132             |
\t  |  get_npm_session_attribute                           |            CTC7132             |
\t  |  get_npm_session_stats                               |            CTC7132             |
\t  |  clear_npm_session_stats                             |            CTC7132             |
\b
\p
 The NPM attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_NPM_SESSION_ATTR_NPM_PORT                       |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_RECEIVE_PORT                   |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_COLOR_MODE                     |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_SESSION_ROLE                   |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_UDP_SRC_PORT                   |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_UDP_DST_PORT                   |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_SRC_IP                         |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_DST_IP                         |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_TC                             |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_TTL                            |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER             |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE         |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT        |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID                |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_PACKET_LENGTH                  |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_PKT_TX_MODE                    |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD                  |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_TX_RATE                        |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_TX_PKT_CNT                     |            CTC7132             |
\t  |  SAI_NPM_SESSION_ATTR_TX_PKT_DURATION                |            CTC7132             |
\b
\p
 The NPM Stats supported by centec devices:
\p
\b
\t  |   STATS TYPE                                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_NPM_SESSION_STATS_RX_PACKETS                     |            CTC7132             |
\t  |  SAI_NPM_SESSION_STATS_RX_BYTE                        |            CTC7132             |
\t  |  SAI_NPM_SESSION_STATS_TX_PACKETS                     |            CTC7132             |
\t  |  SAI_NPM_SESSION_STATS_TX_BYTE                        |            CTC7132             |
\t  |  SAI_NPM_SESSION_STATS_DROP_PACKETS                   |            CTC7132             |
\b
*/

#ifndef _CTC_SAI_NPM_H
#define _CTC_SAI_NPM_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"


#define NPM_ADD_MEP_KEY_RESERVED_FID        (4096 + 1)
#define NPM_ADD_MEP_KEY_RESERVED_LEVEL      (3 + 1)
#define NPM_ADD_MEP_RESERVED_MEP_ID         (10 + 1)

#define NPM_OAM_CCM_INTERVAL            1

#define NPM_PORT_ACL_LOOKUP_PRIORITY    0

#define NPM_PACKET_BASE_LENGTH_IPV4     87
#define NPM_PACKET_BASE_LENGTH_IPV6   107


#define NPM_LMEP_INDEX 0x1FF7

typedef ctc_acl_entry_t npm_acl_param_t;
typedef ctc_stats_statsid_t npm_stats_param_t;


typedef struct sai_npm_common_stats_s
{
    uint64  total_delay_all;
    uint64  tx_pkts_all;
    uint64  rx_pkts_all;
    uint64  max_delay;
    uint64  min_delay;
    uint64  max_jitter;
    uint64  min_jitter;
    uint64  total_jitter_all;
    uint64  disorder_pkts;
    uint8   is_ntp_ts;
} sai_npm_common_stats_t;

typedef struct ctc_sai_npm_s
{
    sai_object_id_t port_id;
    uint32      role;
    sai_object_id_t receive_port_id;
    uint32      color_mode;
    uint32      udp_dst_port;
    uint32      udp_src_port;
    sai_ip_address_t dst_ip;
    sai_ip_address_t src_ip;
    uint32      priority;
    uint8      ttl;
    sai_object_id_t vrf_oid;  // for hw lookup with vrf_id + ipda;
    uint32      encap_type;
    bool        trans_enable;
    bool        hw_lookup;
    uint32      packet_length;

    uint32      auth_mode;
    uint32      pkt_tx_mode;
    uint32      period;
    uint32      tx_rate;
    uint32      pkt_size;
    uint32      pkt_cnt;
    uint32      pkt_duration;
    uint32      session_mode;
    uint32      timestamp_format;
    uint32      nexthop_id;
    uint32_t    acl_entry_id;
    uint32_t    acl_stats_id;

//-------------------------------------
    uint32      oam_iloop_port;   // for reflector
    uint32      oam_eloop_port;   // for reflector 
    uint32      oam_l3if_id;      // for reflector
    uint32      oam_iloop_nh_id;  // for reflector
    uint32      oam_eloop_nh_id;  // for reflector   
    uint32      iloop_port;
    uint32      eloop_port;      
    uint32      l3if_id; 
    uint32      iloop_nexthop;     
    uint32      eloop_nexthop; 
    sai_object_id_t user_nh_id;     // for reflector     
    uint32_t    loop_acl_entry_id;  // just for reflector to chop header
    uint32_t    oam_acl_entry_id;  // for acl match to npm stats   
    uint32_t    is_loop_swap_ip;
    uint32      lmep_index;
    
} ctc_sai_npm_t;

#if 0
typedef struct ctc_sai_npm_s
{
    sai_object_id_t session_id;
    ctc_sai_npm_attr_t session_attr;
    //sai_npm_common_stats_t session_stats; 
    uint32      gport;
    uint8       continuous_ses_cnt;
    uint8       continuous_non_ses_cnt;
    uint64      ses_cnt;
    uint64      non_ses_cnt;
    uint8       flr_for_ses;
    uint64      max_rx_ir;
    uint64      min_rx_ir;
    uint64      seconds;
    uint8       in_avl_period;
    uint32      avl_period_thrd;
    uint64      avl_periods;
    uint64      unavl_periods;
    uint64      total_far_delay_all;
    uint64      tx_bytes_all;
    uint64      rx_bytes_all;
    uint32      last_disorder_pkts; 

} ctc_sai_npm_t;
#endif

sai_status_t
ctc_sai_npm_acl_entry_id_alloc(uint32_t *acl_entry_id);

sai_status_t
ctc_sai_npm_acl_entry_id_dealloc(uint32_t acl_entry_id);

extern sai_status_t
ctc_sai_npm_api_init();

extern sai_status_t
ctc_sai_npm_db_init(uint8 lchip);

#endif /*_CTC_SAI_NPM_H*/

