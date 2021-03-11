
#include "ctc_sai_hostif.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_policer.h"
#include "ctc_sai_lag.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_counter.h"
#include "ctc_sai_y1731.h"
#include "ctcs_api.h"
#include "linux/if_tun.h"

#define CTC_SAI_NOT_NORMAL_EXCEP(custom_reason_id) \
    (((custom_reason_id) == CTC_PKT_CPU_REASON_FWD_CPU) || ((custom_reason_id) == CTC_PKT_CPU_REASON_IP_TTL_CHECK_FAIL) \
    || ((custom_reason_id) == CTC_PKT_CPU_REASON_L3_MTU_FAIL) || ((custom_reason_id) == CTC_PKT_CPU_REASON_SFLOW_SOURCE) \
    || (((custom_reason_id) >= CTC_PKT_CPU_REASON_OAM) && ((custom_reason_id) <= CTC_PKT_CPU_REASON_OAM_DEFECT_MESSAGE)))

#define ________HOSTIF_INNER________

static sai_status_t
_ctc_sai_hostif_db_trap_deinit_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_hostif_trap_t* p_hostif_trap = NULL;

    p_hostif_trap = (ctc_sai_hostif_trap_t*)bucket_data->data;
    if (p_hostif_trap->exclude_port_list.list)
    {
        mem_free(p_hostif_trap->exclude_port_list.list);
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_trap_type_to_ctc_reason_id(uint8 lchip, sai_hostif_trap_type_t trap_type, bool is_user_defined, uint32* p_ctc_cpu_reson, uint32* p_custom_cpu_reson, uint8* is_ipv6)
{
    uint8 chip_type = 0;

    chip_type = ctcs_get_chip_type(lchip);
    *is_ipv6 = 0;
    if (is_user_defined)
    {
        switch (trap_type)
        {
            case SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ROUTER:
            case SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGHBOR:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_COPY_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_COPY_CPU;
                break;
                break;
            case SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ACL:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_FWD_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_FWD_CPU;
                break;
            case SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_FDB:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_COPY_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_COPY_CPU;
                break;
            default:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                return SAI_STATUS_NOT_SUPPORTED;
                break;
        }
    }
    else
    {
        switch (trap_type)
        {
            /* switch trap */
            case SAI_HOSTIF_TRAP_TYPE_STP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_BPDU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_BPDU;
                break;

            case SAI_HOSTIF_TRAP_TYPE_LACP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_SLOW_PROTO;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_SLOW_PROTO;
                break;

            case SAI_HOSTIF_TRAP_TYPE_EAPOL:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_EAPOL;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_EAPOL;
                break;

            case SAI_HOSTIF_TRAP_TYPE_LLDP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_LLDP;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_LLDP;
                break;

            case SAI_HOSTIF_TRAP_TYPE_PVRST:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX;
                break;

            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_QUERY:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                break;

            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_LEAVE:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                if (chip_type == CTC_CHIP_GOLDENGATE)
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                }
                else
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_LEAVE;
                }
                break;


            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V1_REPORT:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                if (chip_type == CTC_CHIP_GOLDENGATE)
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                }
                else
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_V1_REPORT;
                }
                break;

            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V2_REPORT:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                if (chip_type == CTC_CHIP_GOLDENGATE)
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                }
                else
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_V2_REPORT;
                }
                break;

            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V3_REPORT:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                if (chip_type == CTC_CHIP_GOLDENGATE)
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
                }
                else
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_V3_REPORT;
                }
                break;

            case SAI_HOSTIF_TRAP_TYPE_SAMPLEPACKET:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_SFLOW_SOURCE;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_SFLOW_SOURCE;
                break;

            case SAI_HOSTIF_TRAP_TYPE_UDLD:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX;
                break;

            case SAI_HOSTIF_TRAP_TYPE_CDP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_CDP_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_CDP_INDEX;
                break;

            case SAI_HOSTIF_TRAP_TYPE_VTP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_VTP_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_VTP_INDEX;
                break;

            case SAI_HOSTIF_TRAP_TYPE_DTP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_DTP_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_DTP_INDEX;
                break;

            case SAI_HOSTIF_TRAP_TYPE_PAGP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_PAGP_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_PAGP_INDEX;
                break;

            case SAI_HOSTIF_TRAP_TYPE_PTP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_PTP;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_PTP;
                break;

            /* router trap */
            case SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ARP;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ARP;
                break;

            case SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ARP;
                if (chip_type == CTC_CHIP_GOLDENGATE)
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ARP;
                }
                else
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_ARP_RESPONSE;
                }
                break;

            case SAI_HOSTIF_TRAP_TYPE_DHCP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_DHCP;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_DHCP;
                break;

            case SAI_HOSTIF_TRAP_TYPE_OSPF:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_OSPF;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_OSPF;
                break;

            case SAI_HOSTIF_TRAP_TYPE_PIM:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + SAI_HOSTIF_TRAP_TYPE_PIM;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + SAI_HOSTIF_TRAP_TYPE_PIM;
                break;

            case SAI_HOSTIF_TRAP_TYPE_VRRP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_VRRP;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_VRRP;
                break;

            case SAI_HOSTIF_TRAP_TYPE_DHCPV6:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_DHCP;
                if (chip_type == CTC_CHIP_GOLDENGATE)
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_DHCP;
                }
                else
                {
                    *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_DHCPV6;
                }
                *is_ipv6 = 1;
                break;

            case SAI_HOSTIF_TRAP_TYPE_OSPFV6:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_OSPFV6_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_OSPFV6_INDEX;
                *is_ipv6 = 1;
                break;

            case SAI_HOSTIF_TRAP_TYPE_VRRPV6:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_VRRP;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_VRRPV6_INDEX;
                *is_ipv6 = 1;
                break;

            case SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ICMPV6;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ICMPV6;
                *is_ipv6 = 1;
                break;

            case SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_V2:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_PIM;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_IPV6_MLD_V1_V2;
                *is_ipv6 = 1;
                break;

            case SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_REPORT:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_PIM;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_IPV6_MLD_V1_REPORT;
                *is_ipv6 = 1;
                break;

            case SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_DONE:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_PIM;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_IPV6_MLD_V1_DONE;
                *is_ipv6 = 1;
                break;

            case SAI_HOSTIF_TRAP_TYPE_MLD_V2_REPORT:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_PIM;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_MLD_V2_REPORT;
                *is_ipv6 = 1;
                break;

                /* Unknown L3 multicast packets */
            case SAI_HOSTIF_TRAP_TYPE_UNKNOWN_L3_MULTICAST:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_UNKNOWN_L3_MULTICAST;
                return SAI_STATUS_NOT_SUPPORTED;
                break;

            /* Local IP traps */
            /**
             * @brief IP packets to local router IP address (routes with
             * #SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID = #SAI_SWITCH_ATTR_CPU_PORT)
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_IP2ME:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_FWD_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_FWD_CPU;
                break;

            /**
             * @brief SSH traffic (TCP dst port == 22) to local router IP address
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_SSH:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_SSH_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_SSH_INDEX;
                break;

            /**
             * @brief SNMP traffic (UDP dst port == 161) to local router IP address
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_SNMP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_SNMP_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_SNMP_INDEX;
                break;

            /**
             * @brief BGP traffic (TCP src port == 179 or TCP dst port == 179) to local
             * router IP address (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_BGP:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_BGP;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_BGP;
                break;

            /**
             * @brief BGPv6 traffic (TCP src port == 179 or TCP dst port == 179) to
             * local router IP address (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_BGPV6:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_BGPV6_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_BGPV6_INDEX;
                *is_ipv6 = 1;
                break;

            /* Pipeline exceptions */

            /**
             * @brief Packets size exceeds the router interface MTU size
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L3_MTU_FAIL;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L3_MTU_FAIL;
                break;

            /**
             * @brief Packets with TTL 0 or 1
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_TTL_ERROR:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_IP_TTL_CHECK_FAIL;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_IP_TTL_CHECK_FAIL;
                break;

            /**
             * @brief Packets trapped when station move is observed with static FDB entry
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_STATIC_FDB_MOVE:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_MOVE;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_MOVE;
                return SAI_STATUS_NOT_SUPPORTED;
                break;

            /* Pipeline discards. For the following traps, packet action is either drop or trap */
            /**
             * @brief Packets discarded due to egress buffer full
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_EGRESS_BUFFER:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                return SAI_STATUS_NOT_SUPPORTED;
                break;

            /**
             * @brief Packets discarded by WRED
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_WRED:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                return SAI_STATUS_NOT_SUPPORTED;
                break;

            /**
             * @brief Packets discarded due to router causes, such as
             * header checksum, router interface is down,
             * matching a route with drop action (black holes), etc.
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_ROUTER:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                return SAI_STATUS_NOT_SUPPORTED;
                break;

            /* OAM exceptions */

            /**
             * @brief Packets size exceeds the router interface MTU size
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_DM:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_DM_TO_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_DM_TO_CPU;
                break;

            /**
             * @brief Y1731 LinkTrace to local switch send to CPU
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LT:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_EQUAL_LTM_LTR_TO_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_EQUAL_LTM_LTR_TO_CPU;
                break;

            /**
             * @brief Y1731 LBR to local switch send to CPU
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LBR:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_EQUAL_LBR;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_EQUAL_LBR;
                break;

            /**
             * @brief Y1731 LMR to local switch send to CPU
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LMR:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_LM_TO_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_LM_TO_CPU;
                break;

            /**
             * @brief Y1731 TP LBM CV check fail send to CPU
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_CV_FAIL:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_TP_LBM;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_TP_LBM;
                break;

            /**
             * @brief Y1731 APS to local switch send to CPU
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_APS:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_APS_PDU_TO_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_APS_PDU_TO_CPU;
                break;

            /**
             * @brief Y1731 TP DLM to local switch send to CPU
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_DLM:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_MPLS_TP_DLM_TO_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_MPLS_TP_DLM_TO_CPU;
                break;

            /**
             * @brief Y1731 TP DM/DLMDM to local switch send to CPU
             * (default packet action is drop)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_DM:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_MPLS_TP_DM_DLMDM_TO_CPU;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_MPLS_TP_DM_DLMDM_TO_CPU;
                break;

            /**
             * @brief log all packet to cpu when micro burst occur
             * (default packet action is SAI_PACKET_ACTION_COPY)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_MICROBURST_LOG:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_MONITOR_BUFFER_LOG;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_MONITOR_BUFFER_LOG;
                break;

            /**
             * @brief log packet to cpu when latency over the threshold
             * (default packet action is SAI_PACKET_ACTION_COPY)
             */
            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_LATENCY_OVERFLOW_LOG:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_MONITOR_LATENCY_LOG;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_MONITOR_LATENCY_LOG;
                break;

            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_ISIS:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX;
                break;

            default:
                *p_ctc_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                *p_custom_cpu_reson = CTC_PKT_CPU_REASON_CUSTOM_BASE;
                return SAI_STATUS_NOT_SUPPORTED;
                break;
        }
    }
    return SAI_STATUS_SUCCESS;
}

static sai_object_id_t
_ctc_sai_hostif_ctc_reason_id_to_trap_oid(uint8 lchip, uint32 custom_cpu_reson)
{
    sai_object_id_t sai_oid = 0;
    uint8 type = SAI_OBJECT_TYPE_NULL;

    if ((custom_cpu_reson == CTC_PKT_CPU_REASON_L3_COPY_CPU) || (custom_cpu_reson == CTC_PKT_CPU_REASON_FWD_CPU)
        || (custom_cpu_reson == CTC_PKT_CPU_REASON_FWD_CPU))
    {
        type = SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP;
    }
    else
    {
        type = SAI_OBJECT_TYPE_HOSTIF_TRAP;
        if (custom_cpu_reson == CTC_PKT_CPU_REASON_SFLOW_DEST)
        {
            custom_cpu_reson = CTC_PKT_CPU_REASON_SFLOW_SOURCE;
        }
    }

    sai_oid = ctc_sai_create_object_id(type, lchip, 0, 0, custom_cpu_reson);

    return sai_oid;
}
static sai_status_t
_ctc_sai_hostif_chsm_mac_addr_add(uint8* mac, uint32 cnt)
{
    uint32_t value;
    uint32_t val_high, val_low;

    val_high = (mac[0]<<16)+(mac[1]<<8)+mac[2];
    val_low = (mac[3]<<16)+(mac[4]<<8)+mac[5];
    value = val_low + cnt;
    val_low = value & 0xffffff;
    if(value > 0xffffff)
    {
        val_high = val_high+1;
    }
    mac[0] = (val_high >> 16) & 0xff;
    mac[1] = (val_high >> 8) & 0xff;
    mac[2] = val_high & 0xff;
    mac[3] = (val_low >> 16) & 0xff;
    mac[4] = (val_low >> 8) & 0xff;
    mac[5] = val_low & 0xff;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_hostif_set_hw_addr(const char *ifname, uint8 *addr)
{
    struct ifreq    ifr;
    int  fd = 0, err = 0;

    if( (fd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 )
    {
        return fd;
    }

    sal_memset(&ifr, 0, sizeof(ifr));
    ifr.ifr_addr.sa_family = 1;
    sal_strncpy(ifr.ifr_name, ifname, IFNAMSIZ - 1);
    sal_memcpy((unsigned char *)ifr.ifr_hwaddr.sa_data, addr, 6);

    if((err = ioctl(fd, SIOCSIFHWADDR, (void *)&ifr)) < 0)
    {
        close(fd);
        return SAI_STATUS_NOT_EXECUTED;
    }

    close(fd);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_port_get_mac(uint8 lchip, uint8* mac, uint32 port_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_get_router_mac(lchip, mac));

    _ctc_sai_hostif_chsm_mac_addr_add(mac, port_idx);

    return status;
}

int32
_ctc_sai_hostif_sock_set_nonblocking (sal_sock_handle_t sock, int32 state)
{
    int val = 0;

    val = fcntl (sock, F_GETFL, 0);
    if (SAL_SOCK_ERROR != val)
    {
        fcntl (sock, F_SETFL, (state ? val | O_NONBLOCK : val & (~O_NONBLOCK)));
        return 0;
    }
    else
    {
        return errno;
    }
}

int32
_ctc_sai_hostif_packet_epool_init(ctc_sai_switch_master_t* p_switch_master)
{
    p_switch_master->epoll_sock = epoll_create(2048);
    if (p_switch_master->epoll_sock < 0)
    {
        return SAI_STATUS_FAILURE;
    }

    _ctc_sai_hostif_sock_set_nonblocking(p_switch_master->epoll_sock, TRUE);

    p_switch_master->evl.data.fd = -1;
    p_switch_master->evl.events = EPOLLIN;
    return SAI_STATUS_SUCCESS;
}

#define ________HOSTIF_______
void ctc_sai_hostif_lag_member_change_cb_fn(uint8 lchip, uint32 linkagg_id, uint32 mem_port, bool change)
{
    uint32 value = 0;

    value = change?CTC_PDU_L2PDU_ACTION_TYPE_COPY_TO_CPU:CTC_PDU_L2PDU_ACTION_TYPE_FWD;

    ctcs_port_set_property(lchip, mem_port, CTC_PORT_PROP_L3PDU_ARP_ACTION, change?CTC_PORT_ARP_ACTION_TYPE_FW_EX:CTC_PORT_ARP_ACTION_TYPE_FW);
    ctcs_port_set_property(lchip, mem_port, CTC_PORT_PROP_L3PDU_DHCP_ACTION, change?CTC_PORT_ARP_ACTION_TYPE_FW_EX:CTC_PORT_ARP_ACTION_TYPE_FW);
    ctcs_l2pdu_set_port_action(lchip, mem_port, CTC_L2PDU_ACTION_INDEX_BPDU, value);
    ctcs_l2pdu_set_port_action(lchip, mem_port, CTC_L2PDU_ACTION_INDEX_SLOW_PROTO, value);
    ctcs_l2pdu_set_port_action(lchip, mem_port, CTC_L2PDU_ACTION_INDEX_EAPOL, value);
    ctcs_l2pdu_set_port_action(lchip, mem_port, CTC_L2PDU_ACTION_INDEX_LLDP, value);
    ctcs_l2pdu_set_port_action(lchip, mem_port, CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX, value);
    ctcs_l2pdu_set_port_action(lchip, mem_port, CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX, value);
    ctcs_l2pdu_set_port_action(lchip, mem_port, CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX, value);

}

sai_status_t
_ctc_sai_hostif_set_mac(uint8 lchip, const char *ifname, uint32 enable)
{
    mac_addr_t mac;
    uint32 port_idx = 0;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    sal_memset(mac, 0, sizeof(mac_addr_t));

    if (enable)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_get_router_mac(lchip, mac));
    }
    else
    {
        port_idx = if_nametoindex(ifname);
        CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_port_get_mac(lchip, mac, port_idx));
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_set_hw_addr(ifname, (uint8*)mac));

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_hostif_l3if_en(uint8 lchip, uint32 gport, uint32 enable)
{
    sai_object_id_t hostif_id = 0;
    ctc_sai_hostif_t* p_hostif_port = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    if (CTC_IS_LINKAGG_PORT(gport))
    {
        hostif_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF, lchip, SAI_OBJECT_TYPE_LAG, 0, gport);
    }
    else
    {
        hostif_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF, lchip, SAI_OBJECT_TYPE_PORT, 0, gport);
    }

    p_hostif_port = ctc_sai_db_get_object_property(lchip, hostif_id);
    if (NULL == p_hostif_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_set_mac(lchip, p_hostif_port->ifname, enable));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_alloc_hostif(ctc_sai_hostif_t** p_hostif_port)
{
    ctc_sai_hostif_t* p_hostif_port_temp = NULL;

    p_hostif_port_temp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_hostif_t));
    if (NULL == p_hostif_port_temp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_hostif_port_temp, 0, sizeof(ctc_sai_hostif_t));

    *p_hostif_port = p_hostif_port_temp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_free_hostif(ctc_sai_hostif_t* p_hostif_port)
{
    mem_free(p_hostif_port);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_hostif_create_net_device(char *dev)
{
    struct ifreq ifr;
    int fd, err;

    char *clonedev = "/dev/net/tun";

    /* Arguments taken by the function:
    *
    * char *dev: the name of an interface (or '\0'). MUST have enough
    * space to hold the interface name if '\0' is passed
    * int flags: interface flags (eg, IFF_TUN etc.)
    */
    /* open the clone device */

    if( (fd = sal_open(clonedev, O_RDWR)) < 0 )
    {
        return fd;
    }

    /* preparation of the struct ifr, of type "struct ifreq" */
    sal_memset(&ifr, 0, sizeof(ifr));
    ifr.ifr_flags = IFF_TAP | IFF_NO_PI; /* IFF_TUN or IFF_TAP, plus maybe IFF_NO_PI */
    if (*dev)
    {
        /* if a device name was specified, put it in the structure; otherwise,
        * the kernel will try to allocate the "next" device of the
        * specified type */
        sal_strncpy(ifr.ifr_name, dev, IFNAMSIZ);
    }

    /* try to create the device */
    if( (err = ioctl(fd, TUNSETIFF, (void *) &ifr)) < 0 )
    {
        sal_close(fd);
        return err;
    }

    return fd;
}

sai_status_t
_ctc_sai_hostif_remove_net_device(int32 fd)
{
    sal_close(fd);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_hostif_oper_status(char* eth_name, bool link_en)
{
    struct ifreq ifr;
    int fd,err = 0;

    if( (fd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 )
    {
        return fd;
    }

    memset(&ifr, 0, sizeof(ifr));
    ifr.ifr_addr.sa_family = AF_INET;
    strncpy(ifr.ifr_name, eth_name, IFNAMSIZ - 1);
    if( (err = ioctl(fd, SIOCGIFFLAGS, (void *) &ifr)) < 0 ){
        close(fd);
        return err;
    }

    if(link_en){
        ifr.ifr_flags |= IFF_RUNNING;
    }else{
        ifr.ifr_flags &= ~IFF_RUNNING;
    }

    err = ioctl(fd, SIOCSIFFLAGS, (void *) &ifr);
    close(fd);

    return err;
}

sai_status_t
ctc_sai_hostif_create_hostif(
        _Out_ sai_object_id_t *hostif_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val = NULL, *attr_type_val = NULL, *attr_port_val = NULL, *attr_name_val = NULL;
    uint32 attr_idx = 0;
    uint32 attr_type_idx = 0;
    uint32 attr_port_idx = 0;
    uint32 attr_name_idx = 0;
    ctc_object_id_t ctc_oid;
    ctc_object_id_t ctc_hostif_oid;
    char command[100];
    ctc_sai_hostif_t* p_hostif_port = NULL;
    int32 fd = -1;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    mac_addr_t mac;

    CTC_SAI_PTR_VALID_CHECK(hostif_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&ctc_hostif_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&command, 0, sizeof(command));
    sal_memset(mac, 0, sizeof(mac_addr_t));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_ATTR_TYPE, &attr_type_val, &attr_type_idx);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif type on create of host if\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_alloc_hostif(&p_hostif_port));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_ATTR_OPER_STATUS, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_hostif_port->oper_status = attr_val->booldata;
    }
    else
    {
        p_hostif_port->oper_status = false;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_ATTR_QUEUE, &attr_val, &attr_type_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_hostif_port->queue_id = attr_val->u32;
    }
    else
    {
        p_hostif_port->queue_id = 0;
    }

    CTC_SAI_DB_LOCK(lchip);
    ctc_hostif_oid.type = SAI_OBJECT_TYPE_HOSTIF;
    if (SAI_HOSTIF_TYPE_NETDEV == attr_type_val->s32)
    {
        p_hostif_port->hostif_type = SAI_HOSTIF_TYPE_NETDEV;
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_ATTR_OBJ_ID, &attr_port_val, &attr_port_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif port id on create of host if\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_1;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_ATTR_NAME, &attr_name_val, &attr_name_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif name on create of host if\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_1;
        }
        p_hostif_port->port_id = attr_port_val->oid;
        sal_strcpy(p_hostif_port->ifname, attr_name_val->chardata);
        CTC_SAI_ERROR_GOTO(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF, attr_port_val->oid, &ctc_oid), status, roll_back_1);
        p_hostif_port->port_type = ctc_oid.type;
        ctc_hostif_oid.sub_type = ctc_oid.type;
        ctc_hostif_oid.value = ctc_oid.value;
        if (SAI_OBJECT_TYPE_PORT == ctc_oid.type)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, ctc_oid.value, CTC_PORT_PROP_L3PDU_ARP_ACTION, CTC_PORT_ARP_ACTION_TYPE_FW_EX), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, ctc_oid.value, CTC_PORT_PROP_L3PDU_DHCP_ACTION, CTC_PORT_DHCP_ACTION_TYPE_FW_EX), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_L2PDU_ACTION_INDEX_BPDU, CTC_PDU_L2PDU_ACTION_TYPE_COPY_TO_CPU), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_L2PDU_ACTION_INDEX_SLOW_PROTO, CTC_PDU_L2PDU_ACTION_TYPE_COPY_TO_CPU), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_L2PDU_ACTION_INDEX_EAPOL, CTC_PDU_L2PDU_ACTION_TYPE_COPY_TO_CPU), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_L2PDU_ACTION_INDEX_LLDP, CTC_PDU_L2PDU_ACTION_TYPE_COPY_TO_CPU), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX, CTC_PDU_L2PDU_ACTION_TYPE_COPY_TO_CPU), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX, CTC_PDU_L2PDU_ACTION_TYPE_COPY_TO_CPU), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX, CTC_PDU_L2PDU_ACTION_TYPE_COPY_TO_CPU), status, roll_back_2);
        }
        else if (SAI_OBJECT_TYPE_LAG == ctc_oid.type)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctc_sai_lag_register_member_change_cb(lchip, CTC_SAI_LAG_MEM_CHANGE_TYPE_HOSTIF, ctc_oid.value, ctc_sai_hostif_lag_member_change_cb_fn), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctc_sai_lag_notification_all_members_change(lchip, CTC_SAI_LAG_MEM_CHANGE_TYPE_HOSTIF, ctc_oid.value, true), status, roll_back_2);
        }
        else if (SAI_OBJECT_TYPE_VLAN == ctc_oid.type)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_set_property(lchip, ctc_oid.value, CTC_VLAN_PROP_ARP_EXCP_TYPE, CTC_EXCP_FWD_AND_TO_CPU), status, roll_back_2);
            CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_set_property(lchip, ctc_oid.value, CTC_VLAN_PROP_DHCP_EXCP_TYPE, CTC_EXCP_FWD_AND_TO_CPU), status, roll_back_2);
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Invalid port object type %d", ctc_oid.type);
            status = SAI_STATUS_INVALID_ATTR_VALUE_0 + attr_port_idx;
            goto roll_back_1;
        }

