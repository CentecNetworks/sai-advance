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
\e  |  create_npm_session                                  |            CTC7132             |
\e  |  remove_npm_session                                  |            CTC7132             |
\e  |  set_npm_session_attribute                           |            CTC7132             |
\e  |  get_npm_session_attribute                           |            CTC7132             |
\e  |  get_npm_session_stats                               |            CTC7132             |
\e  |  clear_npm_session_stats                             |            CTC7132             |
\b
\p
 The NPM attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                     |       SUPPORT CHIPS LIST       |
\e  |  SAI_NPM_SESSION_ATTR_SESSION_ROLE              |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE    |            CTC7132             |    
\e  |  SAI_NPM_SESSION_ATTR_NPM_TEST_PORT             |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT          |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_SRC_MAC                   |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_DST_MAC                   |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_OUTER_VLANID              |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_INNER_VLANID              |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_SRC_IP                    |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_DST_IP                    |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_UDP_SRC_PORT              |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_UDP_DST_PORT              |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_TTL                       |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_TC                        |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT   |            CTC7132             |     
\e  |  SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER        |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID           |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_PACKET_LENGTH             |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_TX_RATE                   |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_PKT_TX_MODE               |            CTC7132             |  
\e  |  SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD             |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_TX_PKT_CNT                |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_TX_PKT_DURATION           |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_TIMESTAMP_OFFSET          |            CTC7132             |
\e  |  SAI_NPM_SESSION_ATTR_SEQUENCE_NUMBER_OFFSET    |            CTC7132             |
\b
\p
 The NPM Stats supported by centec devices:
\p
\b
\t  |   STATS TYPE                                       |       SUPPORT CHIPS LIST       |
\e  |  SAI_NPM_SESSION_STATS_RX_PACKETS                  |            CTC7132             | 
\e  |  SAI_NPM_SESSION_STATS_RX_BYTE                     |            CTC7132             |
\e  |  SAI_NPM_SESSION_STATS_TX_PACKETS                  |            CTC7132             | 
\e  |  SAI_NPM_SESSION_STATS_TX_BYTE                     |            CTC7132             |
\e  |  SAI_NPM_SESSION_STATS_DROP_PACKETS                |            CTC7132             |   
\e  |  SAI_NPM_SESSION_STATS_MAX_LATENCY                 |            CTC7132             |  
\e  |  SAI_NPM_SESSION_STATS_MIN_LATENCY                 |            CTC7132             |  
\e  |  SAI_NPM_SESSION_STATS_AVG_LATENCY                 |            CTC7132             |  
\e  |  SAI_NPM_SESSION_STATS_MAX_JITTER                  |            CTC7132             | 
\e  |  SAI_NPM_SESSION_STATS_MIN_JITTER                  |            CTC7132             | 
\e  |  SAI_NPM_SESSION_STATS_AVG_JITTER                  |            CTC7132             |    
\e  |  SAI_NPM_SESSION_STATS_MAX_IR                      |            CTC7132             |
\e  |  SAI_NPM_SESSION_STATS_MIN_IR                      |            CTC7132             |

\b
*/

#ifndef _CTC_SAI_NPM_H
#define _CTC_SAI_NPM_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"



#define NPM_PORT_ACL_LOOKUP_PRIORITY    0

#define NPM_PACKET_BASE_HEADER_LENGTH_IPV4   54
#define NPM_PACKET_BASE_HEADER_LENGTH_IPV6   74

#define NPM_PACKET_BASE_LENGTH_IPV4   87
#define NPM_PACKET_BASE_LENGTH_IPV6   107

#define NPM_LMEP_INDEX 0x1FF7


typedef ctc_acl_entry_t npm_acl_param_t;


typedef struct ctc_sai_npm_s
{

    uint8 session_id;
    
    sai_object_id_t test_port_oid;
    
    uint32      role;
        
    uint32 receive_port_bits[8];  
    uint32 receive_port_count; 

    sai_mac_t src_mac;
    sai_mac_t dst_mac;

    uint16 outer_vlan;
    uint16 inner_vlan;
    
    sai_ip_address_t dst_ip;
    sai_ip_address_t src_ip;

    uint32      udp_dst_port;
    uint32      udp_src_port;

    uint32     packet_offset;
    
    uint32      priority;
    uint8      ttl;
    sai_object_id_t vrf_oid;  
    uint32      encap_type;
    bool        trans_enable;
    bool        hw_lookup;
    uint32      packet_length;

    uint32      pkt_tx_mode;
    uint32      period;
    uint32      tx_rate;

    uint32      pkt_cnt;
    uint32      pkt_duration;
    
    uint8 ip_addr_family;

    uint32      l3if_id;         
    uint32      iloop_port;        
    uint32      iloop_nexthop;    

    uint32      eloop_port;     
    uint32      eloop_nexthop;   
    
    uint32    ingress_acl_entry_id; 

    uint32    egress_acl_entry_id; 

    uint32    is_swap_acl_key;

    uint16    ts_offset;
    uint16    seq_offset;
    uint8     ts_offset_set;
    uint8     seq_offset_set;        
} ctc_sai_npm_t;


sai_status_t
_ctc_sai_npm_acl_entry_id_alloc(uint8 lchip, uint32_t *acl_entry_id);

sai_status_t
_ctc_sai_npm_acl_entry_id_dealloc(uint8 lchip, uint32_t acl_entry_id);

sai_status_t
ctc_sai_npm_write_hardware_table(uint8 lchip);

extern sai_status_t
ctc_sai_npm_api_init();

extern sai_status_t
ctc_sai_npm_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_npm_db_deinit(uint8 lchip);


#endif /*_CTC_SAI_NPM_H*/

