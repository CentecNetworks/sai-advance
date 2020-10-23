/**
 @file ctc_sai_bfd.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-06-21

 @version v2.0

\p
 This module defines SAI Bfd.
\b
\p
 The BFD Module APIs supported by centec devices:
\p
\b
\t  |   API                                                     |   SUPPORT CHIPS LIST   |
\t  |  create_bfd_session                                       |        CTC7132         |
\t  |  remove_bfd_session                                       |        CTC7132         |
\t  |  set_bfd_session_attribute                                |        CTC7132         |
\t  |  get_bfd_session_attribute                                |        CTC7132         |
\t  |  get_bfd_session_stats                                    |        CTC7132         |
\t  |  get_bfd_session_stats_ext                                |        CTC7132         |
\t  |  clear_bfd_session_stats                                  |        CTC7132         |
\b
\p
 The BFD Session attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\t  |  SAI_BFD_SESSION_ATTR_TYPE                                |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID                     |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER                      |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_PORT                                |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR                 |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR                |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_UDP_SRC_PORT                        |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_TC                                  |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_VLAN_TPID                           |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_VLAN_ID                             |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_VLAN_PRI                            |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_VLAN_CFI                            |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID                   |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE              |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_IPHDR_VERSION                       |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_TOS                                 |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_TTL                                 |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS                      |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS                      |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS                     |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS                     |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_TUNNEL_TOS                          |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_TUNNEL_TTL                          |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_TUNNEL_SRC_IP_ADDRESS               |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_TUNNEL_DST_IP_ADDRESS               |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_ECHO_ENABLE                         |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_MULTIHOP                            |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_CBIT                                |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_MIN_TX                              |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_MIN_RX                              |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_MULTIPLIER                          |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_REMOTE_MIN_TX                       |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_REMOTE_MIN_RX                       |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_STATE                               |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE                        |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_NEGOTIATED_TX                       |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_NEGOTIATED_RX                       |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_LOCAL_DIAG                          |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_REMOTE_DIAG                         |        CTC7132         |
\t  |  SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER                   |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_REMOTE_STATE                        |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE                 |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID                    |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE                    |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL                       |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_MPLS_TTL                            |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_MPLS_EXP                            |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_TP_CV_ENABLE                        |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_TP_CV_SRC_MEP_ID                    |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID              |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL                      |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_NEXT_HOP_ID                         |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID     |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH    |        CTC7132         |
\e  |  SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN                    |        CTC7132         |
\b
*/

#ifndef _CTC_SAI_BFD_H
#define _CTC_SAI_BFD_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

/* supported BFD rx/tx interval in microseconds */
#define SAI_SUPPORTED_MIN_BFD_RX_INTERVAL 1
#define SAI_SUPPORTED_MIN_BFD_TX_INTERVAL 1

typedef enum _ctc_sai_bfd_inner_nh_type_s
{
    CTC_SAI_BFD_NH_TYPE_NONE,
    CTC_SAI_BFD_NH_TYPE_IPUC,
    CTC_SAI_BFD_NH_TYPE_IP_TUNNEL,
    CTC_SAI_BFD_NH_TYPE_ILOOP,
    CTC_SAI_BFD_NH_TYPE_MAX,
} ctc_sai_bfd_inner_nh_type_t;


typedef struct ctc_sai_bfd_s
{
    /*common */
    sai_bfd_session_type_t session_type;    
    sai_bfd_session_offload_type_t offload_type;
    uint32 local_mep_index;
    uint32 remote_mep_index;
    uint8 hw_lookup_valid;
    uint8 add_self_route_by_bfd;

    sai_object_id_t vr_oid;
    
    uint32 inner_gport;
    uint32 inner_l3if;
    ctc_sai_bfd_inner_nh_type_t inner_nh_type;
    uint32 inner_nhid;
    uint16 udp_src_port;
    
    sai_bfd_encapsulation_type_t encap_type;
    sai_bfd_mpls_type_t mpls_bfd_type;       
    uint8 echo_en;    

    /*micor bfd */
    sai_object_id_t dst_port_oid;
    sai_mac_t src_mac;
    sai_mac_t dst_mac;
        
    /*ip hdr */
    uint8 ip_hdr_ver;
    uint8 ip_tos;
    uint8 ip_ttl;
    sai_ip_address_t src_ip_addr;
    sai_ip_address_t dst_ip_addr;

    /*mpls & tp bfd */
    uint8 ach_header_valid;
    sai_bfd_ach_channel_type_t ach_channel_type;
    sai_label_id_t mpls_in_label;
    uint8 mpls_ttl;
    uint8 mpls_exp;
    uint8 cv_en;
    uint8 without_gal;
    sai_object_id_t section_rif_oid;
    uint8 mep_id_len;

    sai_object_id_t nh_tunnel_oid;

    sai_object_id_t hw_binding_aps_group;
    uint8 hw_binding_is_protecting_path;
    uint8 hw_binding_aps_en;
    
    
} ctc_sai_bfd_t;

extern
void ctc_sai_bfd_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern sai_status_t
ctc_sai_bfd_traverse_get_session_by_mepindex(uint8 lchip, uint32 mepindex, uint8 isremote, sai_object_id_t *session_id);

extern sai_status_t
ctc_sai_bfd_api_init();

extern sai_status_t
ctc_sai_bfd_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_bfd_db_deinit(uint8 lchip);

#endif /*_CTC_SAI_BFD_H*/