#if (0 == SDK_WORK_PLATFORM)

        /* use ioctl to create tap interface in linux kernel */
        fd = _ctc_sai_hostif_create_net_device(p_hostif_port->ifname);
        if (fd < 0)
        {
            status = SAI_STATUS_NO_MEMORY;
            goto roll_back_2;
        }
#endif
        p_hostif_port->fd = fd;

#if (0 == SDK_WORK_PLATFORM)
        if (SAI_OBJECT_TYPE_VLAN != ctc_oid.type)
        {
            uint16 l3if_id =0;
            bool enable = 0;

            CTC_SAI_CTC_ERROR_GOTO(ctcs_port_get_phy_if_en(lchip, ctc_oid.value, &l3if_id, &enable), status, roll_back_3);
            CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_set_mac(lchip, p_hostif_port->ifname, enable), status, roll_back_3);
        }
#endif
        /* add fd to epoll socket list */
        p_switch_master->evl.data.fd = fd;
        epoll_ctl(p_switch_master->epoll_sock, EPOLL_CTL_ADD, fd, &p_switch_master->evl);

#if (0 == SDK_WORK_PLATFORM)

        CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_oper_status(p_hostif_port->ifname, p_hostif_port->oper_status), status, roll_back_3);
#endif

    }
    else if(SAI_HOSTIF_TYPE_FD == attr_type_val->s32)
    {
        p_hostif_port->hostif_type = SAI_HOSTIF_TYPE_FD;
        fd = socket(AF_INET, SOCK_DGRAM, 0);
        if (fd)
        {
            p_hostif_port->fd = fd;
        }
        else
        {
            goto roll_back_1;
        }
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Invalid host interface type %d\n", attr_type_val->s32);
        status = SAI_STATUS_INVALID_ATTR_VALUE_0 + attr_type_idx;
        goto roll_back_1;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_HOSTIF, &ctc_hostif_oid, hostif_id), status, roll_back_3);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *hostif_id, p_hostif_port), status, roll_back_3);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_3:
    _ctc_sai_hostif_remove_net_device(fd);

roll_back_2:
    if (SAI_HOSTIF_TYPE_NETDEV == attr_type_val->s32)
    {
        if (SAI_OBJECT_TYPE_PORT == ctc_oid.type)
        {
            ctcs_port_set_property(lchip, ctc_oid.value, CTC_PORT_PROP_L3PDU_ARP_ACTION, CTC_PORT_ARP_ACTION_TYPE_FW);
            ctcs_port_set_property(lchip, ctc_oid.value, CTC_PORT_PROP_L3PDU_DHCP_ACTION, CTC_PORT_ARP_ACTION_TYPE_FW);
            ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_L2PDU_ACTION_INDEX_BPDU, CTC_PDU_L2PDU_ACTION_TYPE_FWD);
            ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_L2PDU_ACTION_INDEX_SLOW_PROTO, CTC_PDU_L2PDU_ACTION_TYPE_FWD);
            ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_L2PDU_ACTION_INDEX_EAPOL, CTC_PDU_L2PDU_ACTION_TYPE_FWD);
            ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_L2PDU_ACTION_INDEX_LLDP, CTC_PDU_L2PDU_ACTION_TYPE_FWD);
            ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX, CTC_PDU_L2PDU_ACTION_TYPE_FWD);
            ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX, CTC_PDU_L2PDU_ACTION_TYPE_FWD);
            ctcs_l2pdu_set_port_action(lchip, ctc_oid.value, CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX, CTC_PDU_L2PDU_ACTION_TYPE_FWD);
        }
        else if (SAI_OBJECT_TYPE_LAG == ctc_oid.type)
        {
            ctc_sai_lag_notification_all_members_change(lchip, CTC_SAI_LAG_MEM_CHANGE_TYPE_HOSTIF, ctc_oid.value, false);
        }
        else if (SAI_OBJECT_TYPE_VLAN == ctc_oid.type)
        {
            ctcs_vlan_set_property(lchip, ctc_oid.value, CTC_VLAN_PROP_ARP_EXCP_TYPE, CTC_EXCP_NORMAL_FWD);
            ctcs_vlan_set_property(lchip, ctc_oid.value, CTC_VLAN_PROP_DHCP_EXCP_TYPE, CTC_EXCP_NORMAL_FWD);
        }
        epoll_ctl(p_switch_master->epoll_sock, EPOLL_CTL_DEL, p_hostif_port->fd, &p_switch_master->evl);
    }
    else
    {
        close(p_hostif_port->fd);
    }
roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);

    _ctc_sai_hostif_free_hostif(p_hostif_port);

    return status;
}

sai_status_t
ctc_sai_hostif_remove_hostif(
        _In_ sai_object_id_t hostif_id)
{
    ctc_object_id_t ctc_oid;
    char ifname[30];
    ctc_sai_hostif_t* p_hostif_port = NULL;
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&ifname, 0, sizeof(ifname));
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF, hostif_id, &ctc_oid));
    lchip = ctc_oid.lchip;

    CTC_SAI_DB_LOCK(lchip);
    p_hostif_port = ctc_sai_db_get_object_property(lchip, hostif_id);
    if (NULL == p_hostif_port)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if (SAI_HOSTIF_TYPE_NETDEV == p_hostif_port->hostif_type)
    {
        /* vlan interface process */
        if (SAI_OBJECT_TYPE_VLAN == p_hostif_port->port_type)
        {
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VLAN, p_hostif_port->port_id, &ctc_oid);
            ctcs_vlan_set_arp_excp_type(lchip, ctc_oid.value, CTC_EXCP_NORMAL_FWD);
        }
        if (SAI_OBJECT_TYPE_PORT == p_hostif_port->port_type)
        {
            ctc_acl_property_t acl_prop;

            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.acl_priority = CTC_SAI_DEFAULT_ACL_HOST_IF_PRIORITY;
            acl_prop.acl_en = 0;
            acl_prop.direction = CTC_INGRESS;
            acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_COPP;
            ctcs_port_set_acl_property(lchip, ctc_oid.value, &acl_prop);
        }
        else if (SAI_OBJECT_TYPE_LAG == p_hostif_port->port_type)
        {
            ctc_sai_lag_notification_all_members_change(lchip, CTC_SAI_LAG_MEM_CHANGE_TYPE_HOSTIF, ctc_oid.value, false);
        }
        else if (SAI_OBJECT_TYPE_VLAN == p_hostif_port->port_type)
        {
            ctc_acl_property_t acl_prop;

            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.acl_priority = CTC_SAI_DEFAULT_ACL_HOST_IF_PRIORITY;
            acl_prop.acl_en = 0;
            acl_prop.direction = CTC_INGRESS;
            acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_COPP;
            ctcs_vlan_set_acl_property(lchip, ctc_oid.value, &acl_prop);
        }

        /* remove fd from epoll socket list */
        epoll_ctl(p_switch_master->epoll_sock, EPOLL_CTL_DEL, p_hostif_port->fd, &p_switch_master->evl);

        /* remove net device from linux kernel */
        _ctc_sai_hostif_remove_net_device(p_hostif_port->fd);

    }
    else
    {
        close(p_hostif_port->fd);
    }
    ctc_sai_db_remove_object_property(lchip, hostif_id);
    _ctc_sai_hostif_free_hostif(p_hostif_port);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_hostif_get_hostif_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_t* p_hostif_port = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_hostif_port = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_hostif_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "object id %"PRIx64" get hostif port attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_HOSTIF_ATTR_TYPE:
            attr->value.s32 = p_hostif_port->hostif_type;
            break;
        case SAI_HOSTIF_ATTR_OBJ_ID:
            if (SAI_HOSTIF_TYPE_FD == p_hostif_port->hostif_type)
            {
                CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "The hostif fd not support get port object id\n");
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            }
            if (SAI_OBJECT_TYPE_PORT == p_hostif_port->port_type)
            {
               attr->value.oid = p_hostif_port->port_id;
            }
            else if (SAI_OBJECT_TYPE_LAG == p_hostif_port->port_type)
            {
                attr->value.oid = p_hostif_port->port_id;
            }
            else if (SAI_OBJECT_TYPE_VLAN == p_hostif_port->port_type)
            {
                attr->value.oid = p_hostif_port->port_id;
            }
            break;
        case SAI_HOSTIF_ATTR_NAME:
            if (SAI_HOSTIF_TYPE_FD == p_hostif_port->hostif_type)
            {
                CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "The hostif fd not support get port object id\n");
                 return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            }
            sal_memcpy(attr->value.chardata, p_hostif_port->ifname, sizeof(p_hostif_port->ifname));
            break;
        case SAI_HOSTIF_ATTR_OPER_STATUS:
            attr->value.booldata = p_hostif_port->oper_status;
            break;
        case SAI_HOSTIF_ATTR_QUEUE:
            attr->value.u32 = p_hostif_port->queue_id;
            break;
        case SAI_HOSTIF_ATTR_VLAN_TAG:
            attr->value.s32 = p_hostif_port->vlan_tag;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static sai_status_t
ctc_sai_hostif_set_hostif_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_t* p_hostif_port = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_hostif_port = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_hostif_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "object id %"PRIx64" set hostif port attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_HOSTIF_ATTR_TYPE:
        case SAI_HOSTIF_ATTR_OBJ_ID:
        case SAI_HOSTIF_ATTR_NAME:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_HOSTIF_ATTR_OPER_STATUS:
            CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_oper_status(p_hostif_port->ifname, attr->value.booldata));
            p_hostif_port->oper_status = attr->value.booldata;
            break;
        case SAI_HOSTIF_ATTR_QUEUE:
            p_hostif_port->queue_id = attr->value.u32;
            break;
        case SAI_HOSTIF_ATTR_VLAN_TAG:
            if (attr->value.s32 > SAI_HOSTIF_VLAN_TAG_ORIGINAL)
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0;
            }
            p_hostif_port->vlan_tag = attr->value.s32;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t hostif_attr_fn_entries[] = {
    {SAI_HOSTIF_ATTR_TYPE, ctc_sai_hostif_get_hostif_property, NULL},
    {SAI_HOSTIF_ATTR_OBJ_ID, ctc_sai_hostif_get_hostif_property, NULL},
    {SAI_HOSTIF_ATTR_NAME, ctc_sai_hostif_get_hostif_property, NULL},
    {SAI_HOSTIF_ATTR_OPER_STATUS, ctc_sai_hostif_get_hostif_property, ctc_sai_hostif_set_hostif_property},
    {SAI_HOSTIF_ATTR_QUEUE, ctc_sai_hostif_get_hostif_property, ctc_sai_hostif_set_hostif_property},
    {SAI_HOSTIF_ATTR_VLAN_TAG, ctc_sai_hostif_get_hostif_property, ctc_sai_hostif_set_hostif_property},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

sai_status_t
ctc_sai_hostif_set_hostif_attribute(
        _In_ sai_object_id_t hostif_id,
        _In_ const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = hostif_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_HOSTIF, hostif_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

sai_status_t
ctc_sai_hostif_get_hostif_attribute(
        _In_ sai_object_id_t hostif_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = hostif_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_HOSTIF, loop, hostif_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________HOSTIF_TABLE_______

static sai_status_t
_ctc_sai_hostif_alloc_hostif_table(ctc_sai_hostif_table_t** p_hostif_table)
{
    ctc_sai_hostif_table_t* p_hostif_table_temp = NULL;

    p_hostif_table_temp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_hostif_table_t));
    if (NULL == p_hostif_table_temp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_hostif_table_temp, 0, sizeof(ctc_sai_hostif_table_t));

    *p_hostif_table = p_hostif_table_temp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_free_hostif_table(ctc_sai_hostif_table_t* p_hostif_table)
{
    mem_free(p_hostif_table);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_hostif_create_hostif_table_entry(
        _Out_ sai_object_id_t *hostif_table_entry_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_table_t* p_hostif_table = NULL;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val = NULL, *attr_type_val = NULL;
    uint32 attr_idx    = 0;
    uint32 attr_type_idx    = 0;
    sai_object_type_t type = 0;

    CTC_SAI_PTR_VALID_CHECK(hostif_table_entry_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_alloc_hostif_table(&p_hostif_table));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE, &attr_type_val, &attr_type_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_hostif_table->hostif_table_type = attr_type_val->s32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif table entry type on create of hostif table\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }

    if ((SAI_HOSTIF_TABLE_ENTRY_TYPE_PORT == attr_type_val->s32) || (SAI_HOSTIF_TABLE_ENTRY_TYPE_LAG == attr_type_val->s32)
        || (SAI_HOSTIF_TABLE_ENTRY_TYPE_VLAN == attr_type_val->s32))
     {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_hostif_table->obj_id = attr_val->oid;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif table obj id on create of hostif table\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_0;
        }
        CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_type(attr_val->oid, &type), status, roll_back_0);
        if (((SAI_HOSTIF_TABLE_ENTRY_TYPE_PORT == attr_type_val->s32) && (SAI_OBJECT_TYPE_PORT != type))
            || ((SAI_HOSTIF_TABLE_ENTRY_TYPE_LAG == attr_type_val->s32) && (SAI_OBJECT_TYPE_LAG != type))
            || ((SAI_HOSTIF_TABLE_ENTRY_TYPE_VLAN == attr_type_val->s32) && (SAI_OBJECT_TYPE_VLAN != type)))
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif table entry obj id type not right on create of hostif table\n");
            status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            goto roll_back_0;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_hostif_table->trap_id = attr_val->oid;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif table trap id on create of hostif table\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_0;
        }
    }
    else if (SAI_HOSTIF_TABLE_ENTRY_TYPE_TRAP_ID == attr_type_val->s32)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_hostif_table->trap_id = attr_val->oid;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif table trap id on create of hostif table\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_0;
        }
    }
    else if (SAI_HOSTIF_TABLE_ENTRY_TYPE_WILDCARD == attr_type_val->s32)
    {

    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif table entry type not right on create of hostif table\n");
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_type_idx;
        goto roll_back_0;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_hostif_table->channel_type = attr_val->s32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif table channel type on create of hostif table\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }

    if ( SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_FD == p_hostif_table->channel_type)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TABLE_ENTRY_ATTR_HOST_IF, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_hostif_table->hostif_id = attr_val->oid;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif table hostif id on create of hostif table\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_0;
        }
    }

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &p_hostif_table->hostif_table_id), status, roll_back_1);
    *hostif_table_entry_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY, lchip, 0, 0, p_hostif_table->hostif_table_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *hostif_table_entry_id, p_hostif_table), status, roll_back_2);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_hostif_table->hostif_table_id);
roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);
roll_back_0:
    _ctc_sai_hostif_free_hostif_table(p_hostif_table);
    return status;
}

sai_status_t
ctc_sai_hostif_remove_hostif_table_entry(
        _In_ sai_object_id_t hostif_table_entry_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    ctc_sai_hostif_table_t* p_hostif_table = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY, hostif_table_entry_id, &ctc_oid));
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    p_hostif_table = ctc_sai_db_get_object_property(lchip, hostif_table_entry_id);
    if (NULL == p_hostif_table)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    ctc_sai_db_remove_object_property(lchip, hostif_table_entry_id);
    CTC_SAI_DB_UNLOCK(lchip);
    _ctc_sai_hostif_free_hostif_table(p_hostif_table);

    return status;
}

