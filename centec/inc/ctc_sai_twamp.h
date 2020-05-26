/**
 @file ctc_sai_twamp.h

  @author  Copyright (C) 2020 Centec Networks Inc.  All rights reserved.

 @date 2020-05-20

 @version v2.0

\p
This module defines SAI TWAMP.
\b

\p
 The TWAMP Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_twamp_session                                 |            CTC7132             |
\t  |  remove_twamp_session                                 |            CTC7132             |
\t  |  set_twamp_session_attribute                          |            CTC7132             |
\t  |  get_twamp_session_attribute                          |            CTC7132             |
\t  |  get_twamp_session_stats                              |            CTC7132             |
\t  |  clear_twamp_session_stats                            |            CTC7132             |
\b

\p
 The TWAMP attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_TWAMP_SESSION_ATTR_TYPE                          |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_PORT                          |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_SESSION_ROLE                  |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT                  |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT                  |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_SRC_IP                        |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_DST_IP                        |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TC                            |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTE             |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE      |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT       |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID               |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_PADDING_LENGTH                |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_STATE                         |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_AUTH_MODE                     |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID                   |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD                 |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TX_RATE                       |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT                    |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION               |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_MODE                          |            CTC7132             |
\b

*/


#ifndef _CTC_SAI_TWAMP_H
#define _CTC_SAI_TWAMP_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"

#define TWAMP_ACL_GLOBAL_GROUP         (1030)

#define TWAMP_ACL_ENTRY_ID_BASE_INDEX   1
#define TWAMP_IPV4_RECEIVE_ACL_ENTRY_ID 1
#define TWAMP_IPV6_RECEIVE_ACL_ENTRY_ID 2

#define TWAMP_ADD_MEP_KEY_VLAN_ID   4000
#define TWAMP_ADD_MEP_ID   10
#define TWAMP_OAM_CCM_INTERVAL 1
#define TWAMP_FIXED_FRAME_SIZE 256


typedef ctc_acl_entry_t twamp_acl_param_t;
typedef ctc_stats_statsid_t twamp_stats_param_t;


typedef struct sai_twamp_common_stats_s
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
} sai_twamp_common_stats_t;

typedef struct ctc_sai_twamp_attr_s
{
    sai_object_id_t port_id;
    uint32      direction;
    uint32      role;
    uint32      udp_dst_port;
    uint32      udp_src_port;
    sai_ip_address_t dst_ip;
    sai_ip_address_t src_ip;
    uint32      priority;
    uint32      vrf_id;  // for hw lookup with vrf + ipda;
    uint32      encap_type;
    bool        trans_enable;
    bool        hw_lookup;
    uint32      padding_length;
    uint32      session_state;
    uint32      auth_mode;
    uint32      period;
    uint32      tx_rate;
    uint32      pkt_cnt;
    uint32      pkt_duration;
    uint32      session_mode;
    uint32      timestamp_format;
    uint32      iloop_port;
    uint32      l3if_id;
    uint32      nexthop_id;
    uint32_t    acl_entry_id;
    uint32_t    acl_stats_id;
    mac_addr_t  bridge_mac;
    uint32      lmep_index;
    uint32      mep_type;
    ctc_oam_maid_t maid;
    char  md_name[128];
    char  ma_name[128];
} ctc_sai_twamp_attr_t;


typedef struct ctc_sai_twamp_s
{
    sai_object_id_t session_id;
    ctc_sai_twamp_attr_t session_attr;
    sai_twamp_common_stats_t session_stats; 
} ctc_sai_twamp_t;


extern sai_status_t
ctc_sai_twamp_api_init();

extern sai_status_t
ctc_sai_twamp_db_init(uint8 lchip);

#endif /*_CTC_SAI_TWAMP_H*/

