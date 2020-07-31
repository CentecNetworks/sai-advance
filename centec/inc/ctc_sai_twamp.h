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
\t  |   ATTRIBUTE                                        |       SUPPORT CHIPS LIST       |
\t  |  SAI_TWAMP_SESSION_ATTR_TWAMP_PORT                 |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT               |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_SESSION_ROLE               |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT               |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT               |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_SRC_IP                     |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_DST_IP                     |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TC                         |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TTL                        |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER         |            CTC7132             |  
\t  |  SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE   |            CTC7132             |        
\t  |  SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT    |            CTC7132             |       
\t  |  SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID            |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH              |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_AUTH_MODE                  |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID                |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TX_RATE                    |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_PKT_TX_MODE                |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION            |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT                 |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD              |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_MODE                       |            CTC7132             |
\t  |  SAI_TWAMP_SESSION_ATTR_TIMESTAMP_FORMAT           |            CTC7132             |
\b

*/


#ifndef _CTC_SAI_TWAMP_H
#define _CTC_SAI_TWAMP_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"


#define TWAMP_ADD_MEP_KEY_RESERVED_FID  4096
#define TWAMP_ADD_MEP_KEY_RESERVED_LEVEL  3
#define TWAMP_ADD_MEP_RESERVED_MEP_ID   10

#define TWAMP_OAM_CCM_INTERVAL 1

#define TWAMP_PORT_ACL_LOOKUP_PRIORITY 0

#define TWAMP_PACKET_BASE_LENGTH_IPV4 87
#define TWAMP_PACKET_BASE_LENGTH_IPV6 107


typedef ctc_acl_entry_t twamp_acl_param_t;

//typedef ctc_stats_statsid_t twamp_stats_param_t;


typedef struct ctc_sai_twamp_s
{
    sai_object_id_t port_id;
    uint32      role;
    sai_object_id_t receive_port_id;
    uint32      udp_dst_port;
    uint32      udp_src_port;
    sai_ip_address_t dst_ip;
    sai_ip_address_t src_ip;
    uint8      priority;
    uint8      ttl;
    sai_object_id_t vrf_oid;  // for hw lookup with vrf_id + ipda;
    uint32      encap_type;
    bool        trans_enable;
    bool        hw_lookup;
    uint32      packet_length;
    uint32      session_state;
    uint32      auth_mode;
    uint32      pkt_tx_mode;
    uint32      period;
    uint32      tx_rate;
    uint32      pkt_cnt;
    uint32      pkt_duration;
    uint32      session_mode;
    uint32      timestamp_format; // 0 means NTP, 1 means PTP
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
    uint32_t    oam_acl_entry_id;  // for acl match to oam engine   
    uint32_t    is_loop_swap_ip;
    uint32      lmep_index;
} ctc_sai_twamp_t;

sai_status_t
ctc_sai_twamp_acl_entry_id_alloc(uint32_t *acl_entry_id);

sai_status_t
ctc_sai_twamp_acl_entry_id_dealloc(uint32_t acl_entry_id);

sai_status_t
ctc_sai_twamp_acl_port_group_id_alloc(uint32_t gport_id, uint32_t *group_id);

sai_status_t
ctc_sai_twamp_acl_port_group_id_dealloc(uint32_t group_id);

extern sai_status_t
ctc_sai_twamp_api_init();

extern sai_status_t
ctc_sai_twamp_db_init(uint8 lchip);

#endif /*_CTC_SAI_TWAMP_H*/