static sai_status_t
ctc_sai_hostif_get_hostif_table_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_table_t* p_hostif_table = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_hostif_table = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_hostif_table)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "object id %"PRIx64" get hostif table entry attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE:
            attr->value.s32 = p_hostif_table->hostif_table_type;
            break;
        case SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID:
            attr->value.oid = p_hostif_table->obj_id;
            break;
        case SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID:
            attr->value.oid = p_hostif_table->trap_id;
            break;
        case SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE:
            attr->value.s32 = p_hostif_table->channel_type;
            break;
        case SAI_HOSTIF_TABLE_ENTRY_ATTR_HOST_IF:
            attr->value.oid = p_hostif_table->hostif_id;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif table entry attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t hostif_table_attr_fn_entries[] = {
    {SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE, ctc_sai_hostif_get_hostif_table_property, NULL},
    {SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID, ctc_sai_hostif_get_hostif_table_property, NULL},
    {SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID, ctc_sai_hostif_get_hostif_table_property, NULL},
    {SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE, ctc_sai_hostif_get_hostif_table_property, NULL},
    {SAI_HOSTIF_TABLE_ENTRY_ATTR_HOST_IF, ctc_sai_hostif_get_hostif_table_property, NULL},
    {CTC_SAI_FUNC_ATTR_END_ID, ctc_sai_hostif_get_hostif_table_property, NULL}
};

sai_status_t
ctc_sai_hostif_set_hostif_table_entry_attribute(
        _In_ sai_object_id_t hostif_table_entry_id,
        _In_ const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = hostif_table_entry_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_table_entry_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_table_entry_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_HOSTIF, hostif_table_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

sai_status_t
ctc_sai_hostif_get_hostif_table_entry_attribute(
        _In_ sai_object_id_t hostif_table_entry_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = hostif_table_entry_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_table_entry_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_table_entry_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_HOSTIF, loop, hostif_table_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________HOSTIF_TRAP_GROUP_______

static sai_status_t
_ctc_sai_hostif_alloc_trap_group(ctc_sai_hostif_trap_group_t** p_trap_group)
{
    ctc_sai_hostif_trap_group_t* p_trap_group_temp = NULL;

    p_trap_group_temp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_hostif_trap_group_t));
    if (NULL == p_trap_group_temp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_trap_group_temp, 0, sizeof(ctc_sai_hostif_trap_group_t));

    *p_trap_group = p_trap_group_temp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_free_trap_group(ctc_sai_hostif_trap_group_t* p_trap_group)
{
    mem_free(p_trap_group);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_hostif_create_hostif_trap_group(
        _Out_ sai_object_id_t *hostif_trap_group_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_trap_group_t* p_trap_group = NULL;
    uint8 lchip = 0;
    const sai_attribute_value_t* attr_val = NULL;
    uint32 attr_idx    = 0;

    CTC_SAI_PTR_VALID_CHECK(hostif_trap_group_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_alloc_trap_group(&p_trap_group));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_trap_group->admin_sate = attr_val->booldata;
    }
    else
    {
        p_trap_group->admin_sate = true;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_trap_group->queue_id = attr_val->u32;
    }
    else
    {
        p_trap_group->queue_id = 0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_trap_group->policer_id = attr_val->oid;
    }
    else
    {
        p_trap_group->policer_id = SAI_NULL_OBJECT_ID;
    }

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &p_trap_group->hostif_group_id), status, roll_back_1);
    *hostif_trap_group_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP, lchip, 0, 0, p_trap_group->hostif_group_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *hostif_trap_group_id, p_trap_group), status, roll_back_2);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;

roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_trap_group->hostif_group_id);
roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);
    _ctc_sai_hostif_free_trap_group(p_trap_group);

    return status;
}

sai_status_t
ctc_sai_hostif_remove_hostif_trap_group(
        _In_ sai_object_id_t hostif_trap_group_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_hostif_trap_group_t* p_trap_group = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP, hostif_trap_group_id, &ctc_oid));
    CTC_SAI_DB_LOCK(lchip);
    lchip = ctc_oid.lchip;
    p_trap_group = ctc_sai_db_get_object_property(lchip, hostif_trap_group_id);
    if (NULL == p_trap_group)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    ctc_sai_db_remove_object_property(lchip, hostif_trap_group_id);
    CTC_SAI_DB_UNLOCK(lchip);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_trap_group->hostif_group_id);

    _ctc_sai_hostif_free_trap_group(p_trap_group);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_hostif_get_trap_group_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_trap_group_t* p_trap_group = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_trap_group = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_trap_group)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "object id %"PRIx64" get hostif trap group attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE:
            attr->value.booldata = p_trap_group->admin_sate;
            break;
        case SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE:
            attr->value.u32 = p_trap_group->queue_id;
            break;
        case SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER:
            attr->value.oid = p_trap_group->policer_id;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif trap group attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

sai_status_t
_ctc_sai_hostif_add_acl_qos_info(uint8 lchip, ctc_sai_hostif_trap_t* p_hostif_trap)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_qos_queue_cfg_t    qos_queue_cfg;
    ctc_acl_field_action_t action_field;
    ctc_sai_hostif_trap_group_t* p_trap_group = NULL;
    ctc_object_id_t ctc_oid;
    sai_object_id_t policer_id = 0;
    uint32 ctc_policer_id = 0;
    uint32 queue_id = 0;
    uint8 chip_type = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_trap_group = ctc_sai_db_get_object_property(lchip, p_hostif_trap->hostif_group_id);
    if (NULL == p_trap_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "hostif trap group id is error, when create hostif trap!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_POLICER, p_trap_group->policer_id, &ctc_oid);
    ctc_policer_id = ctc_oid.value;
    policer_id = p_trap_group->admin_sate?p_trap_group->policer_id:SAI_NULL_OBJECT_ID;
    queue_id = p_trap_group->admin_sate?p_trap_group->queue_id:0;

    sal_memset(&qos_queue_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
    qos_queue_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_REASON_MAP;
    qos_queue_cfg.value.reason_map.cpu_reason = p_hostif_trap->custom_reason_id;
    qos_queue_cfg.value.reason_map.queue_id = queue_id%CTC_SAI_CPU_MAX_QNUM_PER_GROUP;
    qos_queue_cfg.value.reason_map.reason_group = queue_id/CTC_SAI_CPU_MAX_QNUM_PER_GROUP;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &qos_queue_cfg));

    sal_memset(&qos_queue_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
    qos_queue_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_REASON_DEST;
    qos_queue_cfg.value.reason_dest.cpu_reason = p_hostif_trap->custom_reason_id;
    qos_queue_cfg.value.reason_dest.dest_port = 0;
    qos_queue_cfg.value.reason_dest.dest_type = CTC_PKT_CPU_REASON_TO_LOCAL_CPU;
    if (CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CPU_ETH_EN))
    {
        qos_queue_cfg.value.reason_dest.dest_port = p_switch_master->cpu_eth_port;
        qos_queue_cfg.value.reason_dest.dest_type = CTC_PKT_CPU_REASON_TO_LOCAL_PORT;
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &qos_queue_cfg));

    if (CTC_PKT_CPU_REASON_SFLOW_SOURCE == p_hostif_trap->custom_reason_id)
    {
        sal_memset(&qos_queue_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
        qos_queue_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_REASON_MAP;
        qos_queue_cfg.value.reason_map.cpu_reason = p_hostif_trap->custom_reason_id+1;
        qos_queue_cfg.value.reason_map.queue_id = queue_id%CTC_SAI_CPU_MAX_QNUM_PER_GROUP;
        qos_queue_cfg.value.reason_map.reason_group = queue_id/CTC_SAI_CPU_MAX_QNUM_PER_GROUP;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &qos_queue_cfg));

        sal_memset(&qos_queue_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
        qos_queue_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_REASON_DEST;
        qos_queue_cfg.value.reason_dest.cpu_reason = p_hostif_trap->custom_reason_id+1;
        qos_queue_cfg.value.reason_dest.dest_port = 0;
        qos_queue_cfg.value.reason_dest.dest_type = CTC_PKT_CPU_REASON_TO_LOCAL_CPU;
        if (CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CPU_ETH_EN))
        {
            qos_queue_cfg.value.reason_dest.dest_port = p_switch_master->cpu_eth_port;
            qos_queue_cfg.value.reason_dest.dest_type = CTC_PKT_CPU_REASON_TO_LOCAL_PORT;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &qos_queue_cfg));
    }

    if(SAI_NULL_OBJECT_ID != p_hostif_trap->counter_id)
    {
        chip_type = ctcs_get_chip_type(lchip);
        if (CTC_CHIP_TSINGMA == chip_type)
        {
            sal_memset(&qos_queue_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
            qos_queue_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_STATS_EN;
            qos_queue_cfg.value.stats.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
            qos_queue_cfg.value.stats.queue.cpu_reason = p_hostif_trap->custom_reason_id;
            qos_queue_cfg.value.stats.queue.queue_id = queue_id%CTC_SAI_CPU_MAX_QNUM_PER_GROUP;
            qos_queue_cfg.value.stats.stats_en = 1;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &qos_queue_cfg));
        }
        CTC_SAI_CTC_ERROR_RETURN(ctc_sai_counter_id_hostif_trap_create(p_hostif_trap->counter_id, CTC_SAI_COUNTER_TYPE_HOSTIF,
                                 qos_queue_cfg.value.stats.queue.cpu_reason, qos_queue_cfg.value.stats.queue.queue_id));
    }

    if (SAI_NULL_OBJECT_ID == policer_id)
    {
        return SAI_STATUS_SUCCESS;
    }

    if (CTC_SAI_NOT_NORMAL_EXCEP(p_hostif_trap->custom_reason_id) || (CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip)))
    {
        ctc_qos_shape_t qos_shape;
        ctc_qos_sched_t sched;
        ctc_sai_policer_db_t* p_policer_db = NULL;

        p_policer_db = ctc_sai_db_get_object_property(lchip, policer_id);
        if (NULL == p_policer_db)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }

        sal_memset(&qos_shape, 0, sizeof(ctc_qos_shape_t));
        qos_shape.type = CTC_QOS_SHAPE_QUEUE;
        qos_shape.shape.queue_shape.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
        qos_shape.shape.queue_shape.queue.cpu_reason = p_hostif_trap->custom_reason_id;
        qos_shape.shape.queue_shape.enable = TRUE;
        qos_shape.shape.queue_shape.pir = p_policer_db->cir;
        qos_shape.shape.queue_shape.pbs = CTC_QOS_SHP_TOKE_THRD_DEFAULT;
        qos_shape.shape.queue_shape.cir = p_policer_db->cir;
        qos_shape.shape.queue_shape.cbs = CTC_QOS_SHP_TOKE_THRD_DEFAULT;
        ctcs_qos_set_shape(lchip, &qos_shape);

        sal_memset (&sched, 0, sizeof(ctc_qos_sched_t));
        sched.type = CTC_QOS_SCHED_QUEUE;
        sched.sched.queue_sched.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
        sched.sched.queue_sched.queue.queue_id = 0;
        sched.sched.queue_sched.queue.cpu_reason = p_hostif_trap->custom_reason_id;
        sched.sched.queue_sched.confirm_class = 6;
        sched.sched.queue_sched.exceed_class = 6;

        /*set confirm class*/
        sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_CONFIRM_CLASS;
        ctcs_qos_set_sched(lchip, &sched);

        /*set exceed class*/
        sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_EXCEED_CLASS;
        ctcs_qos_set_sched(lchip, &sched);

        if (CTC_PKT_CPU_REASON_SFLOW_SOURCE == p_hostif_trap->custom_reason_id)
        {
            sal_memset(&qos_shape, 0, sizeof(ctc_qos_shape_t));
            qos_shape.type = CTC_QOS_SHAPE_QUEUE;
            qos_shape.shape.queue_shape.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
            qos_shape.shape.queue_shape.queue.cpu_reason = p_hostif_trap->custom_reason_id+1;
            qos_shape.shape.queue_shape.enable = TRUE;
            qos_shape.shape.queue_shape.pir = p_policer_db->cir;
            qos_shape.shape.queue_shape.pbs = CTC_QOS_SHP_TOKE_THRD_DEFAULT;
            qos_shape.shape.queue_shape.cir = p_policer_db->cir;
            qos_shape.shape.queue_shape.cbs = CTC_QOS_SHP_TOKE_THRD_DEFAULT;
            ctcs_qos_set_shape(lchip, &qos_shape);

            sal_memset (&sched, 0, sizeof(ctc_qos_sched_t));
            sched.type = CTC_QOS_SCHED_QUEUE;
            sched.sched.queue_sched.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
            sched.sched.queue_sched.queue.queue_id = 0;
            sched.sched.queue_sched.queue.cpu_reason = p_hostif_trap->custom_reason_id+1;
            sched.sched.queue_sched.confirm_class = 6;
            sched.sched.queue_sched.exceed_class = 6;

            /*set confirm class*/
            sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_CONFIRM_CLASS;
            ctcs_qos_set_sched(lchip, &sched);

            /*set exceed class*/
            sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_EXCEED_CLASS;
            ctcs_qos_set_sched(lchip, &sched);
        }
    }
    else
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_policer_set_copp_policer(lchip, ctc_policer_id, true));

        sal_memset(&action_field, 0, sizeof(ctc_acl_field_action_t));
        action_field.type = CTC_ACL_FIELD_ACTION_COPP;
        action_field.data0 = ctc_policer_id;
        CTC_SAI_ERROR_GOTO(ctcs_acl_add_action_field(lchip, p_hostif_trap->acl_match_entry_id, &action_field), status, roll_back_0);
    }

    return SAI_STATUS_SUCCESS;

roll_back_0:
    ctc_sai_policer_set_copp_policer(lchip, ctc_policer_id, false);

    return status;
}

sai_status_t
_ctc_sai_hostif_remove_acl_qos_info(uint8 lchip, ctc_sai_hostif_trap_t* p_hostif_trap)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_trap_group_t* p_trap_group = NULL;
    ctc_object_id_t ctc_oid;
    uint32 policer_id = 0;
    uint8 chip_type = 0;
    ctc_qos_queue_cfg_t    qos_queue_cfg;
    ctc_acl_field_action_t action_field;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    sal_memset(&qos_queue_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
    qos_queue_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_REASON_MAP;
    qos_queue_cfg.value.reason_map.cpu_reason = p_hostif_trap->custom_reason_id;
    qos_queue_cfg.value.reason_map.queue_id = 0;
    qos_queue_cfg.value.reason_map.reason_group = 0;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &qos_queue_cfg));

    if (CTC_PKT_CPU_REASON_SFLOW_SOURCE == p_hostif_trap->custom_reason_id)
    {
        sal_memset(&qos_queue_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
        qos_queue_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_REASON_MAP;
        qos_queue_cfg.value.reason_map.cpu_reason = p_hostif_trap->custom_reason_id+1;
        qos_queue_cfg.value.reason_map.queue_id = 0;
        qos_queue_cfg.value.reason_map.reason_group = 0;
        ctcs_qos_set_queue(lchip, &qos_queue_cfg);
    }

    if(SAI_NULL_OBJECT_ID != p_hostif_trap->counter_id)
    {
        chip_type = ctcs_get_chip_type(lchip);
        if (CTC_CHIP_TSINGMA == chip_type)
        {
            sal_memset(&qos_queue_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
            qos_queue_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_STATS_EN;
            qos_queue_cfg.value.stats.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
            qos_queue_cfg.value.stats.queue.cpu_reason = p_hostif_trap->custom_reason_id;
            qos_queue_cfg.value.stats.queue.queue_id = 0;
            qos_queue_cfg.value.stats.stats_en = 0;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &qos_queue_cfg));
        }
        CTC_SAI_CTC_ERROR_RETURN(ctc_sai_counter_id_hostif_trap_remove(p_hostif_trap->counter_id, CTC_SAI_COUNTER_TYPE_HOSTIF));
    }

    p_trap_group = ctc_sai_db_get_object_property(lchip, p_hostif_trap->hostif_group_id);
    if ((NULL != p_trap_group) && (SAI_NULL_OBJECT_ID != p_trap_group->policer_id))
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_POLICER, p_trap_group->policer_id, &ctc_oid);
        policer_id = ctc_oid.value;

        if (CTC_SAI_NOT_NORMAL_EXCEP(p_hostif_trap->custom_reason_id) || (CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip)))
        {
            ctc_qos_shape_t qos_shape;
            ctc_sai_policer_db_t* p_policer_db = NULL;

            p_policer_db = ctc_sai_db_get_object_property(lchip, policer_id);
            if (NULL == p_policer_db)
            {
                return SAI_STATUS_ITEM_NOT_FOUND;
            }

            sal_memset(&qos_shape, 0, sizeof(ctc_qos_shape_t));
            qos_shape.type = CTC_QOS_SHAPE_QUEUE;
            qos_shape.shape.queue_shape.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
            qos_shape.shape.queue_shape.queue.cpu_reason = p_hostif_trap->custom_reason_id;
            qos_shape.shape.queue_shape.enable = FALSE;
            qos_shape.shape.queue_shape.pir = p_policer_db->cir;
            qos_shape.shape.queue_shape.pbs = CTC_QOS_SHP_TOKE_THRD_DEFAULT;
            qos_shape.shape.queue_shape.cir = p_policer_db->cir;
            qos_shape.shape.queue_shape.cbs = CTC_QOS_SHP_TOKE_THRD_DEFAULT;
            ctcs_qos_set_shape(lchip, &qos_shape);

            if (CTC_PKT_CPU_REASON_SFLOW_SOURCE == p_hostif_trap->custom_reason_id)
            {
                sal_memset(&qos_shape, 0, sizeof(ctc_qos_shape_t));
                qos_shape.type = CTC_QOS_SHAPE_QUEUE;
                qos_shape.shape.queue_shape.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
                qos_shape.shape.queue_shape.queue.cpu_reason = p_hostif_trap->custom_reason_id;
                qos_shape.shape.queue_shape.enable = FALSE;
                qos_shape.shape.queue_shape.pir = p_policer_db->cir;
                qos_shape.shape.queue_shape.pbs = CTC_QOS_SHP_TOKE_THRD_DEFAULT;
                qos_shape.shape.queue_shape.cir = p_policer_db->cir;
                qos_shape.shape.queue_shape.cbs = CTC_QOS_SHP_TOKE_THRD_DEFAULT;
                ctcs_qos_set_shape(lchip, &qos_shape);
            }
        }
        else
        {
            sal_memset(&action_field, 0, sizeof(ctc_acl_field_action_t));

            action_field.type = CTC_ACL_FIELD_ACTION_COPP;
            action_field.data0 = 0;
            ctcs_acl_remove_action_field(lchip, p_hostif_trap->acl_match_entry_id, &action_field);

            ctc_sai_policer_set_copp_policer(lchip, policer_id, false);
        }
    }

    return status;
}

static sai_status_t
_ctc_sai_hostif_cmp_trap_group(ctc_sai_oid_property_t* bucket_data, ctc_sai_hostif_lookup_t* user_data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_trap_group_t* p_trap_group = (ctc_sai_hostif_trap_group_t*)user_data;
    sai_object_id_t oid = 0;
    ctc_sai_hostif_trap_t* p_hostif_trap = (ctc_sai_hostif_trap_t*)bucket_data->data;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(bucket_data->oid, &lchip));
    oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP, lchip, 0, 0, p_trap_group->hostif_group_id);

    if (p_hostif_trap->hostif_group_id == oid)
    {
        if (p_trap_group->admin_sate)
        {
            _ctc_sai_hostif_add_acl_qos_info(lchip, p_hostif_trap);
        }
        else
        {
            _ctc_sai_hostif_remove_acl_qos_info(lchip, p_hostif_trap);
        }
    }

    return status;
}

