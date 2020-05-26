#ifndef _CTC_SAI_NPM_H
#define _CTC_SAI_NPM_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"

#define NPM_ACL_GLOBAL_GROUP         (1030)

#define NPM_ACL_ENTRY_ID_BASE_INDEX   1
#define NPM_IPV4_RECEIVE_ACL_ENTRY_ID 1
#define NPM_IPV6_RECEIVE_ACL_ENTRY_ID 2

#define NPM_ADD_MEP_KEY_VLAN_ID   4000
#define NPM_ADD_MEP_ID   10
#define NPM_OAM_CCM_INTERVAL 1
#define NPM_FIXED_FRAME_SIZE 256


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

typedef struct ctc_sai_npm_attr_s
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
} ctc_sai_npm_attr_t;


typedef struct ctc_sai_npm_s
{
    sai_object_id_t session_id;
    ctc_sai_npm_attr_t session_attr;
    sai_npm_common_stats_t session_stats; 
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


extern sai_status_t
ctc_sai_npm_api_init();

extern sai_status_t
ctc_sai_npm_db_init(uint8 lchip);

#endif /*_CTC_SAI_NPM_H*/

