#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/


#define CTC_SAI_DIAG_DROP_REASON_BASE_IPE 0
#define CTC_SAI_DIAG_DROP_REASON_BASE_EPE 64

/* Only support 7132 */
enum ctc_drop_reason_id_e
{
   /*-----------------------  IPE   -----------------------*/
    IPE_START        = CTC_SAI_DIAG_DROP_REASON_BASE_IPE,

    IPE_FEATURE_START = IPE_START,
    IPE_RESERVED0     = IPE_FEATURE_START  ,/**IPE_RESERVED0, Ipe reserved0 discard*/
    IPE_LPBK_HDR_ADJ_RM_ERR                ,/**IPE_LPBK_HDR_ADJ_RM_ERR, Packet discard due to length error when do loopback header adjust*/
    IPE_PARSER_LEN_ERR                     ,/**IPE_PARSER_LEN_ERR, Packet discard due to length error when do parser*/
    IPE_UC_TO_LAG_GROUP_NO_MEMBER          ,/**IPE_UC_TO_LAG_GROUP_NO_MEMBER, Packet discard due to ucast no linkagg member*/
    IPE_EXCEP2_DIS                         ,/**IPE_EXCEP2_DIS, L2 PDU discard*/
    IPE_DS_USERID_DIS                      ,/**IPE_DS_USERID_DIS, Next hop index from SCL is invalid*/
    IPE_RECEIVE_DIS                        ,/**IPE_RECEIVE_DIS, Port or vlan receive function is disabled*/
    IPE_MICROFLOW_POLICING_FAIL_DROP       ,/**IPE_MICROFLOW_POLICING_FAIL_DROP, Microflow policing discard*/
    IPE_PROTOCOL_VLAN_DIS                  ,/**IPE_PROTOCOL_VLAN_DIS, Protocol vlan is configed as discard*/
    IPE_AFT_DIS                            ,/**IPE_AFT_DIS, AFT discard*/
    IPE_L2_ILLEGAL_PKT_DIS                 ,/**IPE_L2_ILLEGAL_PKT_DIS, Packet discard due to invalid mcast MACSA or invalid IPDA/IPSA*/
    IPE_STP_DIS                            ,/**IPE_STP_DIS, STP discard*/
    IPE_DEST_MAP_PROFILE_DISCARD           ,/**IPE_DEST_MAP_PROFILE_DISCARD, Destmap of destmap profile is invalid(destmap=0xFFFF)*/
    IPE_STACK_REFLECT_DISCARD              ,/**IPE_STACK_REFLECT_DISCARD, Stack reflect discard*/
    IPE_ARP_DHCP_DIS                       ,/**IPE_ARP_DHCP_DIS, ARP or DHCP discard*/
    IPE_DS_PHYPORT_SRCDIS                  ,/**IPE_DS_PHYPORT_SRCDIS, Ingress phyport discard*/
    IPE_VLAN_FILTER_DIS                    ,/**IPE_VLAN_FILTER_DIS, Ingress vlan filtering discard*/
    IPE_DS_SCL_DIS                         ,/**IPE_DS_SCL_DIS, Packet discard due to SCL deny or GRE flag mismatch*/
    IPE_ROUTE_ERROR_PKT_DIS                ,/**IPE_ROUTE_ERROR_PKT_DIS, Mcast MAC DA discard or same IP DA SA discard*/
    IPE_SECURITY_CHK_DIS                   ,/**IPE_SECURITY_CHK_DIS, Bridge dest port is equal to source port discard or unknown Mcast/Ucast or Bcast discard*/
    IPE_STORM_CTL_DIS                      ,/**IPE_STORM_CTL_DIS, Port or vlan based storm Control discard*/
    IPE_LEARNING_DIS                       ,/**IPE_LEARNING_DIS, MACSA is configed as discard or source port mismatch or port security discard*/
    IPE_NO_FORWARDING_PTR                  ,/**IPE_NO_FORWARDING_PTR, Packet discard due to not find next hop(no dsFwdPtr)*/
    IPE_IS_DIS_FORWARDING_PTR              ,/**IPE_IS_DIS_FORWARDING_PTR, Packet discard due to next hop index is invalid(dsFwdPtr=0xFFFF)*/
    IPE_FATAL_EXCEP_DIS                    ,/**IPE_FATAL_EXCEP_DIS, Packet discard due to some fatal event occured*/
    IPE_APS_DIS                            ,/**IPE_APS_DIS, APS selector discard*/
    IPE_DS_FWD_DESTID_DIS                  ,/**IPE_DS_FWD_DESTID_DIS, Packet discard due to next hop is invalid(nextHopPtr=0x3FFFF)*/
    IPE_LOOPBACK_DIS                       ,/**IPE_LOOPBACK_DIS, Loopback discard when from Fabric is disabled*/
    IPE_DISCARD_PACKET_LOG_ALL_TYPE        ,/**IPE_DISCARD_PACKET_LOG_ALL_TYPE, Packet log all type discard*/
    IPE_PORT_MAC_CHECK_DIS                 ,/**IPE_PORT_MAC_CHECK_DIS, Port mac check discard*/
    IPE_L3_EXCEP_DIS                       ,/**IPE_L3_EXCEP_DIS, Packet discard due to VXLAN/NVGRE fraginfo error or ACH type error*/
    IPE_STACKING_HDR_CHK_ERR               ,/**IPE_STACKING_HDR_CHK_ERR, Stacking network header length or MAC DA check error*/
    IPE_TUNNEL_DECAP_MARTIAN_ADD           ,/**IPE_TUNNEL_DECAP_MARTIAN_ADD, IPv4/IPv6 tunnel outer IPSA is Martian address*/
    IPE_TUNNELID_FWD_PTR_DIS               ,/**IPE_TUNNELID_FWD_PTR_DIS, Packet discard due to tunnel dsfwdptr is invalid(dsfwdptr=0xFFFF)*/
    IPE_VXLAN_FLAG_CHK_ERROR_DISCARD       ,/**IPE_VXLAN_FLAG_CHK_ERROR_DISCARD, VXLAN flag error*/
    IPE_VXLAN_NVGRE_INNER_VTAG_CHK_DIS     ,/**IPE_VXLAN_NVGRE_INNER_VTAG_CHK_DIS, VXLAN/NVGRE inner Vtag check error*/
    IPE_VXLAN_NVGRE_CHK_FAIL               ,/**IPE_VXLAN_NVGRE_CHK_FAIL, VXLAN/NVGRE check error*/
    IPE_GENEVE_PAKCET_DISCARD              ,/**IPE_GENEVE_PAKCET_DISCARD, VXLAN packet is OAM frame or has option or redirect to CPU*/
    IPE_ICMP_REDIRECT_DIS                  ,/**IPE_ICMP_REDIRECT_DIS, ICMP discard or redirect to CPU*/
    IPE_ICMP_ERR_MSG_DIS                   ,/**IPE_ICMP_ERR_MSG_DIS, IPv4/IPv6 ICMP error MSG check discard*/
    IPE_PTP_PKT_DIS                        ,/**IPE_PTP_PKT_DIS, PTP packet discard*/
    IPE_MUX_PORT_ERR                       ,/**IPE_MUX_PORT_ERR, Mux port error*/
    IPE_HW_ERROR_DISCARD                   ,/**IPE_HW_ERROR_DISCARD, Packet discard due to hardware error*/
    IPE_USERID_BINDING_DIS                 ,/**IPE_USERID_BINDING_DIS, Packet discard due to mac/port/vlan/ip/ binding mismatch */
    IPE_DS_PLC_DIS                         ,/**IPE_DS_PLC_DIS, Policing discard*/
    IPE_DS_ACL_DIS                         ,/**IPE_DS_ACL_DIS, ACL discard*/
    IPE_DOT1AE_CHK                         ,/**IPE_DOT1AE_CHK, Dot1ae check discard*/
    IPE_OAM_DISABLE                        ,/**IPE_OAM_DISABLE, OAM discard*/
    IPE_OAM_NOT_FOUND                      ,/**IPE_OAM_NOT_FOUND, OAM lookup hash conflict or no MEP/MIP at ether OAM edge port*/
    IPE_CFLAX_SRC_ISOLATE_DIS              ,/**IPE_CFLAX_SRC_ISOLATE_DIS, Cflex source isolate discard*/
    IPE_OAM_ETH_VLAN_CHK                   ,/**IPE_OAM_ETH_VLAN_CHK, Linkoam with vlan tag or ethoam without vlan tag*/
    IPE_OAM_BFD_TTL_CHK                    ,/**IPE_OAM_BFD_TTL_CHK, BFD ttl check discard*/
    IPE_OAM_FILTER_DIS                     ,/**IPE_OAM_FILTER_DIS, OAM packet STP/VLAN filter when no MEP/MIP*/
    IPE_TRILL_CHK                          ,/**IPE_TRILL_CHK, Trill check discard*/
    IPE_WLAN_CHK                           ,/**IPE_WLAN_CHK, Wlan check diacard*/
    IPE_TUNNEL_ECN_DIS                     ,/**IPE_TUNNEL_ECN_DIS, Tunnel ECN discard*/
    IPE_EFM_DIS                            ,/**IPE_EFM_DIS, EFM OAM packet discard or redirect to CPU*/
    IPE_ILOOP_DIS                          ,/**IPE_ILOOP_DIS, Iloop discard*/
    IPE_MPLS_ENTROPY_LABEL_CHK             ,/**IPE_MPLS_ENTROPY_LABEL_CHK, Entropy label check discard*/
    IPE_MPLS_TP_MCC_SCC_DIS                ,/**IPE_MPLS_TP_MCC_SCC_DIS, TP MCC or SCC packet redirect to CPU*/
    IPE_MPLS_MC_PKT_ERROR                  ,/**IPE_MPLS_MC_PKT_ERROR, MPLS mcast discard*/
    IPE_L2_EXCPTION_DIS                    ,/**IPE_L2_EXCPTION_DIS, L2 PDU discard*/
    IPE_NAT_PT_CHK                         ,/**IPE_NAT_PT_CHK, IPv4/IPv6 Ucast NAT discard*/
    IPE_SD_CHECK_DIS                       ,/**IPE_SD_CHECK_DIS, Signal degrade discard*/
    IPE_FEATURE_END = IPE_SD_CHECK_DIS,
    IPE_END = IPE_FEATURE_END,
   /*-----------------------  EPE   ------------------------*/
    EPE_START          = CTC_SAI_DIAG_DROP_REASON_BASE_EPE,
    EPE_FEATURE_START = EPE_START,
    EPE_HDR_ADJ_DESTID_DIS = EPE_FEATURE_START,/**EPE_HDR_ADJ_DESTID_DIS, Packet discard by drop channel*/
    EPE_RESERVED                           ,/**EPE_RESERVED, Epe reserved discard*/
    EPE_HDR_ADJ_REMOVE_ERR                 ,/**EPE_HDR_ADJ_REMOVE_ERR, Packet discard due to remove bytes error at header adjust(offset>144B)*/
    EPE_DS_DESTPHYPORT_DSTID_DIS           ,/**EPE_DS_DESTPHYPORT_DSTID_DIS, Egress port discard*/
    EPE_PORT_ISO_DIS                       ,/**EPE_PORT_ISO_DIS, Port isolate or Pvlan discard*/
    EPE_DS_VLAN_TRANSMIT_DIS               ,/**EPE_DS_VLAN_TRANSMIT_DIS, Packet discard due to port/vlan transmit disable*/
    EPE_BRG_TO_SAME_PORT_DIS               ,/**EPE_BRG_TO_SAME_PORT_DIS, Packet discard due to bridge to same port(no use)*/
    EPE_VPLS_HORIZON_SPLIT_DIS             ,/**EPE_VPLS_HORIZON_SPLIT_DIS, VPLS split horizon split or E-tree discard*/
    EPE_VLAN_FILTER_DIS                    ,/**EPE_VLAN_FILTER_DIS, Egress vlan filtering discard*/
    EPE_STP_DIS                            ,/**EPE_STP_DIS, STP discard*/
    EPE_PARSER_LEN_ERR                     ,/**EPE_PARSER_LEN_ERR, Packet discard due to parser length error*/
    EPE_RESERVED0                        ,/**EPE_RESERVED0, Epe reserved0 discard*/
    EPE_UC_MC_FLOODING_DIS                 ,/**EPE_UC_MC_FLOODING_DIS, Unkown-unicast/known-unicast/unkown-mcast/known-mcast/broadcast discard*/
    EPE_OAM_802_3_DIS                      ,/**EPE_OAM_802_3_DIS, Discard non-EFM OAM packet*/
    EPE_TTL_FAIL                           ,/**EPE_TTL_FAIL, TTL check failed*/
    EPE_REMOTE_MIRROR_ESCAP_DIS            ,/**EPE_REMOTE_MIRROR_ESCAP_DIS, Packet discard due to remote mirror filtering*/
    EPE_TUNNEL_MTU_CHK_DIS                 ,/**EPE_TUNNEL_MTU_CHK_DIS, Packet discard due to tunnel MTU check*/
    EPE_INTERF_MTU_CHK_DIS                 ,/**EPE_INTERF_MTU_CHK_DIS, Packet discard due to interface MTU check*/
    EPE_LOGIC_PORT_CHK_DIS                 ,/**EPE_LOGIC_PORT_CHK_DIS, Packet discard due to logic source port is equal to dest port*/
    EPE_DS_ACL_DIS                         ,/**EPE_DS_ACL_DIS, Packet discard due to ACL deny*/
    EPE_DS_VLAN_XLATE_DIS                  ,/**EPE_DS_VLAN_XLATE_DIS, Packet discard due to SCL deny*/
    EPE_RESERVED4                          ,/**EPE_RESERVED4, EPE reserved4*/
    EPE_CRC_ERR_DIS                        ,/**EPE_CRC_ERR_DIS, Packet discard due to CRC check error(no use)*/
    EPE_ROUTE_PLD_OP_DIS                   ,/**EPE_ROUTE_PLD_OP_DIS, Packet discard due to route payload operation no IP*/
    EPE_BRIDGE_PLD_OP_DIS                  ,/**EPE_BRIDGE_PLD_OP_DIS, Bridge payload operation bridge is disabled*/
    EPE_STRIP_OFFSET_LARGE                 ,/**EPE_STRIP_OFFSET_LARGE, Packet strip offset is larger then efficientFirstBufferLength*/
    EPE_BFD_DIS                            ,/**EPE_BFD_DIS, BFD discard(no use)*/
    EPE_PORT_REFLECTIVE_CHK_DIS            ,/**EPE_PORT_REFLECTIVE_CHK_DIS, Packet discard due to dest port is equal to source port*/
    EPE_IP_MPLS_TTL_CHK_ERR                ,/**EPE_IP_MPLS_TTL_CHK_ERR, Packet discard due to IP/MPLS TTL check error when do L3 edit*/
    EPE_OAM_EDGE_PORT_DIS                  ,/**EPE_OAM_EDGE_PORT_DIS, No MEP/MIP at edge port for OAM packet*/
    EPE_NAT_PT_ICMP_ERR                    ,/**EPE_NAT_PT_ICMP_ERR, NAT/PT ICMP error*/
    EPE_LATENCY_DISCARD                    ,/**EPE_LATENCY_DISCARD, Packet discard due to latency is too long*/
    EPE_LOCAL_OAM_DIS                      ,/**EPE_LOCAL_OAM_DIS, Local OAM discard(no use)*/
    EPE_OAM_FILTERING_DIS                  ,/**EPE_OAM_FILTERING_DIS, OAM packet Port/STP/VLAN filter discard or forward link OAM packet*/
    EPE_RESERVED3                          ,/**EPE_RESERVED3, EPE reserved3*/
    EPE_SAME_IPDA_IPSA_DIS                 ,/**EPE_SAME_IPDA_IPSA_DIS, Same MAC DA SA or IP DA SA*/
    EPE_SD_CHK_DISCARD                     ,/**EPE_SD_CHK_DISCARD, Signal degrade discard*/
    EPE_TRILL_PLD_OP_DIS                   ,/**EPE_TRILL_PLD_OP_DIS, TRILL payload operation discard(no use)*/
    EPE_RESERVED2                   ,/**EPE_RESERVED2, Epe reserved2 discard*/
    EPE_DS_NEXTHOP_DATA_VIOLATE            ,/**EPE_DS_NEXTHOP_DATA_VIOLATE, Packet discard due to DsNextHop data violate*/
    EPE_DEST_VLAN_PTR_DIS                  ,/**EPE_DEST_VLAN_PTR_DIS, Packet discard due to dest vlan index is invalid*/
    EPE_DS_L3EDIT_DATA_VIOLATE1            ,/**EPE_DS_L3EDIT_DATA_VIOLATE1, Discard by L3 edit or inner L2 edit violate*/
    EPE_DS_L3EDIT_DATA_VIOLATE2            ,/**EPE_DS_L3EDIT_DATA_VIOLATE2, Discard by L3 edit or inner L2 edit violate*/
    EPE_DS_L3EDITNAT_DATA_VIOLATE          ,/**EPE_DS_L3EDITNAT_DATA_VIOLATE, Discard by L3 edit or inner L2 edit violate*/
    EPE_DS_L2EDIT_DATA_VIOLATE1            ,/**EPE_DS_L2EDIT_DATA_VIOLATE1, Discard by L2 edit config*/
    EPE_DS_L2EDIT_DATA_VIOLATE2            ,/**EPE_DS_L2EDIT_DATA_VIOLATE2, Discard by L2 edit violate*/
    EPE_PKT_HDR_C2C_TTL_ZERO               ,/**EPE_PKT_HDR_C2C_TTL_ZERO, Packet discard due to packetHeader C2C TTL zero(no use)*/
    EPE_PT_UDP_CHKSUM_ZERO                 ,/**EPE_PT_UDP_CHKSUM_ZERO, Packet discard due to PT/UDP checksum is zero for NAT*/
    EPE_OAM_TO_LOCAL_DIS                   ,/**EPE_OAM_TO_LOCAL_DIS, Packet is sent to local up MEP*/
    EPE_HARD_ERROR_DIS                     ,/**EPE_HARD_ERROR_DIS, Packet discard due to hardware error*/
    EPE_MICROFLOW_POLICING_FAIL_DROP       ,/**EPE_MICROFLOW_POLICING_FAIL_DROP, Microflow policing discard*/
    EPE_ARP_MISS_DISCARD                   ,/**EPE_ARP_MISS_DISCARD, ARP miss discard*/
    EPE_ILLEGAL_PACKET_TO_E2I_LOOP_CHANNEL ,/**EPE_ILLEGAL_PACKET_TO_E2I_LOOP_CHANNEL, Packet discard due to illegal packet to e2iloop channel*/
    EPE_UNKNOWN_DOT11_PACKET_DISCARD       ,/**EPE_UNKNOWN_DOT11_PACKET_DISCARD, Unknow dot1ae packet discard*/
    EPE_DOT1AE_PN_OVERFLOW                 ,/**EPE_DOT1AE_PN_OVERFLOW, dot1ae pn overflow*/
    EPE_PON_DOWNSTREAM_CHECK_FAIL          ,/**EPE_PON_DOWNSTREAM_CHECK_FAIL, pon downstream check fail*/
    EPE_FEATURE_END = EPE_PON_DOWNSTREAM_CHECK_FAIL,
    EPE_MIN_PKT_LEN_ERR                    ,/**EPE_MIN_PKT_LEN_ERR, Packet discard due to min length check error*/
    EPE_ELOG_ABORTED_PKT                   ,/**EPE_ELOG_ABORTED_PKT, Packet discard due to elog aborted*/
    EPE_ELOG_DROPPED_PKT                   ,/**EPE_ELOG_DROPPED_PKT, Packet discard due to elog dropped*/
    EPE_HW_START                           ,
    EPE_HW_HAR_ADJ = EPE_HW_START,/**EPE_HW_HAR_ADJ, Some hardware error at header adjust*/
    EPE_HW_NEXT_HOP                        ,/**EPE_HW_NEXT_HOP, Some hardware error occurred at nexthop mapper*/
    EPE_HW_L2_EDIT                         ,/**EPE_HW_L2_EDIT, Some hardware error occurred at l2 edit*/
    EPE_HW_L3_EDIT                         ,/**EPE_HW_L3_EDIT, Some hardware error occurred at l3 edit*/
    EPE_HW_INNER_L2                        ,/**EPE_HW_INNER_L2, Some hardware error occurred at inner l2 edit*/
    EPE_HW_PAYLOAD                         ,/**EPE_HW_PAYLOAD, Some hardware error occurred when edit payload*/
    EPE_HW_ACL_OAM                         ,/**EPE_HW_ACL_OAM, Some hardware error occurred when do OAM lookup*/
    EPE_HW_CLASS                           ,/**EPE_HW_CLASS, Some hardware error occurred at classification*/
    EPE_HW_OAM                             ,/**EPE_HW_OAM, Some hardware error occurred when do OAM process*/
    EPE_HW_EDIT                            ,/**EPE_HW_EDIT, Some hardware error occurred when do edit*/
    EPE_HW_END = EPE_HW_EDIT,
    EPE_END = EPE_HW_END,
    /*-----------------------  BSR   ------------------------*/
    BSR_START                              ,
    /*----------per channel discard stats start--------------*/
    BUFSTORE_ABORT_TOTAL = BSR_START,       /**BUFSTORE_ABORT_TOTAL, Packet discard in BSR and is due to crc/ecc/packet len error or miss EOP or pkt buffer is full */
    BUFSTORE_LEN_ERROR              ,/**BUFSTORE_LEN_ERROR, Packet discard in BSR and is due to maximum or minimum packet length check*/
    BUFSTORE_IRM_RESRC              ,/**BUFSTORE_IRM_RESRC, Packet discard in BSR and is due to IRM no resource*/
    BUFSTORE_DATA_ERR               ,/**BUFSTORE_DATA_ERR, Packet discard in BSR and is due to crc error or ecc error*/
    BUFSTORE_CHIP_MISMATCH          ,/**BUFSTORE_CHIP_MISMATCH, Packet discard in BSR and is due to chip id mismatch*/
    BUFSTORE_NO_BUFF                ,/**BUFSTORE_NO_BUFF, Packet discard in BSR and is due to no pkt buffer*/
    BUFSTORE_NO_EOP                 ,/**BUFSTORE_NO_EOP, Packet discard in BSR and is due to missing EOP */
    METFIFO_STALL_TO_BS_DROP        ,/**METFIFO_STALL_TO_BS_DROP, Packet discard in BSR and is due to the copy ability of MET*/
    BUFSTORE_SLIENT_TOTAL           ,/**BUFSTORE_SLIENT_TOTAL, Packet discard in BSR and is due to resource check fail*/
    /*----------per channel discard stats end----------------*/
    TO_BUFSTORE_FROM_DMA            ,/**TO_BUFSTORE_FROM_DMA, Packet from DMA discard in BSR and is due to Bufstore error*/
    TO_BUFSTORE_FROM_NETRX          ,/**TO_BUFSTORE_FROM_NETRX, Packet from NetRx discard in BSR and is due to Bufstore error*/
    TO_BUFSTORE_FROM_OAM            ,/**TO_BUFSTORE_FROM_OAM, Packet from OAM discard in BSR and is due to Bufstore error*/
    BUFSTORE_OUT_SOP_PKT_LEN_ERR    ,/**BUFSTORE_OUT_SOP_PKT_LEN_ERR, Packet from BUFSTORE discard in BSR and is due to SOP length error */
    METFIFO_MC_FROM_DMA             ,/**METFIFO_MC_FROM_DMA, Mcast packet from DMA discard in BSR and is due to the copy ability of MET*/
    METFIFO_UC_FROM_DMA             ,/**METFIFO_UC_FROM_DMA, Ucast packet from DMA discard in BSR and is due to the copy ability of MET*/
    METFIFO_MC_FROM_ELOOP_MCAST     ,/**METFIFO_MC_FROM_ELOOP_MCAST, Eloop mcast packet discard in BSR and is due to the copy ability of MET*/
    METFIFO_UC_FROM_ELOOP_UCAST     ,/**METFIFO_UC_FROM_ELOOP_UCAST, Eloop ucast packet discard in BSR and is due to the copy ability of MET*/
    METFIFO_MC_FROM_IPE_CUT_THR     ,/**METFIFO_MC_FROM_IPE_CUT_THR, Mcast packet discard in BSR and is due to the copy ability of MET in cutthrough model*/
    METFIFO_UC_FROM_IPE_CUT_THR     ,/**METFIFO_UC_FROM_IPE_CUT_THR, Ucast packet discard in BSR and is due to the copy ability of MET in cutthrough model*/
    METFIFO_MC_FROM_IPE             ,/**METFIFO_MC_FROM_IPE, IPE mcast packet discard in BSR and is due to the copy ability of MET*/
    METFIFO_UC_FROM_IPE             ,/**METFIFO_UC_FROM_IPE, IPE ucast packet discard in BSR and is due to the copy ability of MET*/
    METFIFO_MC_FROM_OAM             ,/**METFIFO_MC_FROM_OAM, OAM mcast packet discard in BSR and is due to the copy ability of MET*/
    METFIFO_UC_FROM_OAM             ,/**METFIFO_UC_FROM_OAM, OAM ucast packet discard in BSR and is due to the copy ability of MET*/
    BUFRETRV_FROM_DEQ_MSG_ERR       ,/**BUFRETRV_FROM_DEQ_MSG_ERR, Packet from DEQ discard in BSR and is due to MSG error */
    BUFRETRV_FROM_QMGR_LEN_ERR      ,/**BUFRETRV_FROM_QMGR_LEN_ERR, Packet from QMGR discard in BSR and is due to length error*/
    BUFRETRV_OUT_DROP               ,/**BUFRETRV_OUT_DROP, Packet from bufRetrv discard in BSR*/
    /*----------per queue discard stats start----------------*/
    ENQ_WRED_DROP                   ,/**ENQ_WRED_DROP, ENQ packet discard in BSR and is due to WRED error*/
    ENQ_TOTAL_DROP                  ,/**ENQ_TOTAL_DROP, ENQ packe total discard*/
    ENQ_NO_QUEUE_ENTRY              ,/**ENQ_NO_QUEUE_ENTRY, ENQ packet discard in BSR and is due to no ptr*/
    ENQ_PORT_NO_BUFF                ,/**ENQ_PORT_NO_BUFF, ENQ packet discard in BSR and is due to port no buffer*/
    ENQ_QUEUE_NO_BUFF               ,/**ENQ_QUEUE_NO_BUFF, ENQ packet discard in BSR and is due to queue no buffer*/
    ENQ_SC_NO_BUFF                  ,/**ENQ_SC_NO_BUFF, ENQ packet discard in BSR and is due to service class no buffer*/
    ENQ_SPAN_NO_BUFF                ,/**ENQ_SPAN_NO_BUFF, ENQ packet discard in BSR and is due to span no buffer*/
    ENQ_TOTAL_NO_BUFF               ,/**ENQ_TOTAL_NO_BUFF, ENQ packet discard in BSR and is due to no total buffer*/
    ENQ_FWD_DROP                    ,/**ENQ_FWD_DROP, ENQ packet discard in BSR and is due to foward drop*/
    ENQ_FWD_DROP_CFLEX_ISOLATE_BLOCK,/**ENQ_FWD_DROP_CFLEX_ISOLATE_BLOCK, ENQ packet discard in BSR and is due to isolated port when stacking*/
    ENQ_FWD_DROP_CHAN_INVALID       ,/**ENQ_FWD_DROP_CHAN_INVALID, ENQ packet discard in BSR and is due to invalid channel id*/
    ENQ_FWD_DROP_TOTAL              ,/**ENQ_FWD_DROP_TOTAL, ENQ packet discard in BSR and is due to fowarding drop*/
    ENQ_FWD_DROP_FROM_LAG           ,/**ENQ_FWD_DROP_FROM_LAG, ENQ packet discard in BSR and is due to linkagg error*/
    ENQ_FWD_DROP_FROM_LAG_ERR       ,/**ENQ_FWD_DROP_FROM_LAG_ERR, ENQ packet discard in BSR and is due to crc error or memory error when do linkagg*/
    ENQ_FWD_DROP_FROM_LAG_MC        ,/**ENQ_FWD_DROP_FROM_LAG_MC, ENQ packet discard in BSR and is due to invalid dest chip id when do mcast linkagg*/
    ENQ_FWD_DROP_FROM_LAG_NO_MEM    ,/**ENQ_FWD_DROP_FROM_LAG_NO_MEM, ENQ packet discard in BSR and is due to no linkagg member*/
    ENQ_FWD_DROP_PORT_ISOLATE_BLOCK ,/**ENQ_FWD_DROP_PORT_ISOLATE_BLOCK, ENQ packet discard in BSR and is due to isolated port*/
    ENQ_FWD_DROP_RSV_CHAN_DROP      ,/**ENQ_FWD_DROP_RSV_CHAN_DROP, ENQ packet discard in BSR and is due to drop channel*/
    ENQ_FWD_DROP_FROM_STACKING_LAG  ,/**ENQ_FWD_DROP_FROM_STACKING_LAG, ENQ packet discard in BSR and is due to stacking linkagg error*/
    /*-----------per queue discard stats end-----------------*/
    BSR_END = ENQ_FWD_DROP_FROM_STACKING_LAG,
   /*-----------------------  NETRX   ----------------------*/
    NETRX_START                            ,
    NETRX_NO_BUFFER = NETRX_START,/**NETRX_NO_BUFFER, Packet discard due to no buffer in port oversub model*/
    NETRX_LEN_ERROR                        ,/**NETRX_LEN_ERROR, Packet discard due to the failure of max or min pkt len check*/
    NETRX_PKT_ERROR                        ,/**NETRX_PKT_ERROR, Packet error discard*/
    NETRX_BPDU_ERROR                       ,/**NETRX_BPDU_ERROR, BPDU discard*/
    NETRX_FRAME_ERROR                      ,/**NETRX_FRAME_ERROR, Packet discard due to misssing sop or eop*/
    NETRX_END = NETRX_FRAME_ERROR,
   /*-----------------------  NETTX   ----------------------*/
    NETTX_START                            ,
    NETTX_MIN_LEN = NETTX_START,/**NETTX_MIN_LEN, Packet discard due to smaller than the cfgMinPktLen*/
    NETTX_NO_BUFFER                        ,/**NETTX_NO_BUFFER, Packet discard due to the use up of PktBuffer in NETTX*/
    NETTX_SOP_EOP                          ,/**NETTX_SOP_EOP, Packet discard due to missing EOP or SOP*/
    NETTX_TX_ERROR                         ,/**NETTX_TX_ERROR, The number of error packets sending to MAC*/
    NETTX_END = NETTX_TX_ERROR,
   /*-----------------------   OAM   ------------------------*/
    OAM_START                              ,
    OAM_HW_ERROR = OAM_START,/**OAM_HW_ERROR, Some hardware error occured*/
    OAM_EXCEPTION                            ,/**OAM_EXCEPTION, Some exception occured when process OAM packet*/
    OAM_END = OAM_EXCEPTION ,
    CTC_SAI_DROP_REASON_MAX,
};
typedef enum ctc_drop_reason_id_e ctc_drop_reason_id_t;


typedef enum ctc_sai_debug_counter_drop_reason_dir_s
{
    DROP_REASON_IN,
    DROP_REASON_OUT,
    DROP_REASON_MAX
}ctc_sai_debug_counter_drop_reason_dir_t;


typedef struct ctc_sai_debug_counter_s
{
    sai_debug_counter_type_t debug_counter_type;    
    sai_debug_counter_bind_method_t bind_method;
    ctc_sai_debug_counter_drop_reason_dir_t dir; 
    uint32_t debug_counter_index;
    uint32_t drop_reason_list_bitmap[2];

}ctc_sai_debug_counter_t;

extern sai_status_t
ctc_sai_debug_counter_api_init();

extern sai_status_t
ctc_sai_debug_counter_db_init(uint8 lchip);

extern void 
ctc_sai_debug_counter_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);
    

extern sai_status_t
ctc_sai_debug_counter_get_port_stats(uint8 lchip, uint16 portid, uint32 drop_index, uint32 with_clear, uint64* count);

extern sai_status_t 
ctc_sai_debug_counter_get_switch_stats(uint8 lchip, uint32 drop_index, uint32 with_clear, uint64* count);