static sai_status_t
ctc_sai_hostif_set_trap_group_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_trap_group_t* p_trap_group = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);


    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_trap_group = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_trap_group)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "object id %"PRIx64" set hostif trap group attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE:
            p_trap_group->admin_sate = attr->value.booldata;
            break;
        case SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE:
            p_trap_group->queue_id = attr->value.u32;
            break;
        case SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER:
            p_trap_group->policer_id = attr->value.oid;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif trap group attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HOSTIF_TRAP, (hash_traversal_fn)_ctc_sai_hostif_cmp_trap_group, (void*)p_trap_group);
    return status;
}

static ctc_sai_attr_fn_entry_t hostif_trap_group_attr_fn_entries[] = {
    {SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE, ctc_sai_hostif_get_trap_group_property, ctc_sai_hostif_set_trap_group_property},
    {SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE, ctc_sai_hostif_get_trap_group_property, ctc_sai_hostif_set_trap_group_property},
    {SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER, ctc_sai_hostif_get_trap_group_property, ctc_sai_hostif_set_trap_group_property},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

sai_status_t
ctc_sai_hostif_set_hostif_trap_group_attribute(
        _In_ sai_object_id_t hostif_trap_group_id,
        _In_ const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = hostif_trap_group_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_trap_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_trap_group_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_HOSTIF, hostif_trap_group_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

sai_status_t
ctc_sai_hostif_get_hostif_trap_group_attribute(
        _In_ sai_object_id_t hostif_trap_group_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = hostif_trap_group_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_trap_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_trap_group_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_HOSTIF, loop, hostif_trap_group_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________HOSTIF_TRAP_______

static sai_status_t
_ctc_sai_hostif_alloc_trap(ctc_sai_hostif_trap_t** p_trap)
{
    ctc_sai_hostif_trap_t* p_trap_temp = NULL;

    p_trap_temp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_hostif_trap_t));
    if (NULL == p_trap_temp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_trap_temp, 0, sizeof(ctc_sai_hostif_trap_t));

    *p_trap = p_trap_temp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_free_trap(ctc_sai_hostif_trap_t* p_trap)
{

    if (p_trap->exclude_port_list.list)
    {
        mem_free(p_trap->exclude_port_list.list);
    }

    mem_free(p_trap);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_hostif_add_acl_field(uint8 lchip, uint32 entry_id, uint32 custom_reason_id)
{
    bool is_drop = false;
    ctc_field_key_t key_field;
    ctc_acl_field_action_t action_field;
    ctc_acl_to_cpu_t acl_cpu;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    switch(custom_reason_id)
    {
        /* switch trap */
        case CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_BPDU: /*SAI_HOSTIF_TRAP_TYPE_STP*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_BPDU;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        case CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_SLOW_PROTO: /*SAI_HOSTIF_TRAP_TYPE_LACP*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_SLOW_PROTO;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        case CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_EAPOL: /*SAI_HOSTIF_TRAP_TYPE_EAPOL*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_EAPOL;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        case CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_LLDP: /*SAI_HOSTIF_TRAP_TYPE_LLDP*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_LLDP;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        case CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX: /*SAI_HOSTIF_TRAP_TYPE_PVRST*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

            /* ACL_IGMP_TYPE_HOST_QUERY                 0x11
               ACL_IGMP_TYPE_HOST_REPORT                0x12
               ACL_IGMP_TYPE_HOST_DVMRP                 0x13
               ACL_IGMP_TYPE_PIM                        0x14
               ACL_IGMP_TYPE_TRACE                      0x15
               ACL_IGMP_TYPE_V2_REPORT                  0x16
               ACL_IGMP_TYPE_V2_LEAVE                   0x17
               ACL_IGMP_TYPE_MTRACE                     0x1f
               ACL_IGMP_TYPE_MTRACE_RESPONSE            0x1e
               ACL_IGMP_TYPE_PRECEDENCE                 0
               ACL_IGMP_TYPE_V3_REPORT                  0x22*/
        case CTC_PKT_CPU_REASON_IGMP_SNOOPING: /*SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_QUERY*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_LEAVE: /*SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_LEAVE*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L3_TYPE;
            key_field.data = CTC_PARSER_L3_TYPE_IPV4;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L4_TYPE;
            key_field.data = CTC_PARSER_L4_TYPE_IGMP;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IGMP_TYPE;
            key_field.data = 0x17;
            key_field.mask = 0xFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_V1_REPORT: /*SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V1_REPORT*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L3_TYPE;
            key_field.data = CTC_PARSER_L3_TYPE_IPV4;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L4_TYPE;
            key_field.data = CTC_PARSER_L4_TYPE_IGMP;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IGMP_TYPE;
            key_field.data = 0x12;
            key_field.mask = 0xFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_V2_REPORT: /*SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V2_REPORT*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L3_TYPE;
            key_field.data = CTC_PARSER_L3_TYPE_IPV4;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L4_TYPE;
            key_field.data = CTC_PARSER_L4_TYPE_IGMP;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IGMP_TYPE;
            key_field.data = 0x16;
            key_field.mask = 0xFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_V3_REPORT: /*SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V3_REPORT*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_IGMP_SNOOPING;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L3_TYPE;
            key_field.data = CTC_PARSER_L3_TYPE_IPV4;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L4_TYPE;
            key_field.data = CTC_PARSER_L4_TYPE_IGMP;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IGMP_TYPE;
            key_field.data = 0x22;
            key_field.mask = 0xFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_SFLOW_SOURCE: /*SAI_HOSTIF_TRAP_TYPE_SAMPLEPACKET*/
            /*sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_SFLOW_SOURCE;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK&0xFFFE;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;*/
            break;

        case CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX: /*SAI_HOSTIF_TRAP_TYPE_UDLD*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

         case CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_CDP_INDEX: /* SAI_HOSTIF_TRAP_TYPE_CDP */
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_CDP_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

         case CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_VTP_INDEX: /* SAI_HOSTIF_TRAP_TYPE_VTP */
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_VTP_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        case CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_DTP_INDEX: /* SAI_HOSTIF_TRAP_TYPE_DTP */
            return SAI_STATUS_NOT_SUPPORTED;

        case CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_PAGP_INDEX: /* SAI_HOSTIF_TRAP_TYPE_PAGP */
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_PAGP_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        /* router trap */
        /*arp request:0x0001 arp response:0x0002*/
        case CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ARP: /*SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ARP;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_ARP_RESPONSE: /*SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ARP;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L3_TYPE;
            key_field.data = CTC_PARSER_L3_TYPE_ARP;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_ARP_OP_CODE;
            key_field.data = 0x0002;
            key_field.mask = 0xFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_DHCP: /*SAI_HOSTIF_TRAP_TYPE_DHCP*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_DHCP;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_OSPF: /*I_HOSTIF_TRAP_TYPE_OSPF*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_OSPF;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_L3_PDU + SAI_HOSTIF_TRAP_TYPE_PIM: /*SAI_HOSTIF_TRAP_TYPE_PIM*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + SAI_HOSTIF_TRAP_TYPE_PIM;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_VRRP: /*SAI_HOSTIF_TRAP_TYPE_VRRP*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_VRRP;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_DHCPV6: /*SAI_HOSTIF_TRAP_TYPE_DHCPV6*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_DHCP;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L3_TYPE;
            key_field.data = CTC_PARSER_L3_TYPE_IPV6;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_OSPFV6_INDEX: /*SAI_HOSTIF_TRAP_TYPE_OSPFV6*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_OSPFV6_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_VRRPV6_INDEX: /*SAI_HOSTIF_TRAP_TYPE_VRRPV6*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_VRRPV6_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ICMPV6: /*SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ICMPV6;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_IPV6_MLD_V1_V2: /*SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_V2*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_PIM;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_IPV6_MLD_V1_REPORT: /*SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_REPORT*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L3_TYPE;
            key_field.data = CTC_PARSER_L3_TYPE_IPV6;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L4_TYPE;
            key_field.data = CTC_PARSER_L4_TYPE_IGMP;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IGMP_TYPE;
            key_field.data = 131;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_IPV6_MLD_V1_DONE: /*SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_DONE*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L3_TYPE;
            key_field.data = CTC_PARSER_L3_TYPE_IPV6;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L4_TYPE;
            key_field.data = CTC_PARSER_L4_TYPE_IGMP;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IGMP_TYPE;
            key_field.data = 132;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

        case CTC_PKT_CPU_REASON_CUSTOM_MLD_V2_REPORT: /*SAI_HOSTIF_TRAP_TYPE_MLD_V2_REPORT*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L3_TYPE;
            key_field.data = CTC_PARSER_L3_TYPE_IPV6;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_L4_TYPE;
            key_field.data = CTC_PARSER_L4_TYPE_IGMP;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IGMP_TYPE;
            key_field.data = 143;
            key_field.mask = 0xFFFF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            break;

            /* Unknown L3 multicast packets */
        case CTC_PKT_CPU_REASON_CUSTOM_UNKNOWN_L3_MULTICAST: /*SAI_HOSTIF_TRAP_TYPE_UNKNOWN_L3_MULTICAST*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IPDA_LKUP;
            key_field.data = 1;
            key_field.mask = 0xF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IPDA_HIT;
            key_field.data = 0;
            key_field.mask = 0xF;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_IP_DA;
            key_field.data = (0xE<<28);
            key_field.mask = (0xF<<28);
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        /* Local IP traps */
        /**
         * @brief IP packets to local router IP address (routes with
         * #SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID = #SAI_SWITCH_ATTR_CPU_PORT)
         * (default packet action is drop)
         */
        case CTC_PKT_CPU_REASON_FWD_CPU: /*SAI_HOSTIF_TRAP_TYPE_IP2ME*/
            /*fwd cpu resaon type cannot use acl key match */
            /*sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_FWD_CPU;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;*/
            break;

        /**
         * @brief SSH traffic (TCP dst port == 22) to local router IP address
         * (default packet action is drop)
         */
        case CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_SSH_INDEX: /*SAI_HOSTIF_TRAP_TYPE_SSH*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_SSH_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        /**
         * @brief SNMP traffic (UDP dst port == 161) to local router IP address
         * (default packet action is drop)
         */
        case CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_SNMP_INDEX: /*SAI_HOSTIF_TRAP_TYPE_SNMP*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_SNMP_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        /**
         * @brief BGP traffic (TCP src port == 179 or TCP dst port == 179) to local
         * router IP address (default packet action is drop)
         */
        case CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_BGP: /*SAI_HOSTIF_TRAP_TYPE_BGP*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_BGP;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        /**
         * @brief BGPv6 traffic (TCP src port == 179 or TCP dst port == 179) to
         * local router IP address (default packet action is drop)
         */
        case CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_BGPV6_INDEX: /*SAI_HOSTIF_TRAP_TYPE_BGPV6*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_PDU + CTC_HOSTIF_L3PDU_ACTION_BGPV6_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        /* Pipeline exceptions */

        /**
         * @brief Packets size exceeds the router interface MTU size
         * (default packet action is drop)
         */
        case CTC_PKT_CPU_REASON_L3_MTU_FAIL: /*SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L3_MTU_FAIL;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        /**
         * @brief Packets with TTL 0 or 1
         * (default packet action is drop)
         */
        case CTC_PKT_CPU_REASON_IP_TTL_CHECK_FAIL: /*SAI_HOSTIF_TRAP_TYPE_TTL_ERROR*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_IP_TTL_CHECK_FAIL;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        /**
         * @brief ISIS pdu
         * (default packet action is drop)
         */
        case CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX: /*SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_ISIS*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_L2_PDU + CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        /**
         * @brief PTP pdu
         * (default packet action is drop)
         */
        case CTC_PKT_CPU_REASON_PTP: /*SAI_HOSTIF_TRAP_TYPE_PTP*/
            sal_memset(&key_field, 0, sizeof(ctc_field_key_t));
            key_field.type = CTC_FIELD_KEY_CPU_REASON_ID;
            key_field.data = CTC_PKT_CPU_REASON_PTP;
            key_field.mask = CTC_SAI_CTC_CPU_REASON_ID_MASK;
            CTC_SAI_ERROR_RETURN(ctcs_acl_add_key_field(lchip, entry_id, &key_field));
            is_drop = true;
            break;

        default:
            /* custom_cpu_reason == CTC_PKT_CPU_REASON_CUSTOM_BASE*/
            /* do not create all zero acl, will match all packet and send to cpu
             * return error, to do ctcs_acl_remove_entry
             */
            return SAI_STATUS_FAILURE;
            break;

    }

    sal_memset(&action_field, 0, sizeof(ctc_acl_field_action_t));
    sal_memset(&acl_cpu, 0, sizeof(ctc_acl_to_cpu_t));
    acl_cpu.mode = CTC_ACL_TO_CPU_MODE_TO_CPU_COVER;
    acl_cpu.cpu_reason_id = custom_reason_id;
    action_field.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
    action_field.ext_data = &acl_cpu;
    CTC_SAI_ERROR_RETURN(ctcs_acl_add_action_field(lchip, entry_id, &action_field));

    if (is_drop)
    {
        sal_memset(&action_field, 0, sizeof(ctc_acl_field_action_t));
        action_field.type = CTC_ACL_FIELD_ACTION_REDIRECT;
        action_field.data0 = CTC_NH_RESERVED_NHID_FOR_DROP;
        CTC_SAI_ERROR_RETURN(ctcs_acl_add_action_field(lchip, entry_id, &action_field));
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_hostif_add_acl_entry(uint8 lchip, ctc_sai_hostif_trap_t* p_trap)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 entry_id = 0;
    ctc_acl_entry_t acl_entry;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID, &entry_id));

    sal_memset(&acl_entry, 0, sizeof(ctc_acl_entry_t));
    acl_entry.mode = 1;
    acl_entry.entry_id = entry_id;
    acl_entry.priority_valid = 1;
    acl_entry.priority = p_trap->priority;
    acl_entry.key_type = CTC_ACL_KEY_COPP;

    CTC_SAI_CTC_ERROR_GOTO(ctcs_acl_add_entry(lchip, p_switch_master->hostif_acl_grp_id, &acl_entry), status, roll_back_0);

    CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_add_acl_field(lchip, entry_id, p_trap->custom_reason_id), status, roll_back_1);

    CTC_SAI_CTC_ERROR_GOTO(ctcs_acl_install_entry(lchip, entry_id), status, roll_back_1);
    p_trap->acl_match_entry_id = entry_id;

    return SAI_STATUS_SUCCESS;

roll_back_1:
    ctcs_acl_remove_entry(lchip, entry_id);

roll_back_0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID, entry_id);
    return status;
}

sai_status_t
_ctc_sai_hostif_remove_acl_entry(uint8 lchip, uint32 entry_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    ctcs_acl_uninstall_entry(lchip, entry_id);

    ctcs_acl_remove_entry(lchip, entry_id);

    /*TBD*/
    //ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY, entry_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, entry_id);

    return status;
}

static sai_status_t
_ctc_sai_hostif_create_trap(uint8 lchip,
        sai_hostif_trap_type_t trap_type,
        bool is_user_defined,
        uint32 entry_priority,
        ctc_sai_hostif_trap_t** pp_hostif_trap)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_trap_t* p_trap = NULL;
    uint32 ctc_reason_id = 0;
    uint32 custom_reason_id = 0;
    uint8 is_ipv6 = 0;
    uint8 chip_type = 0;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_alloc_trap(&p_trap));

    p_trap->trap_type = trap_type;

    CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_trap_type_to_ctc_reason_id(lchip, trap_type, is_user_defined, &ctc_reason_id, &custom_reason_id, &is_ipv6), status, roll_back_0);

    chip_type = ctcs_get_chip_type(lchip);
    if (CTC_CHIP_GOLDENGATE == chip_type)
    {
        if (custom_reason_id >= CTC_PKT_CPU_REASON_CUSTOM_BASE)
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
    }

    p_trap->is_user_defined = is_user_defined;
    p_trap->custom_reason_id = custom_reason_id;
    p_trap->priority = entry_priority;
    if (!CTC_SAI_NOT_NORMAL_EXCEP(custom_reason_id) && (CTC_CHIP_GOLDENGATE != chip_type))
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_add_acl_entry(lchip, p_trap), status, roll_back_0);
    }

    *pp_hostif_trap = p_trap;
    return SAI_STATUS_SUCCESS;

roll_back_0:
    _ctc_sai_hostif_free_trap(p_trap);

    return status;
}

sai_status_t
_ctc_sai_hostif_destroy_trap(uint8 lchip, ctc_sai_hostif_trap_t* p_trap)
{
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    if (!CTC_SAI_NOT_NORMAL_EXCEP(p_trap->custom_reason_id) && (CTC_CHIP_GOLDENGATE != ctcs_get_chip_type(lchip)))
    {
        _ctc_sai_hostif_remove_acl_entry(lchip, p_trap->acl_match_entry_id);
    }

    _ctc_sai_hostif_free_trap(p_trap);

    return status;
}

static sai_status_t
_ctc_sai_hostif_set_trap_action(uint8 lchip, ctc_sai_hostif_trap_t* p_hostif_trap)
{
    ctc_acl_field_action_t action_field;

    if (CTC_SAI_NOT_NORMAL_EXCEP(p_hostif_trap->custom_reason_id) || (CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip)))
    {
        return SAI_STATUS_SUCCESS;
    }

    sal_memset(&action_field, 0, sizeof(ctc_acl_field_action_t));
    action_field.type = CTC_ACL_FIELD_ACTION_REDIRECT;
    action_field.data0 = CTC_NH_RESERVED_NHID_FOR_DROP;
    if ((SAI_PACKET_ACTION_FORWARD == p_hostif_trap->action) || (SAI_PACKET_ACTION_LOG == p_hostif_trap->action))
    {
        CTC_SAI_ERROR_RETURN(ctcs_acl_remove_action_field(lchip, p_hostif_trap->acl_match_entry_id, &action_field));
    }
    else if ((SAI_PACKET_ACTION_DROP == p_hostif_trap->action) || (SAI_PACKET_ACTION_TRAP == p_hostif_trap->action))
    {
        CTC_SAI_ERROR_RETURN(ctcs_acl_add_action_field(lchip, p_hostif_trap->acl_match_entry_id, &action_field));
    }
    else
    {
        return SAI_STATUS_SUCCESS; //SONiC debug modify by cmodel
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_set_port_trap_enable(uint8 lchip, uint32 custom_reason_id, sai_object_list_t* p_objlist, uint32 enable)
{
    uint32 index = 0;
    uint32 gport = 0;
    sai_object_id_t oid = 0;
    ctc_pdu_port_l2pdu_action_t action = 0;

    action = enable?CTC_PDU_L2PDU_ACTION_TYPE_COPY_TO_CPU:CTC_PDU_L2PDU_ACTION_TYPE_FWD;
    for (index = 0; index < p_objlist->count; index++)
    {
        sal_memcpy(&oid, (p_objlist->list+index), sizeof(sai_object_id_t));
        ctc_sai_oid_get_gport(oid, &gport);
        switch (custom_reason_id)
        {
            case SAI_HOSTIF_TRAP_TYPE_STP:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_L2PDU_ACTION_INDEX_BPDU, action));
                break;

            case SAI_HOSTIF_TRAP_TYPE_LACP:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_L2PDU_ACTION_INDEX_SLOW_PROTO, action));
                break;

            case SAI_HOSTIF_TRAP_TYPE_EAPOL:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_L2PDU_ACTION_INDEX_EAPOL, action));
                break;

            case SAI_HOSTIF_TRAP_TYPE_LLDP:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_L2PDU_ACTION_INDEX_LLDP, action));
                break;

            case SAI_HOSTIF_TRAP_TYPE_PVRST:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX, action));
                break;

            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_QUERY:
            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_LEAVE:
            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V1_REPORT:
            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V2_REPORT:
            case SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V3_REPORT:
            case SAI_HOSTIF_TRAP_TYPE_SAMPLEPACKET:
                break;

            case SAI_HOSTIF_TRAP_TYPE_UDLD:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX, action));
                break;

            case SAI_HOSTIF_TRAP_TYPE_CDP:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_HOSTIF_L2PDU_ACTION_CDP_INDEX, action));
                break;

            case SAI_HOSTIF_TRAP_TYPE_VTP:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_HOSTIF_L2PDU_ACTION_VTP_INDEX, action));
                break;

            case SAI_HOSTIF_TRAP_TYPE_DTP:
                return SAI_STATUS_NOT_SUPPORTED;

            case SAI_HOSTIF_TRAP_TYPE_PAGP:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_HOSTIF_L2PDU_ACTION_PAGP_INDEX, action));
                break;

            /* router trap */
            case SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST:
            case SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_L3PDU_ARP_ACTION, enable?CTC_PORT_ARP_ACTION_TYPE_FW_EX:CTC_PORT_ARP_ACTION_TYPE_FW));
                break;

            case SAI_HOSTIF_TRAP_TYPE_DHCP:
            case SAI_HOSTIF_TRAP_TYPE_DHCPV6:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_L3PDU_DHCP_ACTION, enable?CTC_PORT_ARP_ACTION_TYPE_FW_EX:CTC_PORT_ARP_ACTION_TYPE_FW));
                break;

            case SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_ISIS:
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l2pdu_set_port_action(lchip, gport, CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX, action));
                break;

            case SAI_HOSTIF_TRAP_TYPE_OSPF:
            case SAI_HOSTIF_TRAP_TYPE_PIM:
            case SAI_HOSTIF_TRAP_TYPE_VRRP:
            case SAI_HOSTIF_TRAP_TYPE_OSPFV6:
            case SAI_HOSTIF_TRAP_TYPE_VRRPV6:
            case SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY:
            case SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_V2:
            case SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_REPORT:
            case SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_DONE:
            case SAI_HOSTIF_TRAP_TYPE_MLD_V2_REPORT:
            case SAI_HOSTIF_TRAP_TYPE_UNKNOWN_L3_MULTICAST:
            case SAI_HOSTIF_TRAP_TYPE_IP2ME:
            case SAI_HOSTIF_TRAP_TYPE_SSH:
            case SAI_HOSTIF_TRAP_TYPE_SNMP:
            case SAI_HOSTIF_TRAP_TYPE_BGP:
            case SAI_HOSTIF_TRAP_TYPE_BGPV6:
            case SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR:
            case SAI_HOSTIF_TRAP_TYPE_TTL_ERROR:
            case SAI_HOSTIF_TRAP_TYPE_STATIC_FDB_MOVE:
            case SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_EGRESS_BUFFER:
            case SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_WRED:
            case SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_ROUTER:
                /*centec support to config interface to enable/disable this trap*/
                return SAI_STATUS_NOT_SUPPORTED;
                break;

            default:
                break;
        }
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_hostif_create_hostif_trap(
        _Out_ sai_object_id_t *hostif_trap_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val, *attr_type_val, *attr_action_val = NULL;
    uint32 attr_idx = 0;
    uint32 attr_type_idx = 0;
    uint32 attr_action_idx = 0;
    uint32 entry_priority = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_sai_hostif_trap_t* p_hostif_trap = NULL;
    ctc_sai_counter_t* p_sai_counter = NULL;

    CTC_SAI_PTR_VALID_CHECK(hostif_trap_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_NOT_EXECUTED;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        entry_priority = attr_val->u32;
    }
    else
    {
        entry_priority = CTC_ACL_ENTRY_PRIORITY_DEFAULT;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE, &attr_type_val, &attr_type_idx);
    if (!CTC_SAI_ERROR(status))
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_create_trap(lchip, attr_type_val->s32, false, entry_priority, &p_hostif_trap));
        p_hostif_trap->trap_type = attr_type_val->s32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif trap type on create of hostif trap\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION, &attr_action_val, &attr_action_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif trap packet action on create of hostif trap\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    else
    {
        p_hostif_trap->action = attr_action_val->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status) && (0 != attr_val->objlist.count))
    {
        p_hostif_trap->exclude_port_list.list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*(attr_val->objlist.count));
        if (p_hostif_trap->exclude_port_list.list)
        {
            sal_memcpy(p_hostif_trap->exclude_port_list.list, attr_val->objlist.list, sizeof(sai_object_id_t)*(attr_val->objlist.count));
            p_hostif_trap->exclude_port_list.count = attr_val->objlist.count;
            CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_set_port_trap_enable(lchip, p_hostif_trap->trap_type, &(p_hostif_trap->exclude_port_list), false), status, roll_back_0);
        }
        else
        {
            status = SAI_STATUS_NO_MEMORY;
            goto roll_back_0;
        }
    }

    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_hostif_trap->hostif_group_id = attr_val->oid;
    }
    else
    {
        p_hostif_trap->hostif_group_id = p_switch_master->default_trap_grp_id;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_ATTR_MIRROR_SESSION, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "hostif trap mirror session is not supported, when create hostif trap!\n");
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_TRAP_ATTR_COUNTER_ID, &attr_val, &attr_idx);
    if(SAI_STATUS_SUCCESS == status)
    {
        p_sai_counter = ctc_sai_db_get_object_property(lchip, attr_val->oid);
        if (NULL == p_sai_counter)
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        p_hostif_trap->counter_id = attr_val->oid;
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_set_trap_action(lchip, p_hostif_trap), status, roll_back_1);
    CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_add_acl_qos_info(lchip, p_hostif_trap), status, roll_back_1);

    *hostif_trap_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF_TRAP, lchip, 0, 0, p_hostif_trap->custom_reason_id);
    status = ctc_sai_db_add_object_property(lchip, *hostif_trap_id, p_hostif_trap);
    if (CTC_SAI_ERROR(status))
    {
        if (SAI_STATUS_ITEM_ALREADY_EXISTS ==status)
        {
            _ctc_sai_hostif_destroy_trap(lchip, p_hostif_trap);
            p_hostif_trap = ctc_sai_db_get_object_property(lchip, *hostif_trap_id);
            if (NULL == p_hostif_trap)
            {
                CTC_SAI_DB_UNLOCK(lchip);
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
        }
        else
        {
            goto roll_back_2;
        }
    }
    p_hostif_trap->ref_count++;
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_2:
    _ctc_sai_hostif_remove_acl_qos_info(lchip, p_hostif_trap);
roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);
roll_back_0:
    _ctc_sai_hostif_destroy_trap(lchip, p_hostif_trap);
    return status;
}

sai_status_t
ctc_sai_hostif_remove_hostif_trap(
        _In_ sai_object_id_t hostif_trap_id)
{
    ctc_sai_hostif_trap_t* p_hostif_trap = NULL;
    ctc_object_id_t ctc_oid;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF_TRAP, hostif_trap_id, &ctc_oid));
    CTC_SAI_DB_LOCK(lchip);
    lchip = ctc_oid.lchip;
    p_hostif_trap = ctc_sai_db_get_object_property(lchip, hostif_trap_id);
    if (NULL == p_hostif_trap)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_hostif_trap->ref_count--;

    if (0 == p_hostif_trap->ref_count)
    {
        ctc_sai_db_remove_object_property(lchip, hostif_trap_id);
        _ctc_sai_hostif_remove_acl_qos_info(lchip, p_hostif_trap);
        _ctc_sai_hostif_destroy_trap(lchip, p_hostif_trap);
    }
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_hostif_get_trap_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_trap_t* p_hostif_trap = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_hostif_trap = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_hostif_trap)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "object id %"PRIx64" get hostif trap attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE:
            attr->value.s32 = p_hostif_trap->trap_type;
            break;
        case SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION:
            attr->value.s32 = p_hostif_trap->action;
            break;
        case SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY:
            if ((SAI_PACKET_ACTION_TRAP != p_hostif_trap->action) && (SAI_PACKET_ACTION_COPY != p_hostif_trap->action))
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            }
            attr->value.u32 = p_hostif_trap->priority;
            break;
        case SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST:
            if ((SAI_PACKET_ACTION_TRAP != p_hostif_trap->action) && (SAI_PACKET_ACTION_COPY != p_hostif_trap->action))
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(sai_object_id_t), p_hostif_trap->exclude_port_list.list, p_hostif_trap->exclude_port_list.count, &attr->value.objlist));
            break;
        case SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP:
            if ((SAI_PACKET_ACTION_TRAP != p_hostif_trap->action) && (SAI_PACKET_ACTION_COPY != p_hostif_trap->action))
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            }
            attr->value.oid = p_hostif_trap->hostif_group_id;
            break;
        case SAI_HOSTIF_TRAP_ATTR_MIRROR_SESSION:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            break;
        case SAI_HOSTIF_TRAP_ATTR_COUNTER_ID:
            attr->value.oid = p_hostif_trap->counter_id;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif trap attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static sai_status_t
ctc_sai_hostif_set_trap_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 chip_type = 0;
    ctc_sai_hostif_trap_t* p_hostif_trap = NULL;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_sai_counter_t* p_counter_info = NULL;
    ctc_qos_queue_cfg_t qos_queue_cfg;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_hostif_trap = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_hostif_trap)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_NOT_EXECUTED;
    }

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "object id %"PRIx64" set hostif trap attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE:
            status = SAI_STATUS_INVALID_ATTRIBUTE_0;
            break;
        case SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION:
            p_hostif_trap->action = attr->value.s32;
            CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_set_trap_action(lchip, p_hostif_trap));
            break;
        case SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY:
            if ((SAI_PACKET_ACTION_TRAP != p_hostif_trap->action) && (SAI_PACKET_ACTION_COPY != p_hostif_trap->action))
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            p_hostif_trap->priority = attr->value.u32;
            break;
        case SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST:
            if ((SAI_PACKET_ACTION_TRAP != p_hostif_trap->action) && (SAI_PACKET_ACTION_COPY != p_hostif_trap->action))
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            if (p_hostif_trap->exclude_port_list.list)
            {
                _ctc_sai_hostif_set_port_trap_enable(lchip, p_hostif_trap->trap_type, &(p_hostif_trap->exclude_port_list), true);
                mem_free(p_hostif_trap->exclude_port_list.list);
            }
            p_hostif_trap->exclude_port_list.list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*(attr->value.objlist.count));
            if (p_hostif_trap->exclude_port_list.list)
            {
                sal_memcpy(p_hostif_trap->exclude_port_list.list, attr->value.objlist.list, attr->value.objlist.count);
                p_hostif_trap->exclude_port_list.count = attr->value.objlist.count;
                status = _ctc_sai_hostif_set_port_trap_enable(lchip, p_hostif_trap->trap_type, &(p_hostif_trap->exclude_port_list), false);
                if (CTC_SAI_ERROR(status))
                {
                    mem_free(p_hostif_trap->exclude_port_list.list);
                    return status;
                }
            }
            else
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            break;
        case SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP:
            if ((SAI_PACKET_ACTION_TRAP != p_hostif_trap->action) && (SAI_PACKET_ACTION_COPY != p_hostif_trap->action))
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_remove_acl_qos_info(lchip, p_hostif_trap));
            p_hostif_trap->hostif_group_id = attr->value.oid;
            CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_set_trap_action(lchip, p_hostif_trap));
            CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_add_acl_qos_info(lchip, p_hostif_trap));
            break;
        case SAI_HOSTIF_TRAP_ATTR_MIRROR_SESSION:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_HOSTIF_TRAP_ATTR_COUNTER_ID:
            if (SAI_NULL_OBJECT_ID != attr->value.oid)
            {
                p_counter_info = ctc_sai_db_get_object_property(lchip, attr->value.oid);
                if (NULL == p_counter_info)
                {
                    return SAI_STATUS_ITEM_NOT_FOUND;
                }
                if (attr->value.oid == p_hostif_trap->counter_id)
                {
                    break;
                }
                if (SAI_NULL_OBJECT_ID != p_hostif_trap->counter_id)
                {
                    CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_hostif_trap_remove(p_hostif_trap->counter_id, CTC_SAI_COUNTER_TYPE_HOSTIF));
                }
                p_hostif_trap->counter_id = attr->value.oid;
                CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_add_acl_qos_info(lchip, p_hostif_trap));
            }
            else
            {
                if (SAI_NULL_OBJECT_ID != p_hostif_trap->counter_id)
                {
                    chip_type = ctcs_get_chip_type(lchip);
                    if (CTC_CHIP_TSINGMA == chip_type)
                    {
                        sal_memset(&qos_queue_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
                        qos_queue_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_STATS_EN;
                        qos_queue_cfg.value.stats.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
                        qos_queue_cfg.value.stats.queue.cpu_reason = p_hostif_trap->custom_reason_id;
                        qos_queue_cfg.value.stats.queue.queue_id = 0;
                        qos_queue_cfg.value.stats.stats_en = 0;
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &qos_queue_cfg));
                    }
                    CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_hostif_trap_remove(p_hostif_trap->counter_id, CTC_SAI_COUNTER_TYPE_HOSTIF));
                    p_hostif_trap->counter_id = SAI_NULL_OBJECT_ID;
                }
            }
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif trap attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t hostif_trap_attr_fn_entries[] = {
    {SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE, ctc_sai_hostif_get_trap_property, NULL},
    {SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION, ctc_sai_hostif_get_trap_property, ctc_sai_hostif_set_trap_property},
    {SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY, ctc_sai_hostif_get_trap_property, ctc_sai_hostif_set_trap_property},
    {SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST, ctc_sai_hostif_get_trap_property, ctc_sai_hostif_set_trap_property},
    {SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP, ctc_sai_hostif_get_trap_property, ctc_sai_hostif_set_trap_property},
    {SAI_HOSTIF_TRAP_ATTR_MIRROR_SESSION, ctc_sai_hostif_get_trap_property, ctc_sai_hostif_set_trap_property},
    {SAI_HOSTIF_TRAP_ATTR_COUNTER_ID, ctc_sai_hostif_get_trap_property, ctc_sai_hostif_set_trap_property},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

sai_status_t
ctc_sai_hostif_set_hostif_trap_attribute(
        _In_ sai_object_id_t hostif_trap_id,
        _In_ const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = hostif_trap_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_trap_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_trap_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_HOSTIF, hostif_trap_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

sai_status_t
ctc_sai_hostif_get_hostif_trap_attribute(
        _In_ sai_object_id_t hostif_trap_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = hostif_trap_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_trap_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_trap_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_HOSTIF, loop, hostif_trap_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________HOSTIF_USER_DEINED_TRAP_______

sai_status_t
ctc_sai_hostif_create_hostif_user_defined_trap(
        _Out_ sai_object_id_t *hostif_user_defined_trap_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_trap_t* p_user_trap = NULL;
    const sai_attribute_value_t *attr_val, *attr_type_val = NULL;
    uint32 attr_idx    = 0;
    uint32 attr_type_idx    = 0;
    uint32 entry_priority = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_PTR_VALID_CHECK(hostif_user_defined_trap_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_PRIORITY, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        entry_priority = attr_val->u32;
    }
    else
    {
        entry_priority = CTC_ACL_ENTRY_PRIORITY_DEFAULT;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TYPE, &attr_type_val, &attr_type_idx);
    if (!CTC_SAI_ERROR(status))
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_create_trap(lchip, attr_type_val->s32, true, entry_priority, &p_user_trap));
        p_user_trap->trap_type = attr_type_val->s32;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif user define trap type on create of hostif user defined trap\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }

    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_GROUP, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_user_trap->hostif_group_id = attr_val->oid;
    }
    else
    {
        p_switch_master = ctc_sai_get_switch_property(lchip);
        if (NULL == p_switch_master)
        {
            goto roll_back_1;
        }
        p_user_trap->hostif_group_id = p_switch_master->default_trap_grp_id;
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_set_trap_action(lchip, p_user_trap), status, roll_back_1);

    *hostif_user_defined_trap_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP, lchip, 0, attr_type_val->s32, p_user_trap->custom_reason_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *hostif_user_defined_trap_id, p_user_trap), status, roll_back_1);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);
roll_back_0:
    _ctc_sai_hostif_destroy_trap(lchip, p_user_trap);
    return status;
}

sai_status_t
ctc_sai_hostif_remove_hostif_user_defined_trap(
        _In_ sai_object_id_t hostif_user_defined_trap_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_hostif_trap_t* p_user_trap = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP, hostif_user_defined_trap_id, &ctc_oid));
    CTC_SAI_DB_LOCK(lchip);
    lchip = ctc_oid.lchip;
    p_user_trap = ctc_sai_db_get_object_property(lchip, hostif_user_defined_trap_id);
    if (NULL == p_user_trap)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    ctc_sai_db_remove_object_property(lchip, hostif_user_defined_trap_id);
    CTC_SAI_DB_UNLOCK(lchip);
    _ctc_sai_hostif_destroy_trap(lchip, p_user_trap);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_hostif_get_user_defined_trap_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_trap_t* p_user_trap = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_user_trap = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_user_trap)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "object id %"PRIx64" get hostif user defined trap attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TYPE:
            attr->value.s32 = p_user_trap->trap_type;
            break;
        case SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_PRIORITY:
            attr->value.u32 = p_user_trap->priority;
            break;
        case SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_GROUP:
            attr->value.oid = p_user_trap->hostif_group_id;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif trap attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_NOT_IMPLEMENTED;
            break;
    }

    return status;
}

static sai_status_t
ctc_sai_hostif_set_user_defined_trap_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_hostif_trap_t* p_user_trap = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_user_trap = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_user_trap)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "object id %"PRIx64" set hostif user defined trap attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_PRIORITY:
            p_user_trap->priority = attr->value.u32;
            break;
        case SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_GROUP:
            p_user_trap->hostif_group_id = attr->value.oid;
            CTC_SAI_ERROR_RETURN(_ctc_sai_hostif_set_trap_action(lchip, p_user_trap));
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Hostif user defined trap attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_NOT_IMPLEMENTED;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t hostif_user_defined_trap_attr_fn_entries[] = {
    {SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TYPE, ctc_sai_hostif_get_user_defined_trap_property, NULL},
    {SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_PRIORITY, ctc_sai_hostif_get_user_defined_trap_property, ctc_sai_hostif_set_user_defined_trap_property},
    {SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_GROUP, ctc_sai_hostif_get_user_defined_trap_property, ctc_sai_hostif_set_user_defined_trap_property},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

sai_status_t
ctc_sai_hostif_set_hostif_user_defined_trap_attribute(
        _In_ sai_object_id_t hostif_user_defined_trap_id,
        _In_ const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = hostif_user_defined_trap_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_user_defined_trap_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_user_defined_trap_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_HOSTIF, hostif_user_defined_trap_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

sai_status_t
ctc_sai_hostif_get_hostif_user_defined_trap_attribute(
        _In_ sai_object_id_t hostif_user_defined_trap_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = hostif_user_defined_trap_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_user_defined_trap_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = hostif_user_defined_trap_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_HOSTIF, loop, hostif_user_defined_trap_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________HOSTIF_PACKET_______

static sai_status_t
_ctc_sai_hostif_get_table_channel_type(ctc_sai_oid_property_t* bucket_data, ctc_sai_hostif_lookup_channel_t* user_data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_table_t* p_hostif_table = (ctc_sai_hostif_table_t*)bucket_data->data;

    if ((SAI_HOSTIF_TABLE_ENTRY_TYPE_PORT == p_hostif_table->hostif_table_type)
            || (SAI_HOSTIF_TABLE_ENTRY_TYPE_LAG == p_hostif_table->hostif_table_type)
            || (SAI_HOSTIF_TABLE_ENTRY_TYPE_VLAN == p_hostif_table->hostif_table_type))
    {
        if (p_hostif_table->obj_id == user_data->port_id
            && (p_hostif_table->trap_id == user_data->trap_id))
        {
            user_data->channel_type = p_hostif_table->channel_type;
            user_data->is_match = true;
            user_data->hostif_table_type = p_hostif_table->hostif_table_type;
        }
    }
    else if (SAI_HOSTIF_TABLE_ENTRY_TYPE_TRAP_ID == p_hostif_table->hostif_table_type)
    {
        if (p_hostif_table->trap_id == user_data->trap_id
            && (!user_data->is_match || (user_data->is_match && (p_hostif_table->hostif_table_type > SAI_HOSTIF_TABLE_ENTRY_TYPE_TRAP_ID))))
        {
            user_data->channel_type = p_hostif_table->channel_type;
            user_data->is_match = true;
            user_data->hostif_table_type = p_hostif_table->hostif_table_type;
        }
    }
    else if (SAI_HOSTIF_TABLE_ENTRY_TYPE_WILDCARD == p_hostif_table->hostif_table_type)
    {
        if (!user_data->is_match)
        {
            user_data->channel_type = p_hostif_table->channel_type;
            user_data->is_match = true;
            user_data->hostif_table_type = p_hostif_table->hostif_table_type;
        }
    }

    return status;
}


sai_hostif_table_entry_channel_type_t
_ctc_sai_hostif_get_reason_channel(uint8 lchip, uint32 src_gport, uint32 reason_id)
{
    sai_object_id_t host_trap_id;
    sai_object_id_t port_id;
    ctc_sai_hostif_t* p_hostif_trap = NULL;
    ctc_sai_hostif_lookup_channel_t lookup_channel;

    host_trap_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF_TRAP, lchip, 0, 0, reason_id);
    p_hostif_trap = ctc_sai_db_get_object_property(lchip, host_trap_id);
    if (NULL == p_hostif_trap)
    {
        host_trap_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP, lchip, 0, 0, reason_id);
        p_hostif_trap = ctc_sai_db_get_object_property(lchip, host_trap_id);
        if (NULL == p_hostif_trap)
        {
            return SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB;
        }
    }

    if (CTC_IS_LINKAGG_PORT(src_gport))
    {
        port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, CTC_GPORT_LINKAGG_ID(src_gport));
    }
    else
    {
        port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, src_gport);
    }
    sal_memset(&lookup_channel, 0, sizeof(ctc_sai_hostif_lookup_channel_t));
    lookup_channel.trap_id = host_trap_id;
    lookup_channel.port_id = port_id;

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY, (hash_traversal_fn)_ctc_sai_hostif_get_table_channel_type, (void*)&lookup_channel);

    if (lookup_channel.is_match)
    {
       return lookup_channel.channel_type;
    }

    return SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB;
}

static sai_status_t
_ctc_sai_hostif_cmp_hostif(ctc_sai_oid_property_t* bucket_data, ctc_sai_hostif_lookup_t* user_data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_t* p_hostif = (ctc_sai_hostif_t*)bucket_data->data;

    if (SAI_HOSTIF_TYPE_NETDEV != p_hostif->hostif_type)
    {
        return SAI_STATUS_SUCCESS;
    }

    if (user_data->fd == -1)
    {
        if ((SAI_OBJECT_TYPE_VLAN == p_hostif->port_type) && (user_data->vlan_id == p_hostif->port_id))
        {
            user_data->is_match = TRUE;
            user_data->p_hostif = p_hostif;
        }

        if (((SAI_OBJECT_TYPE_PORT == p_hostif->port_type) || (SAI_OBJECT_TYPE_LAG == p_hostif->port_type))
            && (user_data->port_id == p_hostif->port_id) && (FALSE == user_data->is_match))
        {
            user_data->is_match = TRUE;
            user_data->p_hostif = p_hostif;
        }
    }
    else
    {
        if (user_data->fd == p_hostif->fd)
        {
            user_data->is_match = TRUE;
            user_data->p_hostif = p_hostif;
        }
    }

    return status;
}

ctc_sai_hostif_t*
_ctc_sai_hostif_get_hostif(uint8 lchip, uint32 src_gport, uint32 src_vid, int32 fd)
{
    sai_object_id_t vlan_id;
    sai_object_id_t port_id;
    uint16 vlan_ptr = 0;
    ctc_sai_hostif_lookup_t lookup_hostif;

    sal_memset(&lookup_hostif, 0, sizeof(ctc_sai_hostif_lookup_t));
    if (fd == -1)
    {
        ctc_sai_vlan_get_vlan_ptr_from_vlan_id(lchip, src_vid, &vlan_ptr);
        vlan_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, vlan_ptr);

        if (CTC_IS_LINKAGG_PORT(src_gport))
        {
            port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, CTC_GPORT_LINKAGG_ID(src_gport));
        }
        else
        {
            port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, src_gport);
        }

        lookup_hostif.vlan_id = vlan_id;
        lookup_hostif.port_id = port_id;
        lookup_hostif.fd = -1;
    }
    else
    {
        lookup_hostif.fd = fd;
    }
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HOSTIF, (hash_traversal_fn)_ctc_sai_hostif_cmp_hostif, (void*)&lookup_hostif);

    if (lookup_hostif.is_match)
    {
       return lookup_hostif.p_hostif;
    }

    return NULL;
}

static sai_status_t
_ctc_sai_packet_process_vlan(ctc_sai_hostif_t* p_hostif, ctc_pkt_rx_t* p_pkt_rx, uint32 pakcet_offset )
{
    uint8 *pst_vlan = NULL;
    bool vlan_exist = FALSE;
    ctc_object_id_t ctc_oid;

    pst_vlan = p_pkt_rx->pkt_buf->data + pakcet_offset + 12;
    if (pst_vlan[0] != 0x81 || pst_vlan[1] != 0x00)
    {
        vlan_exist = FALSE;
    }
    else
    {
        vlan_exist = TRUE;
    }

    if ((SAI_HOSTIF_VLAN_TAG_STRIP == p_hostif->vlan_tag) && vlan_exist)
    {
        /*remove vlan*/
        sal_memmove(pst_vlan, pst_vlan + 4, p_pkt_rx->pkt_buf->len - pakcet_offset - 12 - 4);
        p_pkt_rx->pkt_buf->len -= 4;
    }
    else if ((SAI_HOSTIF_VLAN_TAG_KEEP == p_hostif->vlan_tag) && (!vlan_exist))
    {
        /*add vlan*/
        sal_memmove(pst_vlan+4, pst_vlan, p_pkt_rx->pkt_buf->len - pakcet_offset - 12);
        *pst_vlan = 0x81;
        *(pst_vlan+1) = 0x00;
        if (SAI_OBJECT_TYPE_VLAN == p_hostif->port_type)
        {
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VLAN, p_hostif->port_id, &ctc_oid);
            *(pst_vlan+2) = (ctc_oid.value>>0x16)|0x0F;;
            *(pst_vlan+3) = ctc_oid.value;
        }
        else
        {
            *(pst_vlan+2) = 0;
            *(pst_vlan+3) = 0;
        }
        p_pkt_rx->pkt_buf->len += 4;
    }
    else if ((SAI_HOSTIF_VLAN_TAG_ORIGINAL == p_hostif->vlan_tag) && (vlan_exist))
    {
        if (SAI_OBJECT_TYPE_VLAN == p_hostif->port_type)
        {
            /*remove vlan*/
            sal_memmove(pst_vlan, pst_vlan + 4, p_pkt_rx->pkt_buf->len - pakcet_offset - 12 - 4);
            p_pkt_rx->pkt_buf->len -= 4;
        }
    }

    return SAI_STATUS_SUCCESS;
}

int32
_ctc_sai_hostif_fdb_get_gport(uint8 lchip, uint8 *mac_address, uint32 vlanid, uint32 *gport)
{
    ctc_l2_fdb_query_t fdb_query;
    ctc_l2_fdb_query_rst_t query_rst;
    int ret = 0;

    if (NULL == gport)
    {
        return SAI_STATUS_FAILURE;
    }

    sal_memset(&fdb_query, 0, sizeof(fdb_query));
    sal_memcpy(fdb_query.mac, mac_address, sizeof(mac_addr_t));
    fdb_query.query_type = CTC_L2_FDB_ENTRY_OP_BY_MAC_VLAN;
    fdb_query.query_flag = CTC_L2_FDB_ENTRY_ALL;
    fdb_query.fid        = vlanid;
    fdb_query.query_hw   = TRUE;

    query_rst.buffer_len = sizeof(ctc_l2_addr_t);
    query_rst.buffer = (ctc_l2_addr_t*)mem_malloc(MEM_APP_MODULE, query_rst.buffer_len);
    sal_memset(query_rst.buffer, 0, query_rst.buffer_len);

    ret = ctcs_l2_get_fdb_entry(lchip, &fdb_query, &query_rst);
    if ((0 == ret) && (fdb_query.count > 0))
    {
        *gport = query_rst.buffer->gport;
        mem_free(query_rst.buffer);
        return SAI_STATUS_SUCCESS;
    }

    return SAI_STATUS_FAILURE;
}


int32
_ctc_sai_hostif_packet_send_to_kernel(int fd, uint8 *buf, uint32 length)
{
    uint8 *head = buf;
    int writenLen = 0;
    int count = 0;

    while(TRUE)
    {
        writenLen = write(fd, head + count, length);
        if (writenLen == -1)
        {
            if (errno == EAGAIN)
            {
                break;
            }
            else if(errno == ECONNRESET)
            {
                break;
            }
            else if (errno == EINTR)
            {
                continue;
            }
            else
            {

            }
        }

        if (writenLen == 0)
        {
            break;
        }

        count += writenLen;
        if (count == length)
        {
            break;
        }
    }

    return SAI_STATUS_SUCCESS;
}

int32
_ctc_sai_hostif_packet_send_to_sdk(uint8 lchip, ctc_sai_hostif_t *p_hostif, uint8 *buffer, int buffer_size)
{
    ctc_pkt_tx_t pkt_tx;
    ctc_pkt_skb_t *p_skb = NULL;
    uint32 gport = 0;
    uint16 vlan_ptr = 0;
    int ret = 0;
    ctc_object_id_t ctc_oid;

    sal_memset(&pkt_tx, 0, sizeof(ctc_pkt_tx_t));
    p_skb = &(pkt_tx.skb);

    ctc_packet_skb_init(p_skb);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF, p_hostif->port_id, &ctc_oid);
    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "send packet %s src_port 0x%x!\n", p_hostif->ifname, p_hostif->port_id);

    /* vlan interface */
    if (SAI_OBJECT_TYPE_VLAN == p_hostif->port_type)
    {
        ctc_packet_skb_put(p_skb, buffer_size);
        sal_memcpy(p_skb->data, buffer, buffer_size);
        pkt_tx.tx_info.flags |= CTC_PKT_FLAG_SRC_SVID_VALID;

        ctc_sai_vlan_get_vlan_ptr_from_vlan_id(lchip, ctc_oid.value, &vlan_ptr);
        /* first get port from static fdb */
        ret = _ctc_sai_hostif_fdb_get_gport(lchip, p_skb->data, vlan_ptr, &gport);
        /* not found static fdb get port from arp fdb */
        if (SAI_STATUS_SUCCESS != ret)
        {
            ret = _ctc_sai_hostif_fdb_get_gport(lchip, p_skb->data, ctc_oid.value, &gport);
        }

        /* flooding in vlan */
        if (SAI_STATUS_SUCCESS != ret)
        {
            pkt_tx.tx_info.flags |= CTC_PKT_FLAG_MCAST;
            pkt_tx.tx_info.flags |= CTC_PKT_FLAG_SRC_SVID_VALID;
            pkt_tx.tx_info.src_svid = ctc_oid.value;
            pkt_tx.tx_info.dest_group_id = ctc_oid.value;
        }
        /* unicat to port */
        else
        {
            pkt_tx.tx_info.flags |= CTC_PKT_FLAG_SRC_SVID_VALID;
            pkt_tx.tx_info.src_svid = ctc_oid.value;
            pkt_tx.tx_info.dest_gport = gport;
            pkt_tx.tx_info.flags |= CTC_PKT_FLAG_NH_OFFSET_BYPASS;
        }
        CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "send packet with vlan 0x%x!\n", ctc_oid.value);
    }
    /* port interface or linkagg interface */
    else
    {
        ctc_packet_skb_put(p_skb, buffer_size);
        sal_memcpy(p_skb->data, buffer, buffer_size);

        pkt_tx.tx_info.dest_gport = ctc_oid.value;
        pkt_tx.tx_info.flags |= CTC_PKT_FLAG_NH_OFFSET_BYPASS;

        CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "send packet with dest_port 0x%x!\n", pkt_tx.tx_info.dest_gport);
    }

    pkt_tx.mode = CTC_PKT_MODE_DMA;
    pkt_tx.lchip = 0;
    pkt_tx.tx_info.ttl = 1;
    pkt_tx.tx_info.oper_type = CTC_PKT_OPER_NORMAL;
    pkt_tx.tx_info.is_critical = TRUE;
    return ctcs_packet_tx(lchip, &pkt_tx);
}

int32
_ctc_sai_hostif_packet_receive_from_sdk(ctc_pkt_rx_t* p_pkt_rx)
{
    sai_attribute_t attr_list[4];
    uint32 count           = 0;
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_object_id_t switch_id = 0;
    ctc_sai_hostif_t* p_hostif = NULL;
    uint8 channel_type = 0;
    uint16 packet_offset = 0;
    uint8 gchip = 0;
	uint32  src_port = 0;

    /* SYSTEM MODIFIED by taocy, SONIC only create phyport hostif, no VLANIF and portchannel. convert src_port to phy port. 20200510*/
    src_port = p_pkt_rx->rx_info.src_port;
    if (CTC_IS_LINKAGG_PORT(src_port))
    {
        src_port = p_pkt_rx->rx_info.lport;
    }

    lchip = p_pkt_rx->lchip;
    ctcs_get_gchip_id(lchip, &gchip);
    channel_type = _ctc_sai_hostif_get_reason_channel(lchip, src_port, p_pkt_rx->rx_info.reason);

    CTC_SAI_DB_LOCK(lchip);
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Failed to get switch global info, invalid lchip %d!\n", lchip);
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    packet_offset = CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CPU_ETH_EN)?58:40;
    CTC_SAI_DB_UNLOCK(lchip);

    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "get packet cpu_resason %d src_port 0x%x!\n", p_pkt_rx->rx_info.reason, src_port);
    if (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB == channel_type)
    {

        attr_list[0].id = SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID;
        attr_list[0].value.oid = _ctc_sai_hostif_ctc_reason_id_to_trap_oid(lchip, p_pkt_rx->rx_info.reason);

        if(CTC_IS_LINKAGG_PORT(src_port))
        {
            attr_list[1].id = SAI_HOSTIF_PACKET_ATTR_INGRESS_LAG;
            attr_list[1].id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, CTC_GPORT_LINKAGG_ID(src_port));
        }
        else
        {
            attr_list[1].id = SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT;
            attr_list[1].value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, src_port);

        }

        attr_list[2].id = SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID;
        if(0 == p_pkt_rx->rx_info.logic_src_port) //.1Q bridge
        {
            attr_list[2].value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_1Q, 0, 1);
        }
        else if(p_pkt_rx->rx_info.fid && (p_pkt_rx->rx_info.fid < CTC_SAI_VPWS_OAM_FID_BASE)) //.1D bridge fid < 8k
        {
            attr_list[2].value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_1D, 0, p_pkt_rx->rx_info.fid);
        }
        else  //cross connect bridge for vpws
        {
            attr_list[2].value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_CROSS_CONNECT, 0, p_pkt_rx->rx_info.fid);
        }
        count = 3;

        /* PTP to CPU */
        if(CTC_PKT_CPU_REASON_PTP == p_pkt_rx->rx_info.reason)
        {
            attr_list[count].id = SAI_HOSTIF_PACKET_ATTR_TIMESTAMP;
            attr_list[count].value.timespec.tv_sec = p_pkt_rx->rx_info.ptp.ts.seconds;
            attr_list[count].value.timespec.tv_nsec = p_pkt_rx->rx_info.ptp.ts.nanoseconds;
            count++;
        }

        /* LMR to CPU */
        if((CTC_PKT_CPU_REASON_OAM + CTC_OAM_EXCP_LM_TO_CPU) == p_pkt_rx->rx_info.reason)
        {
            attr_list[count].id = SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL;
            attr_list[count].value.u64 = p_pkt_rx->rx_info.oam.lm_fcl;
            count++;
        }

        switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);

        if (p_switch_master->packet_event_cb)
        {
            p_switch_master->packet_event_cb(switch_id, p_pkt_rx->pkt_len-packet_offset, p_pkt_rx->pkt_buf->data+packet_offset, count, attr_list);
        }
    }
    else if ((SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_PHYSICAL_PORT == channel_type)
        || (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_LOGICAL_PORT == channel_type)
        || (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_L3 == channel_type))
    {
        /* get vlan interface */
        p_hostif = _ctc_sai_hostif_get_hostif(lchip, src_port, p_pkt_rx->rx_info.src_svid, -1);
        if (NULL == p_hostif)
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Failed to get hostif. lchip:0x%x, src_port:0x%x, src_svid:0x%x!\n", lchip, p_pkt_rx->rx_info.src_port, p_pkt_rx->rx_info.src_svid);
            return SAI_STATUS_FAILURE;
        }
        else
        {
            if ((SAI_OBJECT_TYPE_VLAN == p_hostif->port_type) && (CTC_PKT_CPU_REASON_L3_PDU + CTC_L3PDU_ACTION_INDEX_ARP) == p_pkt_rx->rx_info.reason)
            {
                //ctc_arp_fdb_learning(p_pkt_rx->rx_info.src_svid, portid, p_pkt_rx->pkt_buf->data + 46);
            }
        }

        /* SYSTEM MODIFIED by taocy, SLOW ptotocol, bypass vlan process, packets should send to Kernel without VLAN. 20200510*/
        /* SAI merge 20200824 */
        if ((CTC_PKT_CPU_REASON_L2_PDU + CTC_L2PDU_ACTION_INDEX_SLOW_PROTO) != p_pkt_rx->rx_info.reason)
        {
            _ctc_sai_packet_process_vlan(p_hostif, p_pkt_rx, packet_offset);
        }
        /* send the packet to linux kernel */
        _ctc_sai_hostif_packet_send_to_kernel(p_hostif->fd, p_pkt_rx->pkt_buf->data + packet_offset, p_pkt_rx->pkt_buf->len - packet_offset);
    }

    return SAI_STATUS_SUCCESS;
}

extern int32 sys_usw_chip_check_active(uint8 lchip);

void
_ctc_sai_hostif_packet_receive_from_kernel(void *data)
{
    ctc_sai_hostif_t *p_hostif = NULL;
    struct epoll_event events[2048];
    int sockfd = 0;
    int nfds   = 0;
    uint32 idx    = 0;
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    uint8 pkt_buff[1500];
    uint8 *head = NULL;
    bool bReadOk = false;
    uint32 recvNum = 0;
    uint32 count = 0;

    lchip = (uint8)(uintptr)data;
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return;
    }

    while (TRUE)
    {
        nfds = epoll_wait(p_switch_master->epoll_sock, events, 2048, 1);
        if (-1 == nfds)
        {
            continue;
        }
        //chip active check
        if(sys_usw_chip_check_active(lchip) < 0)
        {
            return;
        }
        for (idx = 0; idx < nfds; ++idx)
        {
            if (events[idx].events & EPOLLIN)
            {
                if ( (sockfd = events[idx].data.fd) < 0)
                {
                    continue;
                }

                head = pkt_buff;
                bReadOk = FALSE;
                recvNum = 0;
                count = 0;

                while (TRUE)
                {
                    recvNum = read(sockfd, head + count, 9600);
                    if(recvNum < 0)
                    {
                        if (errno == EAGAIN)
                        {
                            bReadOk = true;
                            break;
                        }
                        else if (errno == ECONNRESET)
                        {
                            break;
                         }
                        else if (errno == EINTR)
                        {
                            continue;
                        }
                        else
                        {
                            break;
                        }
                   }
                   else if (recvNum == 0)
                   {
                        break;
                   }

                   count += recvNum;
                   if (recvNum >= 9600)
                   {
                       break;
                   }
                   else
                   {
                       bReadOk = true;
                       break;
                   }
                }

                if (bReadOk == true)
                {
                    CTC_SAI_LOG_INFO(SAI_API_HOSTIF, "poll receive one packet!\n");
                    pkt_buff[count] = '\0';
                    p_hostif = _ctc_sai_hostif_get_hostif(lchip, 0, 0, sockfd);
                    if (NULL == p_hostif)
                    {
                        continue;
                    }

                    _ctc_sai_hostif_packet_send_to_sdk(lchip, p_hostif, pkt_buff, count);
                }
            }
        }
    }
}

sai_status_t
ctc_sai_hostif_recv_hostif_packet(
        _In_ sai_object_id_t hostif_id,
        _Inout_ sai_size_t *buffer_size,
        _Out_ void *buffer,
        _Inout_ uint32_t *attr_count,
        _Out_ sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_t* p_hostif = NULL;

    CTC_SAI_PTR_VALID_CHECK(buffer);
    CTC_SAI_PTR_VALID_CHECK(buffer_size);
    CTC_SAI_PTR_VALID_CHECK(attr_count);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_id, &lchip));
    p_hostif = ctc_sai_db_get_object_property(lchip, hostif_id);
    if (NULL == p_hostif)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        return status;
    }

    return SAI_STATUS_NOT_IMPLEMENTED;
}

sai_status_t
ctc_sai_hostif_send_hostif_packet(
        _In_ sai_object_id_t hostif_id,
        _In_ sai_size_t buffer_size,
        _In_ const void *buffer,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8* p_data = NULL;
    const sai_attribute_value_t* attr_val = NULL;
    uint32 attr_idx    = 0;
    ctc_pkt_tx_t pkt_tx;
    ctc_pkt_tx_t* p_pkt_tx = &pkt_tx;
    ctc_pkt_info_t* p_tx_info = &(p_pkt_tx->tx_info);
    ctc_pkt_skb_t* p_skb = &(p_pkt_tx->skb);
    uint32 dest_port = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_hostif_packet_oam_tx_type_t oam_tx_type = 0;
    sai_hostif_tx_type_t hostif_tx_type = 0;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;
    ctc_object_id_t ctc_object_id;
    ctc_ptp_time_t ts;
    sai_object_id_t tx_port_id = 0;
    sai_hostif_packet_ptp_tx_packet_op_type_t ptp_tx_op_type = 0;
    sai_packet_event_ptp_tx_notification_data_t ptp_tx_event_data;
    uint8 msg_type = 0;

    CTC_SAI_PTR_VALID_CHECK(buffer);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_HOSTIF);

    sal_memset(&pkt_tx, 0, sizeof(ctc_pkt_tx_t));
    sal_memset(&ts, 0, sizeof(ctc_ptp_time_t));
    sal_memset(&ptp_tx_event_data, 0, sizeof(ptp_tx_event_data));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(hostif_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    /* must be evaluated field */

    p_tx_info->is_critical = TRUE;
    if (CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CPU_ETH_EN))
    {
        pkt_tx.mode = CTC_PKT_MODE_ETH;
    }
    else
    {
        pkt_tx.mode = CTC_PKT_MODE_DMA;
    }
    CTC_SAI_DB_UNLOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute hostif tx type on send packet\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    hostif_tx_type = attr_val->s32;

    if((SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS == hostif_tx_type) || (SAI_HOSTIF_TX_TYPE_PIPELINE_LOOKUP == hostif_tx_type))
    {
        /* normal packet transmit */
        p_tx_info->oper_type = CTC_PKT_OPER_NORMAL;

        if (SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS == hostif_tx_type)
        {
            p_tx_info->flags |= CTC_PKT_FLAG_NH_OFFSET_BYPASS;
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG, &attr_val, &attr_idx);
            if (CTC_SAI_ERROR(status))
            {
                CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute egress port on send packet pipeline bypass\n");
                return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }
            ctc_sai_oid_get_gport(attr_val->oid, &dest_port);
            if (CTC_IS_CPU_PORT(dest_port))
            {
                p_tx_info->oper_type = CTC_PKT_OPER_C2C;
            }
            p_tx_info->dest_gport = dest_port;
        }
        else if (SAI_HOSTIF_TX_TYPE_PIPELINE_LOOKUP == hostif_tx_type)
        {
            p_tx_info->flags |= CTC_PKT_FLAG_INGRESS_MODE;

            /* set ingress port to send packet loop to and do lookup */
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT, &attr_val, &attr_idx);
            if (CTC_SAI_ERROR(status))
            {
                CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute ingress port on send packet to do pipeline lookup\n");
                return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }
            ctc_sai_oid_get_gport(attr_val->oid, &dest_port);
            p_tx_info->dest_gport = dest_port;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Send Packet invalid TX type %u\n", attr_val->s32);
            return SAI_STATUS_INVALID_ATTR_VALUE_0 + attr_idx;
        }

    }
    else if(SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX == hostif_tx_type)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_CUSTOM_OAM_TX_TYPE, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute oam tx type on send packet\n");
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
        else
        {
            oam_tx_type = attr_val->s32;
        }

        /* oam packet transmit */
        p_tx_info->oper_type = CTC_PKT_OPER_OAM;

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_CUSTOM_OAM_Y1731_SESSION_ID, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute oam tx type on send packet\n");
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }

        p_y1731_session_info = ctc_sai_db_get_object_property(lchip, attr_val->oid);
        if (NULL == p_y1731_session_info)
        {
            CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to get y1731 session, invalid sai_y1731_session_id %d!\n", attr_val->oid);
            return SAI_STATUS_ITEM_NOT_FOUND;
        }

        if(SAI_Y1731_SESSION_DIRECTION_UPMEP == p_y1731_session_info->dir)
        {
            p_tx_info->oam.flags |= CTC_PKT_OAM_FLAG_IS_UP_MEP;

            //Ether or vpls/vpws upmep
            if(p_y1731_session_info->meg_type <= SAI_Y1731_MEG_TYPE_L2VPN_VPWS)
            {
                p_tx_info->dest_gport = p_y1731_session_info->oam_key.u.eth.gport;
                p_tx_info->oam.vid = p_y1731_session_info->oam_key.u.eth.vlan_id;
            }
            else
            {
                /* Y1731 session type is not correct */
                return SAI_STATUS_INVALID_PARAMETER;
            }
        }
        else if((SAI_Y1731_SESSION_DIRECTION_DOWNMEP == p_y1731_session_info->dir))
        {
            //Ether or vpls/vpws upmep
            if(p_y1731_session_info->meg_type <= SAI_Y1731_MEG_TYPE_L2VPN_VPWS)
            {
                p_tx_info->dest_gport = p_y1731_session_info->oam_key.u.eth.gport;
            }
        }

        if(p_y1731_session_info->meg_type <= SAI_Y1731_MEG_TYPE_L2VPN_VPWS)
        {
            p_tx_info->oam.type = CTC_OAM_TYPE_ETH;
        }
        else if(p_y1731_session_info->meg_type == SAI_Y1731_MEG_TYPE_MPLS_TP)
        {
            //packet do not have mpls, L2 header
            p_tx_info->oam.type = CTC_OAM_TYPE_ACH;

            if(p_y1731_session_info->nh_oid)
            {
                p_tx_info->flags |= CTC_PKT_FLAG_NHID_VALID;
                ctc_sai_oid_get_value(p_y1731_session_info->nh_oid, &p_tx_info->nhid);
            }

            if(!p_y1731_session_info->without_gal)
            {
                p_tx_info->flags |= CTC_PKT_OAM_FLAG_HAS_MPLS_GAL;
            }
        }

        if((p_y1731_session_info->meg_type == SAI_Y1731_MEG_TYPE_L2VPN_VPLS)
            || (p_y1731_session_info->meg_type == SAI_Y1731_MEG_TYPE_L2VPN_VPWS))
        {
            p_tx_info->flags |= CTC_PKT_FLAG_OAM_USE_FID;
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, p_y1731_session_info->bridge_id, &ctc_object_id);
            p_tx_info->fid = ctc_object_id.value;
        }

        if(p_y1731_session_info->is_link_oam)
        {
            p_tx_info->oam.flags |= CTC_PKT_OAM_FLAG_LINK_OAM;
        }

        if(SAI_HOSTIF_PACKET_OAM_TX_TYPE_LM == oam_tx_type)
        {
            //may not use
            //p_tx_info->oam.flags |= CTC_PKT_OAM_FLAG_IS_LM;
        }
        else if(SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM == oam_tx_type)
        {
            p_tx_info->oam.flags |= CTC_PKT_OAM_FLAG_IS_DM;

            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_CUSTOM_TIMESTAMP_OFFSET, &attr_val, &attr_idx);
            if (CTC_SAI_ERROR(status))
            {
                CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute oam dm offset on send dm packet\n");
                return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }

            p_tx_info->oam.dm_ts_offset = attr_val->u32;
        }
    }
    else if(SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX == hostif_tx_type)
    {
        /* ptp packet transmit */
        p_tx_info->oper_type = CTC_PKT_OPER_PTP;

        p_tx_info->flags |= CTC_PKT_FLAG_NH_OFFSET_BYPASS;
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute egress port on send packet\n");
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
        ctc_sai_oid_get_gport(attr_val->oid, &dest_port);
        tx_port_id = attr_val->oid;
        p_tx_info->dest_gport = dest_port;

        p_tx_info->flags |= CTC_PKT_FLAG_PTP_TS_PRECISION;

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_CUSTOM_PTP_TX_PACKET_OP_TYPE, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute ptp tx packet op type on send packet\n");
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
        ptp_tx_op_type = attr_val->s32;

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_CUSTOM_TIMESTAMP_OFFSET, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute ptp correctionField offset on send ptp packet\n");
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }

        p_tx_info->ptp.ts_offset = attr_val->u32;
        msg_type = *((uint8*)buffer + p_tx_info->ptp.ts_offset) & 0xF;
        if ((CTC_PTP_MSG_TYPE_DELAY_REQ == msg_type)||(CTC_PTP_MSG_TYPE_PDELAY_REQ == msg_type))
        {
            p_tx_info->ptp.delay_asymmetry_en = 1;
        }

        if(CTC_CHIP_TSINGMA <= ctcs_get_chip_type(lchip))
        {
            if(SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_1 == ptp_tx_op_type)
            {
                p_tx_info->ptp.ts.seconds = 0;
                p_tx_info->ptp.ts.nanoseconds = 0;
                p_tx_info->ptp.oper = CTC_PTP_REPLACE_ONLY;
            }
            else if(SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_2 == ptp_tx_op_type)
            {
                if (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
                {
                    ctcs_ptp_get_clock_timestamp(lchip, &ts);
                    p_tx_info->ptp.ts.seconds = ts.seconds;
                    p_tx_info->ptp.ts.nanoseconds = ts.nanoseconds;
                    p_tx_info->ptp.oper = CTC_PTP_CORRECTION;

                    ptp_tx_event_data.tx_port = tx_port_id;
                    ptp_tx_event_data.msg_type = *((uint8*)buffer + p_tx_info->ptp.ts_offset) & 0xF;
                    ptp_tx_event_data.ptp_seq_id = *((uint8*)buffer + p_tx_info->ptp.ts_offset + 30); // 30 is sequenceId offset in PTP pdu
                    ptp_tx_event_data.tx_timestamp.tv_sec = ts.seconds;
                    ptp_tx_event_data.tx_timestamp.tv_nsec = ts.nanoseconds;

                    p_switch_master->ptp_packet_tx_event_cb(1, &ptp_tx_event_data);
                }
                else if (CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))
                {
                    p_tx_info->ptp.oper = CTC_PTP_CAPTURE_ONLY;
                }
            }
            else if(SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_3 == ptp_tx_op_type)
            {
                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_HOSTIF_PACKET_ATTR_TX_TIMESTAMP, &attr_val, &attr_idx);
                if (CTC_SAI_ERROR(status))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_HOSTIF, "Missing mandatory attribute ptp tx timestamp on send ptp op type 3 packet\n");
                    return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
                }

                p_tx_info->ptp.ts.seconds = attr_val->timespec.tv_sec;
                p_tx_info->ptp.ts.nanoseconds = attr_val->timespec.tv_nsec;
                p_tx_info->ptp.oper = CTC_PTP_CORRECTION;
            }

        }

    }

    ctc_packet_skb_init(p_skb);
    p_data = ctc_packet_skb_put(p_skb, buffer_size);
    sal_memcpy(p_data, buffer, buffer_size);

    CTC_SAI_CTC_ERROR_RETURN(ctcs_packet_tx(lchip, p_pkt_tx));

    return status;
}

#define ________HOSTIF_WB________

static sai_status_t
_ctc_sai_hostif_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_t* p_hostif = (ctc_sai_hostif_t*)data;
    int32 fd = -1;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    /* use ioctl to create tap interface in linux kernel */
    fd = _ctc_sai_hostif_create_net_device(p_hostif->ifname);
    if (fd < 0)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    p_hostif->fd = fd;


    /* add fd to epoll socket list */
    p_switch_master->evl.data.fd = fd;
    epoll_ctl(p_switch_master->epoll_sock, EPOLL_CTL_ADD, fd, &p_switch_master->evl);

    CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_oper_status(p_hostif->ifname, p_hostif->oper_status), status, roll_back_0);

    return SAI_STATUS_SUCCESS;
roll_back_0:
    _ctc_sai_hostif_remove_net_device(fd);

    return status;
}

static sai_status_t
_ctc_sai_hostif_table_entry_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_table_t* p_hostif_table = (ctc_sai_hostif_table_t*)data;

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_hostif_table->hostif_table_id));

    return status;
}

static sai_status_t
_ctc_sai_hostif_trap_group_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_trap_group_t* p_hostif_trap_grp = (ctc_sai_hostif_trap_group_t*)data;

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_hostif_trap_grp->hostif_group_id));

    return status;
}

static sai_status_t
_ctc_sai_hostif_trap_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_hostif_trap_t* p_hostif_trap = (ctc_sai_hostif_trap_t*)data;

    if (p_hostif_trap->acl_match_entry_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID, p_hostif_trap->acl_match_entry_id));
    }

    return status;
}

#define ________HOSTIF_DUMP________

static sai_status_t
_ctc_sai_hostif_dump_hostif_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  hostif_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_hostif_t* p_hostif = NULL;

    hostif_oid = bucket_data->oid;
    p_hostif = (ctc_sai_hostif_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (hostif_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-32s %-11d %-9d 0x%016"PRIx64" %-8d %-11d %-8d\n", num_cnt, hostif_oid, p_hostif->ifname, \
           p_hostif->hostif_type, p_hostif->port_type, p_hostif->port_id, p_hostif->queue_id, p_hostif->oper_status, p_hostif->vlan_tag);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_dump_hostif_table_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  hostif_tab_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_hostif_table_t* p_hostif_tab = NULL;

    hostif_tab_oid = bucket_data->oid;
    p_hostif_tab = (ctc_sai_hostif_table_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (hostif_tab_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-4d %-12d 0x%016"PRIx64" 0x%016"PRIx64" 0x%016"PRIx64"\n", num_cnt, hostif_tab_oid,  p_hostif_tab->hostif_table_type,\
           p_hostif_tab->channel_type, p_hostif_tab->obj_id, p_hostif_tab->trap_id, p_hostif_tab->hostif_id);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_dump_hostif_trap_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  hostif_trap_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_hostif_trap_t* p_hostif_trap = NULL;

    hostif_trap_oid = bucket_data->oid;
    p_hostif_trap = (ctc_sai_hostif_trap_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (hostif_trap_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-4d 0x%016"PRIx64" %-16d %-12d %-8d %-6d %-6d\n", num_cnt, hostif_trap_oid, p_hostif_trap->trap_type,\
           p_hostif_trap->hostif_group_id, p_hostif_trap->custom_reason_id, p_hostif_trap->acl_match_entry_id, p_hostif_trap->priority, p_hostif_trap->action, p_hostif_trap->enable);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_hostif_dump_hostif_trap_group_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  hostif_trap_grp_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_hostif_trap_group_t* p_hostif_trap_grp = NULL;

    hostif_trap_grp_oid = bucket_data->oid;
    p_hostif_trap_grp = (ctc_sai_hostif_trap_group_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (hostif_trap_grp_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-8d 0x%016"PRIx64" %-11d\n", num_cnt, hostif_trap_grp_oid, p_hostif_trap_grp->queue_id,\
           p_hostif_trap_grp->policer_id, p_hostif_trap_grp->admin_sate);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_hostif_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Hostif MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_HOSTIF))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Hostif");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_hostif_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-32s %-11s %-9s %-18s %-8s %-11s %-8s\n", "No.", "Hostif_oid", "Ifname", "Hostif_type", "Port_type", "Port_id", "Queue_id", "Oper_status", "Vlan_tag");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HOSTIF,
                                            (hash_traversal_fn)_ctc_sai_hostif_dump_hostif_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Hostif table entry");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_hostif_table_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-4s %-12s %-18s %-18s %-18s\n", "No.", "Hostif_tab_id", "Type", "Channel_type", "Port_oid", "Trap_id", "Hostif_id");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY,
                                            (hash_traversal_fn)_ctc_sai_hostif_dump_hostif_table_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_HOSTIF_TRAP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Hostif trap");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_hostif_trap_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-4s %-18s %-16s %-12s %-8s %-6s %-6s\n", "No.", "Hostif_trap_id", "Type", "Hostif_grp_id", "Custom_reason_id", "Acl_entry_id", "Priority", "Action", "Enable");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HOSTIF_TRAP,
                                            (hash_traversal_fn)_ctc_sai_hostif_dump_hostif_trap_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Hostif user defined trap");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_hostif_trap_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-4s %-18s %-16s %-12s %-8s %-6s %-6s\n", "No.", "Hostif_trap_id", "Type", "Hostif_grp_id", "Custom_reason_id", "Acl_entry_id", "Priority", "Action", "Enable");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP,
                                            (hash_traversal_fn)_ctc_sai_hostif_dump_hostif_trap_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Hostif trap group");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_hostif_trap_group_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-8s %-18s %-11s\n", "No.", "Hostif_trap_grp", "Queue_id", "Policer_id", "Admin_state");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP,
                                            (hash_traversal_fn)_ctc_sai_hostif_dump_hostif_trap_group_print_cb, (void*)(&sai_cb_data));
    }
}


#define ________HOSTIF_API_______

sai_hostif_api_t g_ctc_sai_hostif_api = {
    ctc_sai_hostif_create_hostif,
    ctc_sai_hostif_remove_hostif,
    ctc_sai_hostif_set_hostif_attribute,
    ctc_sai_hostif_get_hostif_attribute,
    ctc_sai_hostif_create_hostif_table_entry,
    ctc_sai_hostif_remove_hostif_table_entry,
    ctc_sai_hostif_set_hostif_table_entry_attribute,
    ctc_sai_hostif_get_hostif_table_entry_attribute,
    ctc_sai_hostif_create_hostif_trap_group,
    ctc_sai_hostif_remove_hostif_trap_group,
    ctc_sai_hostif_set_hostif_trap_group_attribute,
    ctc_sai_hostif_get_hostif_trap_group_attribute,
    ctc_sai_hostif_create_hostif_trap,
    ctc_sai_hostif_remove_hostif_trap,
    ctc_sai_hostif_set_hostif_trap_attribute,
    ctc_sai_hostif_get_hostif_trap_attribute,
    ctc_sai_hostif_create_hostif_user_defined_trap,
    ctc_sai_hostif_remove_hostif_user_defined_trap,
    ctc_sai_hostif_set_hostif_user_defined_trap_attribute,
    ctc_sai_hostif_get_hostif_user_defined_trap_attribute,
    ctc_sai_hostif_recv_hostif_packet,
    ctc_sai_hostif_send_hostif_packet
};

sai_status_t
ctc_sai_hostif_db_init(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 acl_grp_id = 0;
    uint32 igmp_snooping_mode = 0;
    ctc_acl_group_info_t group_info;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_sai_hostif_trap_group_t* p_trap_group = NULL;
    ctc_acl_property_t acl_prop;
    ctc_global_acl_property_t acl_glb_prop;
    ctc_pdu_global_l3pdu_action_t action;
    mac_addr_t mac_da;
    mac_addr_t mac_da_mask;
    ctc_pdu_l2pdu_key_t pdu_l2pdu;
    ctc_pdu_global_l2pdu_action_t l2pdu_entry;
    ctc_pdu_l3pdu_key_t l3pdu_entry;
    ctc_pdu_l3pdu_type_t l3pdu_type;
    uint8 chip_type = 0;

    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_HOSTIF;
    wb_info.data_len = sizeof(ctc_sai_hostif_t);;
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_hostif_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_HOSTIF, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_HOSTIF;
    wb_info.data_len = sizeof(ctc_sai_hostif_table_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_hostif_table_entry_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_HOSTIF;
    wb_info.data_len = sizeof(ctc_sai_hostif_trap_group_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_hostif_trap_group_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_HOSTIF;
    wb_info.data_len = sizeof(ctc_sai_hostif_trap_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_hostif_trap_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_HOSTIF_TRAP, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
    sal_memset(&group_info, 0, sizeof(ctc_acl_group_info_t));

    chip_type = ctcs_get_chip_type(lchip);
    /*udld macda 01-00-0c-cc-cc-cc*/
    mac_da[0] = 0x01;
    mac_da[1] = 0x00;
    mac_da[2] = 0x0c;
    mac_da[3] = 0xcc;
    mac_da[4] = 0xcc;
    mac_da[5] = 0xcc;
    sal_memset(mac_da_mask, 0xFF, sizeof(mac_da_mask));
    sal_memset(&pdu_l2pdu, 0, sizeof(ctc_pdu_l2pdu_key_t));
    sal_memcpy(pdu_l2pdu.l2pdu_by_mac.mac, mac_da, sizeof(mac_addr_t));
    sal_memcpy(pdu_l2pdu.l2pdu_by_mac.mac_mask, mac_da_mask, sizeof(mac_addr_t));
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_classify_l2pdu(lchip, CTC_PDU_L2PDU_TYPE_MACDA, CTC_HOSTIF_L2PDU_UDLD_INDEX, &pdu_l2pdu));
    sal_memset(&l2pdu_entry, 0, sizeof(ctc_pdu_global_l2pdu_action_t));
    l2pdu_entry.action_index = CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX;
    l2pdu_entry.entry_valid = 1;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_set_global_action(lchip, CTC_PDU_L2PDU_TYPE_MACDA, CTC_HOSTIF_L2PDU_UDLD_INDEX, &l2pdu_entry));

    /*pvrst macda 01-00-0c-cc-cc-cd*/
    mac_da[0] = 0x01;
    mac_da[1] = 0x00;
    mac_da[2] = 0x0c;
    mac_da[3] = 0xcc;
    mac_da[4] = 0xcc;
    mac_da[5] = 0xcd;
    sal_memset(mac_da_mask, 0xFF, sizeof(mac_da_mask));
    sal_memset(&pdu_l2pdu, 0, sizeof(ctc_pdu_l2pdu_key_t));
    sal_memcpy(pdu_l2pdu.l2pdu_by_mac.mac, mac_da, sizeof(mac_addr_t));
    sal_memcpy(pdu_l2pdu.l2pdu_by_mac.mac_mask, mac_da_mask, sizeof(mac_addr_t));
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_classify_l2pdu(lchip, CTC_PDU_L2PDU_TYPE_MACDA, CTC_HOSTIF_L2PDU_PVRST_INDEX, &pdu_l2pdu));
    sal_memset(&l2pdu_entry, 0, sizeof(ctc_pdu_global_l2pdu_action_t));
    l2pdu_entry.action_index = CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX;
    l2pdu_entry.entry_valid = 1;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_set_global_action(lchip, CTC_PDU_L2PDU_TYPE_MACDA, CTC_HOSTIF_L2PDU_PVRST_INDEX, &l2pdu_entry));

    /* CDP */
    sal_memset(&pdu_l2pdu, 0, sizeof(ctc_pdu_l2pdu_key_t));
    pdu_l2pdu.l2hdr_proto = 0X2000;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_classify_l2pdu(lchip, CTC_PDU_L2PDU_TYPE_L2HDR_PROTO, CTC_HOSTIF_L2PDU_CDP_INDEX, &pdu_l2pdu));
    sal_memset(&l2pdu_entry, 0, sizeof(ctc_pdu_global_l2pdu_action_t));
    l2pdu_entry.action_index = CTC_HOSTIF_L2PDU_ACTION_CDP_INDEX;
    l2pdu_entry.entry_valid = 1;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_set_global_action(lchip, CTC_PDU_L2PDU_TYPE_L2HDR_PROTO, CTC_HOSTIF_L2PDU_CDP_INDEX, &l2pdu_entry));

    /* VTP */
    /* VTP packets are sent in either Inter-Switch Link (ISL) frames or in IEEE 802.1Q (dot1q) frames.
    These packets are sent to the destination MAC address 01-00-0C-CC-CC-CC with a logical link control (LLC) code of Subnetwork Access Protocol (SNAP) (AAAA) and a type of 2003 (in the SNAP header).  */
    sal_memset(&pdu_l2pdu, 0, sizeof(ctc_pdu_l2pdu_key_t));
    pdu_l2pdu.l2hdr_proto = 0X2003;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_classify_l2pdu(lchip, CTC_PDU_L2PDU_TYPE_L2HDR_PROTO, CTC_HOSTIF_L2PDU_VTP_INDEX, &pdu_l2pdu));
    sal_memset(&l2pdu_entry, 0, sizeof(ctc_pdu_global_l2pdu_action_t));
    l2pdu_entry.action_index = CTC_HOSTIF_L2PDU_ACTION_VTP_INDEX;
    l2pdu_entry.entry_valid = 1;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_set_global_action(lchip, CTC_PDU_L2PDU_TYPE_L2HDR_PROTO, CTC_HOSTIF_L2PDU_VTP_INDEX, &l2pdu_entry));

    /* PAGP */
    sal_memset(&pdu_l2pdu, 0, sizeof(ctc_pdu_l2pdu_key_t));
    pdu_l2pdu.l2hdr_proto = 0X0104;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_classify_l2pdu(lchip, CTC_PDU_L2PDU_TYPE_L2HDR_PROTO, CTC_HOSTIF_L2PDU_PAGP_INDEX, &pdu_l2pdu));
    sal_memset(&l2pdu_entry, 0, sizeof(ctc_pdu_global_l2pdu_action_t));
    l2pdu_entry.action_index = CTC_HOSTIF_L2PDU_ACTION_PAGP_INDEX;
    l2pdu_entry.entry_valid = 1;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_set_global_action(lchip, CTC_PDU_L2PDU_TYPE_L2HDR_PROTO, CTC_HOSTIF_L2PDU_PAGP_INDEX, &l2pdu_entry));

    /*isis broadcast macda 01-80-c2-00-00-14, mask ff-ff-ff-ff-ff-fe */
    mac_da[0] = 0x01;
    mac_da[1] = 0x80;
    mac_da[2] = 0xc2;
    mac_da[3] = 0x00;
    mac_da[4] = 0x00;
    mac_da[5] = 0x14;
    mac_da_mask[0] = 0xff;
    mac_da_mask[1] = 0xff;
    mac_da_mask[2] = 0xff;
    mac_da_mask[3] = 0xff;
    mac_da_mask[4] = 0xff;
    mac_da_mask[5] = 0xfe;
    sal_memset(&pdu_l2pdu, 0, sizeof(ctc_pdu_l2pdu_key_t));
    sal_memcpy(pdu_l2pdu.l2pdu_by_mac.mac, mac_da, sizeof(mac_addr_t));
    sal_memcpy(pdu_l2pdu.l2pdu_by_mac.mac_mask, mac_da_mask, sizeof(mac_addr_t));
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_classify_l2pdu(lchip, CTC_PDU_L2PDU_TYPE_MACDA, CTC_HOSTIF_L2PDU_ISIS_BROADCAST_INDEX, &pdu_l2pdu));
    sal_memset(&l2pdu_entry, 0, sizeof(ctc_pdu_global_l2pdu_action_t));
    l2pdu_entry.action_index = CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX;
    l2pdu_entry.entry_valid = 1;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_set_global_action(lchip, CTC_PDU_L2PDU_TYPE_MACDA, CTC_HOSTIF_L2PDU_ISIS_BROADCAST_INDEX, &l2pdu_entry));
    
    /*isis p2p macda 09-00-2b-00-00-04, mask ff-ff-ff-ff-ff-fe , isis use same l2pdu cam index */
    mac_da[0] = 0x09;
    mac_da[1] = 0x00;
    mac_da[2] = 0x2b;
    mac_da[3] = 0x00;
    mac_da[4] = 0x00;
    mac_da[5] = 0x04;
    mac_da_mask[0] = 0xff;
    mac_da_mask[1] = 0xff;
    mac_da_mask[2] = 0xff;
    mac_da_mask[3] = 0xff;
    mac_da_mask[4] = 0xff;
    mac_da_mask[5] = 0xfe;
    sal_memset(&pdu_l2pdu, 0, sizeof(ctc_pdu_l2pdu_key_t));
    sal_memcpy(pdu_l2pdu.l2pdu_by_mac.mac, mac_da, sizeof(mac_addr_t));
    sal_memcpy(pdu_l2pdu.l2pdu_by_mac.mac_mask, mac_da_mask, sizeof(mac_addr_t));
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_classify_l2pdu(lchip, CTC_PDU_L2PDU_TYPE_MACDA, CTC_HOSTIF_L2PDU_ISIS_P2P_INDEX, &pdu_l2pdu));
    sal_memset(&l2pdu_entry, 0, sizeof(ctc_pdu_global_l2pdu_action_t));
    l2pdu_entry.action_index = CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX;
    l2pdu_entry.entry_valid = 1;
    CTC_SAI_ERROR_RETURN(ctcs_l2pdu_set_global_action(lchip, CTC_PDU_L2PDU_TYPE_MACDA, CTC_HOSTIF_L2PDU_ISIS_P2P_INDEX, &l2pdu_entry));
    

    /*BGPV6*/
    sal_memset(&action, 0, sizeof(ctc_pdu_global_l3pdu_action_t));
    action.entry_valid = 1;
    action.action_index = CTC_HOSTIF_L3PDU_ACTION_BGPV6_INDEX;
    CTC_SAI_ERROR_RETURN(ctcs_l3pdu_set_global_action(lchip, CTC_PDU_L3PDU_TYPE_IPV6BGP, 0, &action));

    /*OSPFV6*/
    sal_memset(&action, 0, sizeof(ctc_pdu_global_l3pdu_action_t));
    action.entry_valid = 1;
    action.action_index = CTC_HOSTIF_L3PDU_ACTION_OSPFV6_INDEX;
    CTC_SAI_ERROR_RETURN(ctcs_l3pdu_set_global_action(lchip, CTC_PDU_L3PDU_TYPE_IPV6OSPF, 0, &action));

    /*VRRPV6*/
    sal_memset(&action, 0, sizeof(ctc_pdu_global_l3pdu_action_t));
    action.entry_valid = 1;
    action.action_index = CTC_HOSTIF_L3PDU_ACTION_VRRPV6_INDEX;
    CTC_SAI_ERROR_RETURN(ctcs_l3pdu_set_global_action(lchip, CTC_PDU_L3PDU_TYPE_IPV6VRRP, 0, &action));

    /*SNMP*/
    sal_memset(&l3pdu_entry, 0, sizeof(ctc_pdu_l3pdu_key_t));
    sal_memset(&l3pdu_type, 0, sizeof(ctc_pdu_l3pdu_type_t));
    l3pdu_entry.l3pdu_by_port.is_udp = 1;
    l3pdu_entry.l3pdu_by_port.is_tcp = 0;
    l3pdu_entry.l3pdu_by_port.dest_port = 161;
    ctcs_l3pdu_classify_l3pdu(lchip, CTC_PDU_L3PDU_TYPE_LAYER4_PORT, CTC_HOSTIF_L3PDU_CLASSIFY_SNMP_INDEX, &l3pdu_entry);

    sal_memset(&action, 0, sizeof(ctc_pdu_global_l3pdu_action_t));
    action.entry_valid = 1;
    action.action_index = CTC_HOSTIF_L3PDU_ACTION_SNMP_INDEX;
    CTC_SAI_ERROR_RETURN(ctcs_l3pdu_set_global_action(lchip, CTC_PDU_L3PDU_TYPE_LAYER4_PORT, CTC_HOSTIF_L3PDU_CLASSIFY_SNMP_INDEX, &action));

    /*SSH*/
    sal_memset(&l3pdu_entry, 0, sizeof(ctc_pdu_l3pdu_key_t));
    sal_memset(&l3pdu_type, 0, sizeof(ctc_pdu_l3pdu_type_t));
    l3pdu_entry.l3pdu_by_port.is_udp = 0;
    l3pdu_entry.l3pdu_by_port.is_tcp = 1;
    l3pdu_entry.l3pdu_by_port.dest_port = 22;
    CTC_SAI_ERROR_RETURN(ctcs_l3pdu_classify_l3pdu(lchip, CTC_PDU_L3PDU_TYPE_LAYER4_PORT, CTC_HOSTIF_L3PDU_CLASSIFY_SSH_INDEX, &l3pdu_entry));

    sal_memset(&action, 0, sizeof(ctc_pdu_global_l3pdu_action_t));
    action.entry_valid = 1;
    action.action_index = CTC_HOSTIF_L3PDU_ACTION_SSH_INDEX;
    CTC_SAI_ERROR_RETURN(ctcs_l3pdu_set_global_action(lchip, CTC_PDU_L3PDU_TYPE_LAYER4_PORT, CTC_HOSTIF_L3PDU_CLASSIFY_SSH_INDEX, &action));

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_NOT_EXECUTED;
    }
    /*alloc acl group id*/
    if (CTC_WB_STATUS_RELOADING == ctc_sai_warmboot_get_status(lchip))
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, p_switch_master->hostif_acl_grp_id));
    }
    else
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, &acl_grp_id));
    }
    group_info.type = CTC_ACL_GROUP_TYPE_NONE;
    group_info.priority = CTC_SAI_DEFAULT_ACL_HOST_IF_PRIORITY;
    group_info.dir = CTC_INGRESS;
    group_info.lchip = lchip;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_acl_create_group(lchip, acl_grp_id, &group_info), status, roll_back_0);

    p_switch_master->hostif_acl_grp_id = acl_grp_id;

    CTC_SAI_ERROR_GOTO(_ctc_sai_hostif_alloc_trap_group(&p_trap_group), status, roll_back_1);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &p_trap_group->hostif_group_id), status, roll_back_2);
    p_switch_master->default_trap_grp_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP, lchip, 0, 0, p_trap_group->hostif_group_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, p_switch_master->default_trap_grp_id, p_trap_group), status, roll_back_3);
    p_trap_group->queue_id = 0;
    p_trap_group->admin_sate = true;
    p_trap_group->policer_id = SAI_NULL_OBJECT_ID;

    if ((CTC_CHIP_DUET2 == chip_type) || (CTC_CHIP_TSINGMA == chip_type))
    {
        sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
        acl_prop.acl_priority = CTC_SAI_DEFAULT_ACL_HOST_IF_PRIORITY;
        acl_prop.acl_en = 1;
        acl_prop.direction = CTC_INGRESS;
        acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_COPP;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_global_ctl_set(lchip, CTC_GLOBAL_ACL_LKUP_PROPERTY, &acl_prop), status, roll_back_4);

        sal_memset(&acl_glb_prop, 0, sizeof(ctc_global_acl_property_t));
        acl_glb_prop.lkup_level = CTC_SAI_DEFAULT_ACL_HOST_IF_PRIORITY;
        acl_glb_prop.dir = CTC_INGRESS;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_global_ctl_get(lchip, CTC_GLOBAL_ACL_PROPERTY, &acl_glb_prop), status, roll_back_5);
        acl_glb_prop.copp_key_use_ext_mode[3] = 0;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_global_ctl_set(lchip, CTC_GLOBAL_ACL_PROPERTY, &acl_glb_prop), status, roll_back_5);

        igmp_snooping_mode = CTC_GLOBAL_IGMP_SNOOPING_MODE_2;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_global_ctl_set(lchip, CTC_GLOBAL_IGMP_SNOOPING_MODE, &igmp_snooping_mode), status, roll_back_5);
    }

    CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_hostif_packet_epool_init(p_switch_master), status, roll_back_6);

    system("mkdir /dev/net");
    system("modprobe tun");
    system("mknod /dev/net/tun c 10 200");
    system("chmod 777 /dev/net/tun");

    sal_task_create(&p_switch_master->recv_task, "saiRecvThread", SAL_DEF_TASK_STACK_SIZE, 0,
        _ctc_sai_hostif_packet_receive_from_kernel, (void*)(uintptr)lchip);

    return SAI_STATUS_SUCCESS;
roll_back_6:
    if((CTC_CHIP_DUET2 == chip_type) || (CTC_CHIP_TSINGMA == chip_type))
    {
        igmp_snooping_mode = CTC_GLOBAL_IGMP_SNOOPING_MODE_0;
        ctcs_global_ctl_set(lchip, CTC_GLOBAL_IGMP_SNOOPING_MODE, &igmp_snooping_mode);
    }

roll_back_5:
    if((CTC_CHIP_DUET2 == chip_type) || (CTC_CHIP_TSINGMA == chip_type))
    {
        sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
        acl_prop.acl_priority = CTC_SAI_DEFAULT_ACL_HOST_IF_PRIORITY;
        acl_prop.acl_en = 0;
        acl_prop.direction = CTC_INGRESS;
        acl_prop.tcam_lkup_type = 0;
        ctcs_global_ctl_set(lchip, CTC_GLOBAL_ACL_LKUP_PROPERTY, &acl_prop);
    }

roll_back_4:
    ctc_sai_db_remove_object_property(lchip, p_switch_master->default_trap_grp_id);

roll_back_3:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_trap_group->hostif_group_id);

roll_back_2:
    _ctc_sai_hostif_free_trap_group(p_trap_group);

roll_back_1:
    ctcs_acl_destroy_group(lchip, acl_grp_id);
roll_back_0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, acl_grp_id);
    return status;
}

sai_status_t
ctc_sai_hostif_db_deinit(uint8 lchip)
{
    ctc_sai_switch_master_t* p_switch_master = NULL;
    uint8 chip_type = 0;

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HOSTIF_TRAP, (hash_traversal_fn)_ctc_sai_hostif_db_trap_deinit_cb, NULL);

    chip_type = ctcs_get_chip_type(lchip);
    if (CTC_CHIP_GOLDENGATE == chip_type)
    {
        p_switch_master = ctc_sai_get_switch_property(lchip);
        if (NULL == p_switch_master)
        {
            return SAI_STATUS_FAILURE;
        }
        sal_task_destroy(p_switch_master->recv_task);
    }

    return SAI_STATUS_SUCCESS;
}

/*SYSTEM MODIFIED by yoush for warm-reboot in 2020-08-12*/ /* SAI merge 20200824 */
sai_status_t
ctc_sai_hostif_db_run(uint8 lchip)
{
    ctc_sai_switch_master_t* p_switch_master = NULL;

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_NOT_EXECUTED;
    }

    p_switch_master->recv_task = NULL;
    sal_task_create(&p_switch_master->recv_task, "saiRecvThread", SAL_DEF_TASK_STACK_SIZE, 0,
                    _ctc_sai_hostif_packet_receive_from_kernel, (void*)(uintptr)lchip);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_hostif_api_init(void)
{
    ctc_sai_register_module_api(SAI_API_HOSTIF, (void*)&g_ctc_sai_hostif_api);

    return SAI_STATUS_SUCCESS;
}

