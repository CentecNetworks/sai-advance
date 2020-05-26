#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"

#include "ctcs_api.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_isolation_group.h"
#include "ctc_sai_tunnel.h"
#include "ctc_sai_mpls.h"
#include "ctc_sai_lag.h"
#include "ctc_sai_port.h"


void _ctc_sai_bridge_port_lag_member_change_cb_fn(uint8 lchip, uint32 linkagg_id, uint32 mem_port, bool change)
{

    CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "this lag have beend binded for bridge port\n");
    CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "lag member changed lead to execute this function \n"); 
    
    uint32 bit_cnt = 0;
    uint8 gchip = 0;
    ctc_sai_lag_info_t *p_db_lag = NULL;
    ctc_sai_bridge_port_t *p_db_bridge_port = NULL;  
    sai_object_id_t sai_lag_oid;
    sai_object_id_t sai_bridge_port_oid;
    sai_bridge_port_type_t bport_type = 0;
    ctc_port_scl_property_t port_scl_property;
    ctc_port_restriction_t port_restriction;
    ctc_object_id_t ctc_object_id = {0};
    ctc_security_learn_limit_t learn_limit;
    sal_memset(&learn_limit, 0, sizeof(ctc_security_learn_limit_t));

    
    ctcs_get_gchip_id(lchip, &gchip);
    sai_lag_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, linkagg_id);
    p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_oid);
    if(p_db_lag == NULL)
    {
        return;
    }

    bport_type = p_db_lag->bind_bridge_port_type - 1 ;    
    sai_bridge_port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, bport_type, 0, linkagg_id);
    p_db_bridge_port = ctc_sai_db_get_object_property(lchip, sai_bridge_port_oid);

    if(p_db_bridge_port == NULL)
    {
        return;
    }    
    
    if(bport_type == SAI_BRIDGE_PORT_TYPE_PORT)
    {

        // stp port restore
  
        if(p_db_bridge_port->stp_port_bind_count)
        {        
            for (bit_cnt = 0; bit_cnt < sizeof(p_db_bridge_port->stp_port_bind_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_db_bridge_port->stp_port_bind_bits, bit_cnt))
                {
                    if(change)
                    {
                        ctcs_stp_set_state(lchip, mem_port, bit_cnt, p_db_bridge_port->stp_port_state[bit_cnt]);
                    }
                    else
                    {
                        ctcs_stp_set_state(lchip, mem_port, bit_cnt, CTC_STP_FORWARDING);
                    }

                }
            }
        }    

        // vlan member restore

        if(p_db_bridge_port->vlan_member_bind_count)
        {        

            for (bit_cnt = 0; bit_cnt < sizeof(p_db_bridge_port->vlan_member_bind_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_db_bridge_port->vlan_member_bind_bits, bit_cnt))
                {
                    if(change)
                    {
                        ctcs_vlan_add_port(lchip, bit_cnt, mem_port);
                        ctcs_vlan_set_tagged_port( lchip, bit_cnt, mem_port, p_db_bridge_port->vlan_member_tag_mode[bit_cnt]);
                    }
                    else
                    {
                        ctcs_vlan_remove_port(lchip, bit_cnt, mem_port);
                        ctcs_vlan_set_tagged_port( lchip, bit_cnt, mem_port, SAI_VLAN_TAGGING_MODE_TAGGED);
                    }
                }
            }
        }

        // bridge port self restore

        if(change)
        {
            ctcs_port_set_vlan_filter_en(lchip, mem_port, CTC_INGRESS, p_db_bridge_port->ingress_filter);        
            ctcs_port_set_vlan_filter_en(lchip, mem_port, CTC_EGRESS, p_db_bridge_port->egress_filter);

            port_restriction.mode = CTC_PORT_RESTRICTION_PORT_ISOLATION;
            port_restriction.type = CTC_PORT_ISOLATION_ALL;
            port_restriction.dir = CTC_INGRESS;           
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, p_db_bridge_port->isolation_group_oid, &ctc_object_id);
            port_restriction.isolated_id = ctc_object_id.value;
            ctcs_port_set_restriction(lchip, mem_port, &port_restriction);
            
            ctcs_port_set_transmit_en(lchip, mem_port, p_db_bridge_port->admin_state);
            ctcs_port_set_receive_en(lchip, mem_port, p_db_bridge_port->admin_state);

            learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_PORT;
            learn_limit.limit_num = p_db_bridge_port->limit_num;
            learn_limit.limit_action = p_db_bridge_port->limit_action;
            learn_limit.gport = mem_port;
            ctcs_mac_security_set_learn_limit(lchip, &learn_limit);
                                 
        }
        else
        {

            ctcs_port_set_vlan_filter_en(lchip, mem_port, CTC_INGRESS, false);        
            ctcs_port_set_vlan_filter_en(lchip, mem_port, CTC_EGRESS, false);
            
            port_restriction.mode = CTC_PORT_RESTRICTION_PORT_ISOLATION;
            port_restriction.type = CTC_PORT_ISOLATION_ALL;
            port_restriction.dir = CTC_INGRESS;           
            port_restriction.isolated_id = 0;
            ctcs_port_set_restriction(lchip, mem_port, &port_restriction);

            ctcs_port_set_transmit_en(lchip, mem_port, true);
            ctcs_port_set_receive_en(lchip, mem_port, true); 

            learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_PORT;
            learn_limit.limit_num = 0xFFFFFFFF;
            learn_limit.limit_action = CTC_MACLIMIT_ACTION_FWD;
            learn_limit.gport = mem_port;
            ctcs_mac_security_set_learn_limit(lchip, &learn_limit);
            
        }
                                
   }
    
    if(bport_type == SAI_BRIDGE_PORT_TYPE_SUB_PORT)
    {

        sal_memset(&port_scl_property, 0, sizeof(port_scl_property));
        port_scl_property.scl_id = 0;
        port_scl_property.direction = CTC_INGRESS;
        port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_PORT_SVLAN;
        port_scl_property.action_type = CTC_PORT_SCL_ACTION_TYPE_SCL;

        if(change)
        {    
            ctcs_port_set_scl_property(lchip, mem_port, &port_scl_property);
            ctcs_port_set_property(lchip, mem_port, CTC_PORT_PROP_REFLECTIVE_BRIDGE_EN, 1);  
        }
        else
        {
            port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_DISABLE;
            ctcs_port_set_scl_property(lchip, mem_port, &port_scl_property);
            ctcs_port_set_property(lchip, mem_port, CTC_PORT_PROP_REFLECTIVE_BRIDGE_EN, 0); 
        }
    }    
    
}

typedef struct  ctc_sai_bridge_traverse_param_s
{
   uint8 lchip;
   uint8 sucess;
   void* cmp_value1;
   void* cmp_value2;
   void* out_value1;
   void* out_value2;
}ctc_sai_bridge_traverse_param_t;

#define ________BridgePort_______

static int32
_ctc_sai_bridge_port_traverse_get_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_bridge_traverse_param_t* user_data)
{
    uint16 bridge_id = *((uint16*)(user_data->cmp_value1));
    uint16 logic_port = *((uint16*)(user_data->cmp_value2));
    ctc_sai_bridge_port_t* p_bridge_port = bucket_data->data;


    if ((p_bridge_port->bridge_id == bridge_id) && (p_bridge_port->logic_port == logic_port))
    {
        *(uint32*)user_data->out_value1 = p_bridge_port->gport;
        *(uint16*)user_data->out_value2 = p_bridge_port->vlan_id;
        user_data->sucess = 1;
        return (-1);
    }

    return SAI_STATUS_SUCCESS;
}
#if 0

static int32
_ctc_sai_bridge_tunnel_port_traverse_get_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_bridge_traverse_param_t* user_data)
{

    uint16 bridge_id = *((uint16*)(user_data->cmp_value1));
    sai_object_id_t tunnel_id = *((sai_object_id_t*)(user_data->cmp_value2));
    
    ctc_sai_bridge_port_t* p_bridge_port = bucket_data->data;

    if ((p_bridge_port->bridge_id == bridge_id) && (p_bridge_port->tunnel_id == tunnel_id))
    {
        *(uint32*)user_data->out_value1 = p_bridge_port->logic_port;
        user_data->sucess = 1;
        return (-1);
    }

    return SAI_STATUS_SUCCESS;
}
#endif

static int32
_ctc_sai_bridge_sub_port_traverse_get_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_bridge_traverse_param_t* user_data)
{

    uint32 gport = *((uint32*)(user_data->cmp_value1));
    uint16 vlan_id = *((uint16*)(user_data->cmp_value2));
    
    ctc_sai_bridge_port_t* p_bridge_port = bucket_data->data;

    if ((p_bridge_port->gport == gport) && (p_bridge_port->vlan_id == vlan_id))
    {
        *(uint32*)user_data->out_value1 = p_bridge_port->logic_port;
        user_data->sucess = 1;
        return (-1);
    }

    return SAI_STATUS_SUCCESS;
}


#if 0

static sai_status_t
ctc_sai_bridge_traverse_get_tunnel_bridge_port_info(uint8 lchip, uint16 bridge_id, sai_object_id_t tunnel_id, uint32* logic_port)
{
    ctc_sai_bridge_traverse_param_t traverse_param;

    CTC_SAI_PTR_VALID_CHECK(logic_port);

    sal_memset(&traverse_param, 0, sizeof(traverse_param));
    
    traverse_param.lchip = lchip;
    traverse_param.sucess = 0;
    traverse_param.cmp_value1 = (void*)(&bridge_id);
    traverse_param.cmp_value2 = (void*)(&tunnel_id);
    traverse_param.out_value1 = (void*)logic_port;
    
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BRIDGE_PORT, (hash_traversal_fn)_ctc_sai_bridge_tunnel_port_traverse_get_cb, (void*)(&traverse_param));
    
    if (0 == traverse_param.sucess)
    {
        return SAI_STATUS_FAILURE;
    }
    return SAI_STATUS_SUCCESS;
}
#endif

sai_status_t
ctc_sai_bridge_traverse_get_sub_port_info(uint8 lchip, uint32 gport, uint16 vlan_id, uint32* logic_port)
{
    ctc_sai_bridge_traverse_param_t traverse_param;

    CTC_SAI_PTR_VALID_CHECK(logic_port);

    sal_memset(&traverse_param, 0, sizeof(traverse_param));
    
    traverse_param.lchip = lchip;
    traverse_param.sucess = 0;
    traverse_param.cmp_value1 = (void*)(&gport);
    traverse_param.cmp_value2 = (void*)(&vlan_id);
    traverse_param.out_value1 = (void*)logic_port;
    
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BRIDGE_PORT, (hash_traversal_fn)_ctc_sai_bridge_sub_port_traverse_get_cb, (void*)(&traverse_param));
    
    if (0 == traverse_param.sucess)
    {
        return SAI_STATUS_FAILURE;
    }
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_bridge_port_check_global_port(uint32 gport)
{
    if ((CTC_IS_LINKAGG_PORT(gport) && ((gport & CTC_LOCAL_PORT_MASK) > CTC_MAX_LINKAGG_ID))  \
       || (!CTC_IS_LINKAGG_PORT(gport) && (!CTC_IS_CPU_PORT(gport))&& ((CTC_MAP_GPORT_TO_GCHIP(gport) > CTC_MAX_GCHIP_CHIP_ID)   \
       || (CTC_MAP_GPORT_TO_LPORT(gport) >= MAX_PORT_NUM_PER_CHIP))))                        
    {                                                                                         
        return SAI_STATUS_INVALID_PARAMETER;                                                     
    }

return SAI_STATUS_SUCCESS;

}

static sai_status_t
_ctc_sai_bridge_port_check_port_type_attr(sai_bridge_port_type_t port_type, sai_attr_id_t attr_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;

    switch(attr_id)
    {
        case SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
            if (SAI_BRIDGE_PORT_TYPE_PORT == port_type)
            {
                status = SAI_STATUS_INVALID_PARAMETER;
            }
            break;

        case SAI_BRIDGE_PORT_ATTR_PORT_ID:
            if ((SAI_BRIDGE_PORT_TYPE_PORT != port_type)
                && (SAI_BRIDGE_PORT_TYPE_SUB_PORT != port_type))
            {
                status = SAI_STATUS_INVALID_PARAMETER;
            }
            break;
        case SAI_BRIDGE_PORT_ATTR_VLAN_ID:
        case SAI_BRIDGE_PORT_ATTR_TAGGING_MODE:
            if (SAI_BRIDGE_PORT_TYPE_SUB_PORT != port_type)
            {
                status = SAI_STATUS_INVALID_PARAMETER;
            }
            break;
        case SAI_BRIDGE_PORT_ATTR_RIF_ID:
            if (SAI_BRIDGE_PORT_TYPE_1D_ROUTER != port_type)
            {
                status = SAI_STATUS_INVALID_PARAMETER;
            }
            break;
        case SAI_BRIDGE_PORT_ATTR_TUNNEL_ID:
            if (SAI_BRIDGE_PORT_TYPE_TUNNEL != port_type)
            {
                status = SAI_STATUS_INVALID_PARAMETER;
            }
            break;
        case SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES:
        case SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION:
        case SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING:
        case SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING:
        case SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP:
            if (SAI_BRIDGE_PORT_TYPE_PORT != port_type)
            {
                status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            }
            break;
        default:
            break;
    }

    return status;
}

static sai_status_t
_ctc_sai_bridge_packet_action_mapping_to_limit_action(uint32* p_action, const  sai_attribute_value_t *attr_value)
{
    switch(attr_value->s32)
    {
    case SAI_PACKET_ACTION_FORWARD:
        *p_action = CTC_MACLIMIT_ACTION_FWD;
        break;
    case SAI_PACKET_ACTION_DROP:
        *p_action = CTC_MACLIMIT_ACTION_DISCARD;
        break;
    case SAI_PACKET_ACTION_COPY:
        *p_action = CTC_MACLIMIT_ACTION_TOCPU;
        break;
    case SAI_PACKET_ACTION_COPY_CANCEL:
    case SAI_PACKET_ACTION_TRAP :
    case SAI_PACKET_ACTION_LOG:
    case SAI_PACKET_ACTION_DENY:
    case SAI_PACKET_ACTION_TRANSIT:
        return SAI_STATUS_NOT_SUPPORTED;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "invalid action\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    return SAI_STATUS_SUCCESS;

}

static sai_status_t
_ctc_limit_action_mapping_to_sai_bridge_packet_action(sai_attribute_t *attr, uint32 ctc_action )
{
    switch(ctc_action)
    {
    case CTC_MACLIMIT_ACTION_FWD:
        attr->value.s32 = SAI_PACKET_ACTION_FORWARD;
        break;
    case CTC_MACLIMIT_ACTION_DISCARD:
        attr->value.s32 = SAI_PACKET_ACTION_DROP;
        break;
    case CTC_MACLIMIT_ACTION_TOCPU:
        attr->value.s32 = SAI_PACKET_ACTION_COPY;
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "invalid action\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    return SAI_STATUS_SUCCESS;

}


void ctc_sai_bridge_port_lag_member_change_cb_fn(uint8 lchip, uint32 linkagg_id, uint32 mem_port, bool change)
{
    uint32 value = 0;

    value = change?TRUE:FALSE;

    ctcs_port_set_property(lchip, mem_port, CTC_PORT_PROP_ADD_DEFAULT_VLAN_DIS, value);
}

static sai_status_t
_ctc_sai_bridge_port_set_admin_state(uint8 lchip, ctc_sai_bridge_port_t* p_bridge_port, bool admin_state)
{
    ctc_l2dflt_addr_t  l2dflt_addr;
    ctc_vlan_mapping_t vlan_mapping;
    ctc_sai_bridge_port_t* p_bport = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_mpls_ilm_t ctc_mpls_ilm;
    ctc_mpls_ilm_t ctc_mpls_ilm_old;
    sai_object_id_t     sai_lag_id;
    ctc_sai_lag_info_t *p_db_lag = NULL;
    uint8 gchip = 0;
    uint32 bit_cnt = 0;
    uint32 invalid_nh_id[64] = {0};


    ctcs_get_gchip_id(lchip, &gchip);
    sal_memset(&ctc_mpls_ilm, 0, sizeof(ctc_mpls_ilm_t));
    sal_memset(&ctc_mpls_ilm_old, 0, sizeof(ctc_mpls_ilm_t));
    if (admin_state == p_bridge_port->admin_state)
    {
        return SAI_STATUS_SUCCESS;
    }

    if (p_bridge_port->port_type == SAI_BRIDGE_PORT_TYPE_PORT)
    {
        if (CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
        {
            sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_bridge_port->gport);
            p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
            if (NULL == p_db_lag)
            {
                return SAI_STATUS_INVALID_OBJECT_ID;
            }
            for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                {
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_transmit_en(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), admin_state));
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_receive_en(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), admin_state));
                }
            }    
        }
        else
        {    
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_transmit_en(lchip, p_bridge_port->gport, admin_state));
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_receive_en(lchip, p_bridge_port->gport, admin_state));
        }
    }
    else if (p_bridge_port->port_type == SAI_BRIDGE_PORT_TYPE_SUB_PORT)
    {
        sal_memset(&vlan_mapping, 0, sizeof(ctc_vlan_mapping_t));
        vlan_mapping.key = CTC_VLAN_MAPPING_KEY_SVID;
        vlan_mapping.old_svid = p_bridge_port->vlan_id;
        
        sal_memset(&l2dflt_addr, 0, sizeof(ctc_l2dflt_addr_t));
        l2dflt_addr.fid = p_bridge_port->bridge_id;
        l2dflt_addr.with_nh = TRUE;
        l2dflt_addr.member.nh_id = p_bridge_port->nh_id;
        l2dflt_addr.member.mem_port = p_bridge_port->logic_port;
        if (admin_state)
        {
            if(SAI_BRIDGE_TYPE_CROSS_CONNECT != p_bridge_port->bridge_type)
            {
                CTC_SET_FLAG(vlan_mapping.action, CTC_VLAN_MAPPING_OUTPUT_FID);
                CTC_SET_FLAG(vlan_mapping.action, CTC_VLAN_MAPPING_OUTPUT_VLANPTR);
                vlan_mapping.action |= CTC_VLAN_MAPPING_FLAG_VPLS;
                
                vlan_mapping.u3.fid = p_bridge_port->bridge_id;
                vlan_mapping.user_vlanptr = p_bridge_port->bridge_id;  /*for SAI_BRIDGE_PORT_TYPE_1D_ROUTER, implemented by vlanif*/
                CTC_SET_FLAG(vlan_mapping.action, CTC_VLAN_MAPPING_OUTPUT_LOGIC_SRC_PORT);
            
                vlan_mapping.logic_src_port = p_bridge_port->logic_port;
                vlan_mapping.logic_port_type = 0;                
            }
            else
            {
                vlan_mapping.action |= CTC_VLAN_MAPPING_OUTPUT_NHID;
                vlan_mapping.action |= CTC_VLAN_MAPPING_FLAG_VPWS;
                if(0 == p_bridge_port->cross_connect_port)
                {
                    vlan_mapping.u3.nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
                }
                else
                {
                    p_bport = ctc_sai_db_get_object_property(lchip, p_bridge_port->cross_connect_port);
                    vlan_mapping.u3.nh_id = p_bport->nh_id;
                }
            }

            if(p_bridge_port->sub_port_or_tunnel_oam_en)
            {
                CTC_SET_FLAG(vlan_mapping.action, CTC_VLAN_MAPPING_FLAG_L2VPN_OAM);
                vlan_mapping.l2vpn_oam_id = p_bridge_port->bridge_id;  //vpls/vpws oam fid
            }
            
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_update_vlan_mapping(lchip, p_bridge_port->gport, &vlan_mapping));
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_set_nhid_by_logic_port(lchip, p_bridge_port->logic_port, p_bridge_port->nh_id), status, roll_back_0);
            if(SAI_BRIDGE_TYPE_CROSS_CONNECT != p_bridge_port->bridge_type)
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_add_port_to_default_entry(lchip, &l2dflt_addr), status, roll_back_1);
            }
        }
        else
        {          
            vlan_mapping.action |= CTC_VLAN_MAPPING_OUTPUT_NHID;
            vlan_mapping.u3.nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_update_vlan_mapping(lchip, p_bridge_port->gport, &vlan_mapping));
            if(SAI_BRIDGE_TYPE_CROSS_CONNECT != p_bridge_port->bridge_type)
            {
                ctcs_l2_remove_port_from_default_entry(lchip, &l2dflt_addr);
            }
            ctcs_l2_set_nhid_by_logic_port(lchip, p_bridge_port->logic_port, CTC_NH_RESERVED_NHID_FOR_DROP);
        }
    }
    else if (p_bridge_port->port_type == SAI_BRIDGE_PORT_TYPE_1D_ROUTER)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_update_bridge_rif(lchip, p_bridge_port->l3if_id, p_bridge_port->bridge_id, admin_state));
    }
    else if (p_bridge_port->port_type == SAI_BRIDGE_PORT_TYPE_TUNNEL)
    {
        sal_memset(&l2dflt_addr, 0, sizeof(ctc_l2dflt_addr_t));
        l2dflt_addr.fid = p_bridge_port->bridge_id;
        l2dflt_addr.with_nh = TRUE;
        l2dflt_addr.member.nh_id = p_bridge_port->nh_id;
        l2dflt_addr.member.mem_port = p_bridge_port->logic_port;
        
        p_tunnel = ctc_sai_db_get_object_property(lchip, p_bridge_port->tunnel_id);
        if(SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type)
        {
            ctc_mpls_ilm.label = p_tunnel->inseg_label;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_get_ilm(lchip, invalid_nh_id, &ctc_mpls_ilm));
            sal_memcpy(&ctc_mpls_ilm_old, &ctc_mpls_ilm, sizeof(ctc_mpls_ilm_t));
            if(0 == p_bridge_port->cross_connect_port && SAI_BRIDGE_TYPE_CROSS_CONNECT != p_bridge_port->bridge_type)
            {
                if (admin_state)
                {
                    ctc_mpls_ilm.fid = p_bridge_port->bridge_id;
                    ctc_mpls_ilm.type = CTC_MPLS_LABEL_TYPE_VPLS;
                    ctc_mpls_ilm.logic_port_type = TRUE;
                    ctc_mpls_ilm.pwid = p_tunnel->logic_port;
                    ctc_mpls_ilm.nh_id = 0;
                }
            }
            else
            {
                ctc_mpls_ilm.type = CTC_MPLS_LABEL_TYPE_VPWS;
                if(0 != p_bridge_port->cross_connect_port)
                {
                    p_bport = ctc_sai_db_get_object_property(lchip, p_bridge_port->cross_connect_port);
                    if (admin_state)
                    {              
                        ctc_mpls_ilm.nh_id = p_bport->nh_id;
                        
                    }
                }
                else
                {
                    ctc_mpls_ilm.nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
                }
            }
            
            
            ctc_mpls_ilm.pop = 1;
            ctc_mpls_ilm.cwen = p_tunnel->decap_cw_en;
            ctc_mpls_ilm.pw_mode = p_tunnel->decap_pw_mode;
            if (!admin_state)
            {
                ctc_mpls_ilm.nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
                if(p_bridge_port->sub_port_or_tunnel_oam_en)
                {
                    CTC_UNSET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_L2VPN_OAM);
                    ctc_mpls_ilm.l2vpn_oam_id = 0;
                }  
            }
            else
            {
                if(p_bridge_port->sub_port_or_tunnel_oam_en)
                {
                    CTC_SET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_L2VPN_OAM);
                    ctc_mpls_ilm.l2vpn_oam_id = p_bridge_port->bridge_id;  //vpls/vpws oam fid
                }  
            }
            if(p_tunnel->decap_esi_label_valid)
            {
                CTC_SET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_ESLB_EXIST);
            }
            else
            {
                CTC_UNSET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_ESLB_EXIST);
            }
            CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_update_ilm(lchip, &ctc_mpls_ilm));
        }
    
        if (admin_state)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_set_nhid_by_logic_port(lchip, p_bridge_port->logic_port, p_bridge_port->nh_id), status, roll_back_0);
            if(SAI_BRIDGE_TYPE_CROSS_CONNECT != p_bridge_port->bridge_type)
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_add_port_to_default_entry(lchip, &l2dflt_addr), status, roll_back_1);
            }
        }
        else
        {
            ctcs_l2_set_nhid_by_logic_port(lchip, p_bridge_port->logic_port, CTC_NH_RESERVED_NHID_FOR_DROP);
            if(SAI_BRIDGE_TYPE_CROSS_CONNECT != p_bridge_port->bridge_type)
            {
                ctcs_l2_remove_port_from_default_entry(lchip, &l2dflt_addr);
            }
        }

    }
    p_bridge_port->admin_state = admin_state;

    return SAI_STATUS_SUCCESS;

roll_back_1:
    if (admin_state && (SAI_BRIDGE_PORT_TYPE_TUNNEL == p_bridge_port->port_type || SAI_BRIDGE_PORT_TYPE_SUB_PORT == p_bridge_port->port_type))
    {
        ctcs_l2_set_nhid_by_logic_port(lchip, p_bridge_port->logic_port, CTC_NH_RESERVED_NHID_FOR_DROP);
    }

roll_back_0:
    if (admin_state)
    {
        if (SAI_BRIDGE_PORT_TYPE_SUB_PORT == p_bridge_port->port_type)
        {
            sal_memset(&vlan_mapping, 0, sizeof(ctc_vlan_mapping_t));
            vlan_mapping.key = CTC_VLAN_MAPPING_KEY_SVID;
            vlan_mapping.old_svid = p_bridge_port->vlan_id;
            vlan_mapping.action |= CTC_VLAN_MAPPING_OUTPUT_NHID;
            vlan_mapping.u3.nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
            ctcs_vlan_update_vlan_mapping(lchip, p_bridge_port->gport, &vlan_mapping);
        }
        else if (SAI_BRIDGE_PORT_TYPE_TUNNEL == p_bridge_port->port_type)
        {
            if(SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type)
            {
                //ctc_mpls_ilm_old.nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
                ctcs_mpls_update_ilm(lchip, &ctc_mpls_ilm_old);
            }
        }
    }
    return status;
}

/**
 * @brief Bridge port type
 *
 * @type sai_bridge_port_type_t
 * @flags MANDATORY_ON_CREATE | CREATE_ONLY
 */
static sai_status_t
ctc_sai_bridge_port_get_port_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_port_restriction_t port_restriction;            
    sal_memset(&port_restriction, 0, sizeof(ctc_port_restriction_t)); 

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_bridge_port = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_bridge_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_BRIDGE, "object id %"PRIx64" get bridge port attribute id %d\n", key->key.object_id, attr->id);

    CTC_SAI_ATTR_ERROR_RETURN(_ctc_sai_bridge_port_check_port_type_attr(p_bridge_port->port_type, attr->id), attr_idx);

    switch(attr->id)
    {
        case SAI_BRIDGE_PORT_ATTR_TYPE:
            attr->value.s32 = p_bridge_port->port_type;
            break;
        case SAI_BRIDGE_PORT_ATTR_PORT_ID:
            if (CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_bridge_port->gport);
            }
            else
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, p_bridge_port->gport);
            }
            break;
        case SAI_BRIDGE_PORT_ATTR_TAGGING_MODE:
            attr->value.s32 = p_bridge_port->tag_mode;
            break;
        case SAI_BRIDGE_PORT_ATTR_VLAN_ID:
            attr->value.u16 = p_bridge_port->vlan_id;
            break;
        case SAI_BRIDGE_PORT_ATTR_RIF_ID:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, lchip, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, p_bridge_port->l3if_id);
            break;
        case SAI_BRIDGE_PORT_ATTR_TUNNEL_ID:
            attr->value.oid = p_bridge_port->tunnel_id;
            break;
        case SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_1D, 0, p_bridge_port->bridge_id);
            break;
        case SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            break;
        case SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES:
            attr->value.u32 = (p_bridge_port->limit_num == 0xFFFFFFFF)?0:p_bridge_port->limit_num;
            break;
        case SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION:
            CTC_SAI_ERROR_RETURN(_ctc_limit_action_mapping_to_sai_bridge_packet_action(attr, p_bridge_port->limit_action));
            break;
        case SAI_BRIDGE_PORT_ATTR_ADMIN_STATE:
            attr->value.booldata = p_bridge_port->admin_state;
            break;
        case SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING:
            attr->value.booldata = p_bridge_port->ingress_filter;
            break;
        case SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING:
            attr->value.booldata = p_bridge_port->egress_filter;
            break;
        case SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP:               
            attr->value.oid = p_bridge_port->isolation_group_oid;            
            break;            
        case SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT:
            attr->value.oid = p_bridge_port->cross_connect_port;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "bridge port attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }
    
    return status;
}

static sai_status_t
ctc_sai_bridge_port_set_port_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint32 value = 0;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    ctc_security_learn_limit_t learn_limit;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    //ctc_vlan_edit_nh_param_t nh_param;
    //ctc_vlan_egress_edit_info_t edit_info;
    ctc_port_restriction_t port_restriction;
    ctc_object_id_t ctc_object_id;
    ctc_sai_bridge_port_t* p_cross_connect_bport=NULL;
    uint32 bit_cnt = 0;
    ctc_sai_lag_info_t *p_db_lag;
    uint8 gchip = 0;
    sai_object_id_t sai_lag_id;

    
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&port_restriction, 0, sizeof(ctc_port_restriction_t));

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    ctcs_get_gchip_id(lchip, &gchip);
    p_bridge_port = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_bridge_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_BRIDGE, "object id %"PRIx64" set bridge port attribute id %d\n", key->key.object_id, attr->id);

    CTC_SAI_ERROR_RETURN(_ctc_sai_bridge_port_check_port_type_attr(p_bridge_port->port_type, attr->id));

    switch(attr->id)
    {
        case SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
            if (p_bridge_port->admin_state)
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, attr->value.oid, &ctc_oid);
            p_bridge_port->bridge_id = ctc_oid.value;
            break;
        case SAI_BRIDGE_PORT_ATTR_TAGGING_MODE:

            /*
            sal_memset(&nh_param, 0, sizeof(nh_param));
            sal_memset(&edit_info, 0, sizeof(edit_info));
            edit_info.output_svid = p_bridge_port->vlan_id;
            if (attr->value.s32 == SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED)
            {
                edit_info.svlan_edit_type = CTC_VLAN_EGRESS_EDIT_REPLACE_VLAN;
            }
            else if (attr->value.s32 == SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED)
            {
                edit_info.svlan_edit_type = CTC_VLAN_EGRESS_EDIT_STRIP_VLAN;
            }
            else
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }   
            edit_info.edit_flag= CTC_VLAN_EGRESS_EDIT_OUPUT_SVID_VALID;
            nh_param.dsnh_offset = 0;
            nh_param.gport_or_aps_bridge_id = p_bridge_port->gport;
            nh_param.vlan_edit_info = edit_info;
            // need nexthop update interface  
            // CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_xlate(lchip, p_bridge_port->nh_id, &nh_param));             
            p_bridge_port->tag_mode = attr->value.s32;           
            */
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES:
            sal_memset(&learn_limit, 0, sizeof(ctc_security_learn_limit_t));
            learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_PORT;
            learn_limit.gport = p_bridge_port->gport;
            value = attr->value.u32?attr->value.u32:0xFFFFFFFF;
            learn_limit.limit_num = value;
            learn_limit.limit_action = p_bridge_port->limit_action;        
            CTC_SAI_CTC_ERROR_RETURN(ctcs_mac_security_set_learn_limit(lchip, &learn_limit));
            p_bridge_port->limit_num = value;
            break;
        case SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION:            
            sal_memset(&learn_limit, 0, sizeof(ctc_security_learn_limit_t));            
            learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_PORT;
            learn_limit.limit_num = p_bridge_port->limit_num;
            CTC_SAI_ERROR_RETURN(_ctc_sai_bridge_packet_action_mapping_to_limit_action(&value, &(attr->value)));
            learn_limit.limit_action = value;

            if(CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
            {   
                sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_bridge_port->gport);
                p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
                if (NULL == p_db_lag)
                {
                    return SAI_STATUS_INVALID_OBJECT_ID;
                }       
                for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
                {
                    if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                    {
                        learn_limit.gport = CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt);
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_mac_security_set_learn_limit(lchip, &learn_limit));
                         
                    }
                }
            }
            else
            {
                learn_limit.gport = p_bridge_port->gport;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_mac_security_set_learn_limit(lchip, &learn_limit));
            }      
            p_bridge_port->limit_action = value;
            break;
        case SAI_BRIDGE_PORT_ATTR_ADMIN_STATE:
            CTC_SAI_ERROR_RETURN(_ctc_sai_bridge_port_set_admin_state(lchip, p_bridge_port, attr->value.booldata));
            break;
        case SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING:
            value = attr->value.booldata ? TRUE : FALSE;
            if(CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
            {   
                sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_bridge_port->gport);
                p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
                if (NULL == p_db_lag)
                {
                    return SAI_STATUS_INVALID_OBJECT_ID;
                }       
                for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
                {
                    if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                    {
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_vlan_filter_en(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), CTC_INGRESS, value));
                    }
                }
            }
            else
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_vlan_filter_en(lchip, p_bridge_port->gport, CTC_INGRESS, value));
            }

            p_bridge_port->ingress_filter = attr->value.booldata;
            
            break;
        case SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING:
            value = attr->value.booldata ? TRUE : FALSE;
            if(CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
            {   
                sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_bridge_port->gport);
                p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
                if (NULL == p_db_lag)
                {
                    return SAI_STATUS_INVALID_OBJECT_ID;
                }       
                for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
                {
                    if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                    {
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_vlan_filter_en(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), CTC_EGRESS, value));
                    }
                }
            }
            else
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_vlan_filter_en(lchip, p_bridge_port->gport, CTC_EGRESS, value));
            }
            
            p_bridge_port->egress_filter = attr->value.booldata;
            
            break;
        case SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP:
            port_restriction.mode = CTC_PORT_RESTRICTION_PORT_ISOLATION;
            port_restriction.type = CTC_PORT_ISOLATION_ALL;
            port_restriction.dir = CTC_INGRESS;
            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {            
                port_restriction.isolated_id = 0;  // SAI_NULL_OBJECT_ID mean disable
            }
            else
            {
                ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr->value.oid, &ctc_object_id);
                port_restriction.isolated_id = ctc_object_id.value;
            }

            if(CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
            {   
                sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_bridge_port->gport);
                p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
                if (NULL == p_db_lag)
                {
                    return SAI_STATUS_INVALID_OBJECT_ID;
                }       
                for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
                {
                    if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                    {
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_restriction(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &port_restriction));
                    }
                }
            }
            else
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_restriction(lchip, p_bridge_port->gport, &port_restriction));
            }

            p_bridge_port->isolation_group_oid = attr->value.oid;
            break;
        case SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT:

        
            if (p_bridge_port->admin_state)
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            p_cross_connect_bport = ctc_sai_db_get_object_property(lchip, attr->value.oid);
            
            if(NULL != p_cross_connect_bport)
            {
                if(0 != p_cross_connect_bport->nh_id && SAI_BRIDGE_TYPE_CROSS_CONNECT == p_bridge_port->bridge_type)
                {
                    if(SAI_BRIDGE_PORT_TYPE_SUB_PORT != p_bridge_port->port_type && SAI_BRIDGE_PORT_TYPE_TUNNEL != p_bridge_port->port_type)
                    {
                        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "bridge port attribute %d value invalid\n", attr->id);
                        status = SAI_STATUS_INVALID_ATTR_VALUE_0;
                    }
                    else
                    {
                        p_bridge_port->cross_connect_port = attr->value.oid;
                    }
                }
                else
                {
                    CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "bridge port attribute %d value invalid\n", attr->id);
                    status = SAI_STATUS_INVALID_ATTR_VALUE_0;
                }
            }
            else
            {
                CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "bridge port attribute %d value invalid\n", attr->id);
                status = SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "bridge port attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }

    return status;
}

/**
 * @brief Get bridge port statistics counters.
 *
 * @param[in] bridge_port_id Bridge port id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[out] counters Array of resulting counter values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_bridge_get_bridge_port_stats( sai_object_id_t               bridge_port_id,
                                                uint32_t                      number_of_counters,
                                                const sai_stat_id_t *counter_ids,
                                                uint64_t                    *counters)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 index = 0;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    ctc_mac_stats_t mac_rx_stats;
    ctc_mac_stats_t mac_tx_stats;

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(bridge_port_id, &lchip));
    p_bridge_port = ctc_sai_db_get_object_property(lchip, bridge_port_id);
    if (NULL == p_bridge_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if (p_bridge_port->port_type != SAI_BRIDGE_PORT_TYPE_PORT)
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    if(CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    sal_memset(&mac_rx_stats, 0, sizeof(ctc_mac_stats_t));
    sal_memset(&mac_tx_stats, 0, sizeof(ctc_mac_stats_t));
    mac_rx_stats.stats_mode = CTC_STATS_MODE_PLUS;
    mac_tx_stats.stats_mode = CTC_STATS_MODE_PLUS;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_mac_stats(lchip, p_bridge_port->gport, CTC_STATS_MAC_STATS_RX, &mac_rx_stats));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_mac_stats(lchip, p_bridge_port->gport, CTC_STATS_MAC_STATS_TX, &mac_tx_stats));


    for (index = 0; index < number_of_counters; index++)
    {
        switch (counter_ids[index])
        {
            case SAI_BRIDGE_PORT_STAT_IN_OCTETS:
                counters[index] = mac_rx_stats.u.stats_plus.stats.rx_stats_plus.all_octets - p_bridge_port->igs_byte_count;
                break;

            case SAI_BRIDGE_PORT_STAT_OUT_OCTETS:
                counters[index] = mac_tx_stats.u.stats_plus.stats.tx_stats_plus.all_octets - p_bridge_port->egs_byte_count;
                break;

            case SAI_BRIDGE_PORT_STAT_IN_PACKETS:
                counters[index] = mac_rx_stats.u.stats_plus.stats.rx_stats_plus.all_pkts - p_bridge_port->igs_packet_count;
                break;

            case SAI_BRIDGE_PORT_STAT_OUT_PACKETS:
                counters[index] = mac_tx_stats.u.stats_plus.stats.tx_stats_plus.all_pkts - p_bridge_port->egs_packet_count;
                break;

            default:
                CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Unexptected type of counter - %d\n", counter_ids[index]);
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }

    return status;
}

static sai_status_t
ctc_sai_bridge_get_bridge_port_stats_ext( sai_object_id_t               bridge_port_id,
                                                uint32_t                      number_of_counters,
                                                const sai_stat_id_t *counter_ids,
                                                sai_stats_mode_t mode,
                                                uint64_t                    *counters)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 index = 0;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    ctc_mac_stats_t mac_rx_stats;
    ctc_mac_stats_t mac_tx_stats;
    bool tx_en = FALSE;
    bool rx_en = FALSE;

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);
    CTC_SAI_MAX_VALUE_CHECK(mode, SAI_STATS_MODE_READ_AND_CLEAR);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(bridge_port_id, &lchip));
    p_bridge_port = ctc_sai_db_get_object_property(lchip, bridge_port_id);
    if (NULL == p_bridge_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if (p_bridge_port->port_type != SAI_BRIDGE_PORT_TYPE_PORT)
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    if(CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    sal_memset(&mac_rx_stats, 0, sizeof(ctc_mac_stats_t));
    sal_memset(&mac_tx_stats, 0, sizeof(ctc_mac_stats_t));
    mac_rx_stats.stats_mode = CTC_STATS_MODE_PLUS;
    mac_tx_stats.stats_mode = CTC_STATS_MODE_PLUS;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_mac_stats(lchip, p_bridge_port->gport, CTC_STATS_MAC_STATS_RX, &mac_rx_stats));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_mac_stats(lchip, p_bridge_port->gport, CTC_STATS_MAC_STATS_TX, &mac_tx_stats));

    for (index = 0; index < number_of_counters; index++)
    {
        switch (counter_ids[index])
        {
            case SAI_BRIDGE_PORT_STAT_IN_OCTETS:
                rx_en = TRUE;
                counters[index] = mac_rx_stats.u.stats_plus.stats.rx_stats_plus.all_octets - p_bridge_port->igs_byte_count;
                break;

            case SAI_BRIDGE_PORT_STAT_OUT_OCTETS:
                tx_en = TRUE;
                counters[index] = mac_tx_stats.u.stats_plus.stats.tx_stats_plus.all_octets - p_bridge_port->egs_byte_count;
                break;

            case SAI_BRIDGE_PORT_STAT_IN_PACKETS:
                rx_en = TRUE;
                counters[index] = mac_rx_stats.u.stats_plus.stats.rx_stats_plus.all_pkts - p_bridge_port->igs_packet_count;
                break;

            case SAI_BRIDGE_PORT_STAT_OUT_PACKETS:
                tx_en = TRUE;
                counters[index] = mac_tx_stats.u.stats_plus.stats.tx_stats_plus.all_pkts - p_bridge_port->egs_packet_count;
                break;

            default:
                CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Unexptected type of counter - %d\n", counter_ids[index]);
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }

    if (SAI_STATS_MODE_READ_AND_CLEAR == mode)
    {
        if (rx_en)
        {
            p_bridge_port->igs_byte_count = mac_rx_stats.u.stats_plus.stats.rx_stats_plus.all_octets;
            p_bridge_port->igs_packet_count = mac_rx_stats.u.stats_plus.stats.rx_stats_plus.all_pkts;
        }
        if (tx_en)
        {
            p_bridge_port->egs_byte_count = mac_tx_stats.u.stats_plus.stats.tx_stats_plus.all_octets;
            p_bridge_port->egs_packet_count = mac_tx_stats.u.stats_plus.stats.tx_stats_plus.all_pkts;
        }
    }

    return status;
}

/**
 * @brief Clear bridge port statistics counters.
 *
 * @param[in] bridge_port_id Bridge port id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_bridge_clear_bridge_port_stats(sai_object_id_t bridge_port_id,
                                                  uint32_t number_of_counters,
                                                  const sai_stat_id_t* counter_ids)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 index = 0;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    ctc_mac_stats_t mac_rx_stats;
    ctc_mac_stats_t mac_tx_stats;    

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(bridge_port_id, &lchip));
    p_bridge_port = ctc_sai_db_get_object_property(lchip, bridge_port_id);
    if (NULL == p_bridge_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if (p_bridge_port->port_type != SAI_BRIDGE_PORT_TYPE_PORT)
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    if(CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
    
    sal_memset(&mac_rx_stats, 0, sizeof(ctc_mac_stats_t));
    sal_memset(&mac_tx_stats, 0, sizeof(ctc_mac_stats_t));
    mac_rx_stats.stats_mode = CTC_STATS_MODE_PLUS;
    mac_tx_stats.stats_mode = CTC_STATS_MODE_PLUS;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_mac_stats(lchip, p_bridge_port->gport, CTC_STATS_MAC_STATS_RX, &mac_rx_stats));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_mac_stats(lchip, p_bridge_port->gport, CTC_STATS_MAC_STATS_TX, &mac_tx_stats));
    

    for (index = 0; index < number_of_counters; index++)
    {
        switch (counter_ids[index])
        {
            case SAI_BRIDGE_PORT_STAT_IN_OCTETS:
            case SAI_BRIDGE_PORT_STAT_IN_PACKETS:
                p_bridge_port->igs_byte_count = mac_rx_stats.u.stats_plus.stats.rx_stats_plus.all_octets;
                p_bridge_port->igs_packet_count = mac_rx_stats.u.stats_plus.stats.rx_stats_plus.all_pkts;
                break;

            case SAI_BRIDGE_PORT_STAT_OUT_OCTETS:
            case SAI_BRIDGE_PORT_STAT_OUT_PACKETS:
                p_bridge_port->egs_byte_count = mac_tx_stats.u.stats_plus.stats.tx_stats_plus.all_octets;
                p_bridge_port->egs_packet_count = mac_tx_stats.u.stats_plus.stats.tx_stats_plus.all_pkts;
                break;

            default:
                CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Unexptected type of counter - %d\n", counter_ids[index]);
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }

    return status;
}

static sai_status_t
_ctc_sai_bridge_port_alloc(ctc_sai_bridge_port_t** p_bridge_port)
{
    ctc_sai_bridge_port_t* p_bridge_port_temp = NULL;

    p_bridge_port_temp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_bridge_port_t));

    sal_memset(p_bridge_port_temp, 0, sizeof(ctc_sai_bridge_port_t));

    *p_bridge_port = p_bridge_port_temp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_bridge_port_free(ctc_sai_bridge_port_t* p_bridge_port)
{
    mem_free(p_bridge_port);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_bridge_port_create_sub_port(uint8 lchip, ctc_sai_bridge_port_t* p_bridge_port,
                                                uint32_t attr_count, const sai_attribute_t* attr_list)
{
    uint16 vlan_id = 0;
    uint32 logic_port = 0;
    uint32 nh_id = 0;
    uint32 gport = 0;
    uint32 attr_idx = 0;
    ctc_port_scl_property_t port_scl_property;
    ctc_vlan_edit_nh_param_t nh_param;
    ctc_vlan_egress_edit_info_t edit_info;
    const sai_attribute_value_t* attr_val = NULL;
    ctc_object_id_t  ctc_obj_id;
    sai_status_t status = SAI_STATUS_SUCCESS;
    //bool is_first = false
    bool entry_is_first = false;
    ctc_vlan_mapping_t vlan_mapping;
    ctc_vlan_mapping_t vlan_mapping_get;
    uint8 sub_port_or_tunnel_oam_en = 0;
    sai_object_id_t port_oid;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_sai_lag_info_t *p_db_lag = NULL;
    sai_object_id_t sai_lag_id;
    bool is_lag = false;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;

    ctcs_get_gchip_id(lchip, &gchip);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_PORT_ID, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Missing mandatory SAI_BRIDGE_PORT_ATTR_PORT_ID attr\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    sal_memset(&ctc_obj_id, 0, sizeof(ctc_obj_id));
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_val->oid, &ctc_obj_id));
    gport = ctc_obj_id.value;

    if(CTC_IS_LINKAGG_PORT(gport))
    {
        is_lag = true;
        sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
        p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id); 
        if (NULL == p_db_lag)
        {
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto roll_back_0;
        }         
    }
    else
    {
        port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, gport);
        CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(port_oid, &p_port_db));
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_VLAN_ID, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Missing mandatory SAI_BRIDGE_PORT_ATTR_VLAN_ID attr\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    vlan_id = attr_val->u16;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_TAGGING_MODE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        p_bridge_port->tag_mode = SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED;  // default SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED 
    }
    else 
    {
        if ((attr_val->s32 == SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED) || (attr_val->s32 == SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED))
        {
            p_bridge_port->tag_mode = attr_val->s32;
        }
        else
        {
            status = SAI_STATUS_INVALID_ATTR_VALUE_0;
            goto roll_back_0;
        }            
    }

    // vpls, vpws oam enable 
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_OAM_ENABLE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        sub_port_or_tunnel_oam_en = attr_val->booldata;
    }    

    status = ctc_sai_bridge_traverse_get_sub_port_info(lchip, gport, vlan_id, &logic_port);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "bridge sub port already exist, logic_port is %d\n", logic_port);
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_LOGIC_PORT, &logic_port), status, roll_back_0);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id), status, roll_back_1);

    sal_memset(&port_scl_property, 0, sizeof(port_scl_property));
    port_scl_property.scl_id = 0;
    port_scl_property.direction = CTC_INGRESS;
    port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_PORT_SVLAN;
    port_scl_property.action_type = CTC_PORT_SCL_ACTION_TYPE_SCL;
    
    if(is_lag)
    {       
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                ctcs_port_set_scl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &port_scl_property);
                ctcs_port_set_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), CTC_PORT_PROP_REFLECTIVE_BRIDGE_EN, 1);
            }
        }
    }
    else
    {
        ctcs_port_set_scl_property(lchip, gport, &port_scl_property);
        ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_REFLECTIVE_BRIDGE_EN, 1);
    }
    
    sal_memset(&nh_param, 0, sizeof(nh_param));
    sal_memset(&edit_info, 0, sizeof(edit_info));

    edit_info.output_svid = vlan_id;

    if (p_bridge_port->tag_mode == SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED)
    {
        edit_info.svlan_edit_type = CTC_VLAN_EGRESS_EDIT_REPLACE_VLAN;
    }
    else
    {
        edit_info.svlan_edit_type = CTC_VLAN_EGRESS_EDIT_STRIP_VLAN;
    }
    
    edit_info.edit_flag= CTC_VLAN_EGRESS_EDIT_OUPUT_SVID_VALID;
    nh_param.dsnh_offset = 0;
    nh_param.gport_or_aps_bridge_id = gport;
    nh_param.vlan_edit_info = edit_info;
    nh_param.logic_port_check = 1;
    nh_param.logic_port = logic_port;

    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_xlate(lchip, nh_id, &nh_param), status, roll_back_2);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_set_nhid_by_logic_port(lchip, logic_port, 1), status, roll_back_3);
    
    /*port+vlan only, need port/port double vlan subtype FFS*/
    sal_memset(&vlan_mapping, 0, sizeof(ctc_vlan_mapping_t));

    vlan_mapping.key = CTC_VLAN_MAPPING_KEY_SVID;
    vlan_mapping.old_svid = vlan_id;
    vlan_mapping.action |= CTC_VLAN_MAPPING_OUTPUT_NHID;
    vlan_mapping.u3.nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;

    sal_memset(&vlan_mapping_get, 0, sizeof(ctc_vlan_mapping_t));
    vlan_mapping_get.key = CTC_VLAN_MAPPING_KEY_SVID;
    vlan_mapping_get.old_svid = vlan_id;
    
    ctcs_vlan_get_vlan_mapping(lchip, gport, &vlan_mapping_get);

    if(0 == vlan_mapping_get.action)
    {
        entry_is_first = true;
    }
    if(entry_is_first)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_add_vlan_mapping(lchip, gport, &vlan_mapping), status, roll_back_3);
        if(is_lag)
        {
            p_db_lag->sub_port_ref_cnt++;
        }
        else
        {
            p_port_db->sub_port_ref_cnt++;
        }
    }
    else
    {
        goto roll_back_3;
    }
    p_bridge_port->gport = gport;
    p_bridge_port->vlan_id = vlan_id;
    p_bridge_port->port_type = SAI_BRIDGE_PORT_TYPE_SUB_PORT;
    p_bridge_port->logic_port = logic_port;
    p_bridge_port->nh_id = nh_id;
    p_bridge_port->sub_port_or_tunnel_oam_en = sub_port_or_tunnel_oam_en;
    return SAI_STATUS_SUCCESS;

roll_back_3:
    ctcs_nh_remove_xlate(lchip, nh_id);
roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);
roll_back_1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_LOGIC_PORT, logic_port);
roll_back_0:

    return status;
}

static sai_status_t
_ctc_sai_bridge_port_destroy_sub_port(uint8 lchip, ctc_sai_bridge_port_t* p_bridge_port)
{
    ctc_port_scl_property_t port_scl_property;
    ctc_vlan_mapping_t vlan_mapping;
    ctc_sai_port_db_t* p_port_db = NULL;
    sai_object_id_t port_oid;
    ctc_sai_lag_info_t *p_db_lag = NULL;
    sai_object_id_t sai_lag_id;
    bool is_lag = false;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;

    ctcs_get_gchip_id(lchip, &gchip);
    
    if(CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
    {
        is_lag = true;
        sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_bridge_port->gport);
        p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id); 
        if (NULL == p_db_lag)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }
    }
    else
    {    
        port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, p_bridge_port->gport);
        CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(port_oid, &p_port_db));
    }
    
    ctcs_l2_set_nhid_by_logic_port(lchip, p_bridge_port->logic_port, 0);
    ctcs_nh_remove_xlate(lchip, p_bridge_port->nh_id);
    
    sal_memset(&vlan_mapping, 0, sizeof(ctc_vlan_mapping_t));
    vlan_mapping.key = CTC_VLAN_MAPPING_KEY_SVID;
    vlan_mapping.old_svid = p_bridge_port->vlan_id;
    CTC_SAI_ERROR_RETURN(ctcs_vlan_remove_vlan_mapping(lchip, p_bridge_port->gport, &vlan_mapping));

    if(is_lag)
    {
        p_db_lag->sub_port_ref_cnt--;
        if(0 == p_db_lag->sub_port_ref_cnt)
        {
            sal_memset(&port_scl_property, 0, sizeof(ctc_port_scl_property_t));
            port_scl_property.scl_id = 0;
            port_scl_property.direction = CTC_INGRESS;
            port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_DISABLE;            
            for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                {
                    ctcs_port_set_scl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), &port_scl_property);
                    ctcs_port_set_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), CTC_PORT_PROP_REFLECTIVE_BRIDGE_EN, 0);
                }
            }
        }         
    }
    else
    {
        p_port_db->sub_port_ref_cnt--;
        if(0 == p_port_db->sub_port_ref_cnt)
        {
            sal_memset(&port_scl_property, 0, sizeof(ctc_port_scl_property_t));
            port_scl_property.scl_id = 0;
            port_scl_property.direction = CTC_INGRESS;
            port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_DISABLE;
            ctcs_port_set_scl_property(lchip, p_bridge_port->gport, &port_scl_property);
            ctcs_port_set_property(lchip, p_bridge_port->gport, CTC_PORT_PROP_REFLECTIVE_BRIDGE_EN, 0);
        }        
    }

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_bridge_port->nh_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_LOGIC_PORT, p_bridge_port->logic_port);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_bridge_port_create_tunnel_port(uint8 lchip, ctc_sai_bridge_port_t* p_bridge_port,
                                                uint32_t attr_count, const sai_attribute_t* attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 attr_idx = 0;
    const sai_attribute_value_t* attr_val = NULL;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_object_id_t ctc_nhp_id;
    uint8 sub_port_or_tunnel_oam_en = 0;
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_TUNNEL_ID, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Missing mandatory SAI_BRIDGE_PORT_ATTR_TUNNEL_ID attr\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (false == ctc_sai_db_check_object_property_exist(lchip, attr_val->oid))
    {
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        goto roll_back_0;
    }
    
    p_bridge_port->port_type = SAI_BRIDGE_PORT_TYPE_TUNNEL;    
    p_bridge_port->tunnel_id = attr_val->oid;
    p_tunnel = ctc_sai_db_get_object_property(lchip, p_bridge_port->tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, p_tunnel->encap_nexthop_sai, &ctc_nhp_id);
    
    p_bridge_port->nh_id = ctc_nhp_id.value;
    p_bridge_port->logic_port = p_tunnel->logic_port;

    /*vpls, vpws oam enable */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_OAM_ENABLE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        sub_port_or_tunnel_oam_en = attr_val->booldata;
    }
    p_bridge_port->sub_port_or_tunnel_oam_en = sub_port_or_tunnel_oam_en;
    
    return SAI_STATUS_SUCCESS;

roll_back_0:

    return status;
}

static sai_status_t
_ctc_sai_bridge_port_destroy_tunnel_port(uint8 lchip, ctc_sai_bridge_port_t* p_bridge_port)
{
    ctcs_l2_set_nhid_by_logic_port(lchip, p_bridge_port->logic_port, 0);    

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_LOGIC_PORT, p_bridge_port->logic_port);

    p_bridge_port->tunnel_id = 0;
    p_bridge_port->logic_port = 0;

    return SAI_STATUS_SUCCESS;
}

/**
 * @brief Create bridge port
 *
 * @param[out] bridge_port_id Bridge port ID
 * @param[in] switch_id Switch object id
 * @param[in] attr_count number of attributes
 * @param[in] attr_list array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t
ctc_sai_bridge_create_bridge_port(sai_object_id_t* bridge_port_id,
                                               sai_object_id_t        switch_id,
                                               uint32_t               attr_count,
                                               const sai_attribute_t *attr_list)
{
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    uint32 gport = 0;
    uint32 bridge_id = 0;
    uint8 bridge_type = SAI_BRIDGE_TYPE_1Q;
    ctc_object_id_t              ctc_bridge_id = {0};
    ctc_object_id_t              ctc_bridge_port_id = {0};
    ctc_object_id_t              ctc_obj_id    = {0};
    sai_object_id_t              lag_oid = {0};
    const sai_attribute_value_t *attr_val = NULL, *ingress_filter = NULL, *egress_filter = NULL;
    sai_bridge_port_type_t       bport_type = 0;
    uint32                       attr_idx = 0;
    uint8 lchip = 0;
    bool ingress_filter_en = FALSE;
    bool admin_state = FALSE;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_security_learn_limit_t learn_limit;
    uint32 value = 0;
    ctc_sai_lag_info_t *p_db_lag;
    bool is_lag_port = FALSE;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;
    sai_object_id_t sai_lag_id;    
    
    CTC_SAI_PTR_VALID_CHECK(bridge_port_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);
    
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SWITCH, switch_id, &ctc_obj_id));
    lchip = ctc_obj_id.lchip;

    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_TYPE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Missing mandatory SAI_BRIDGE_PORT_ATTR_TYPE attr\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    bport_type = attr_val->s32;            

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_BRIDGE_ID, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        CTC_SAI_CTC_ERROR_GOTO(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, attr_val->oid, &ctc_bridge_id), status, roll_back_0);
        bridge_id = ctc_bridge_id.value;
        bridge_type = ctc_bridge_id.sub_type;
    }
    else
    {
        p_switch_master = ctc_sai_get_switch_property(lchip);
        if (NULL == p_switch_master)
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_FAILURE;
        }
        bridge_id = p_switch_master->default_bridge_id;
    }

    status = _ctc_sai_bridge_port_alloc(&p_bridge_port);
    
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Failed to allocate bridge port entry\n");
        goto roll_back_0;
    }
    else
    {
        p_bridge_port->bridge_id = bridge_id;
        p_bridge_port->bridge_type = bridge_type;
    }

    switch (bport_type)
    {
        case SAI_BRIDGE_PORT_TYPE_PORT:
            
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_PORT_ID, &attr_val, &attr_idx);
            if (CTC_SAI_ERROR(status))
            {
                CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Missing mandatory SAI_BRIDGE_PORT_ATTR_PORT_ID attr\n");
                status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
                goto roll_back_0;
            }

            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_val->oid, &ctc_obj_id);
            gport = ctc_obj_id.value;

            if(CTC_IS_LINKAGG_PORT(gport))
            {
                is_lag_port = TRUE;
            }
            
            CTC_SAI_LOG_INFO(SAI_API_BRIDGE, "The Bridge port bind gport 0x%x\n", gport);

            CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_bridge_port_check_global_port(gport), status, roll_back_0);
            
            if (CTC_IS_CPU_PORT(gport))
            {
                CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Invalid port id - CPU port\n");
                status = SAI_STATUS_INVALID_ATTR_VALUE_0 + attr_idx;
                goto roll_back_0;
            }


            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING,
                                                 &ingress_filter, &attr_idx);
            if (!CTC_SAI_ERROR(status))
            {
                if (bport_type != SAI_BRIDGE_PORT_TYPE_PORT)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Ingress filter is only supported for bridge port type port\n");
                    status = SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
                    goto roll_back_0;
                }
            }
            
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING,
                                                 &egress_filter, &attr_idx);
            if (!CTC_SAI_ERROR(status))
            {
                if (bport_type != SAI_BRIDGE_PORT_TYPE_PORT)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Egress filter is only supported for bridge port type port\n");
                    status = SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
                    goto roll_back_0;
                }
            }              

            if (ingress_filter)
            {
                ingress_filter_en = ingress_filter->booldata ? TRUE : FALSE;

                if(is_lag_port)
                {
                    sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
                    p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
                    if (NULL == p_db_lag)
                    {
                        status = SAI_STATUS_INVALID_OBJECT_ID;
                        goto roll_back_0;
                    }       
                    for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
                    {
                        if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                        {
                            CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_vlan_filter_en(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt),  CTC_INGRESS, ingress_filter_en), status, roll_back_0);                           
                        }
                    }   
                }
                else
                {
                    status = ctcs_port_set_vlan_filter_en(lchip, gport,  CTC_INGRESS, ingress_filter_en);
                }
                
                if (CTC_SAI_ERROR(status))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Failed to set port %x ingress filter.\n", gport);
                    goto roll_back_0;
                }
            }

            if (egress_filter)
            {
                ingress_filter_en = egress_filter->booldata ? TRUE : FALSE;


                if(is_lag_port)
                {
                    sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
                    p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
                    if (NULL == p_db_lag)
                    {
                        status = SAI_STATUS_INVALID_OBJECT_ID;
                        goto roll_back_0;
                    }       
                    for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
                    {
                        if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                        {
                            CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_vlan_filter_en(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt),  CTC_EGRESS, ingress_filter_en), status, roll_back_0);                           
                        }
                    }   
                }
                else
                {
                    status = ctcs_port_set_vlan_filter_en(lchip, gport,  CTC_EGRESS, ingress_filter_en);
                }

                if (CTC_SAI_ERROR(status))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Failed to set port %x egress filter.\n", gport);
                    goto roll_back_0;
                }
            }

            sal_memset(&learn_limit, 0, sizeof(ctc_security_learn_limit_t));
            learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_PORT;
            learn_limit.gport = gport;

            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, &attr_val, &attr_idx);
            if (status == SAI_STATUS_SUCCESS )
            {
                learn_limit.limit_num = attr_val->u32?attr_val->u32:0xFFFFFFFF;   
            }
            else  // default 0, mean disable mac learning limit
            {
                learn_limit.limit_num = 0xFFFFFFFF;             
            }

            p_bridge_port->limit_num = learn_limit.limit_num; 

            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, &attr_val, &attr_idx);
            if (status == SAI_STATUS_SUCCESS)
            {
                CTC_SAI_ERROR_GOTO(_ctc_sai_bridge_packet_action_mapping_to_limit_action(&value, attr_val), status, roll_back_0);
                learn_limit.limit_action = value;
            }
            else
            {
                learn_limit.limit_action = CTC_MACLIMIT_ACTION_DISCARD;  // default SAI_PACKET_ACTION_DROP 
            }

            p_bridge_port->limit_action = learn_limit.limit_action;


            if(is_lag_port)
            {
                sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
                p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
                if (NULL == p_db_lag)
                {
                    status = SAI_STATUS_INVALID_OBJECT_ID;
                    goto roll_back_0;
                }       
                for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
                {
                    if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                    {
                        learn_limit.gport = CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt);
                        CTC_SAI_ERROR_GOTO(ctcs_mac_security_set_learn_limit(lchip, &learn_limit), status, roll_back_0);
                    }
                }   
            }
            else
            {
                CTC_SAI_ERROR_GOTO(ctcs_mac_security_set_learn_limit(lchip, &learn_limit), status, roll_back_0);
            }
            
            p_bridge_port->gport = gport;
            p_bridge_port->port_type = SAI_BRIDGE_PORT_TYPE_PORT;
            ctc_bridge_port_id.lchip = lchip;
            ctc_bridge_port_id.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
            ctc_bridge_port_id.sub_type = SAI_BRIDGE_PORT_TYPE_PORT;
            ctc_bridge_port_id.value = gport;
            ctc_bridge_port_id.value2 = 0;
            break;

        case SAI_BRIDGE_PORT_TYPE_SUB_PORT:
            CTC_SAI_ERROR_GOTO(_ctc_sai_bridge_port_create_sub_port(lchip, p_bridge_port, attr_count, attr_list), status, roll_back_0);
            ctc_bridge_port_id.lchip = lchip;
            ctc_bridge_port_id.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
            ctc_bridge_port_id.sub_type = SAI_BRIDGE_PORT_TYPE_SUB_PORT;
            ctc_bridge_port_id.value = p_bridge_port->logic_port;
            ctc_bridge_port_id.value2 = 0;          
            break;
        case SAI_BRIDGE_PORT_TYPE_1Q_ROUTER:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            goto roll_back_0;

        case SAI_BRIDGE_PORT_TYPE_1D_ROUTER:
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_RIF_ID, &attr_val, &attr_idx);
            if (CTC_SAI_ERROR(status))
            {
                CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Missing mandatory SAI_BRIDGE_PORT_ATTR_RIF_ID attr\n");
                status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
                goto roll_back_0;
            }
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_val->oid, &ctc_obj_id);
            p_bridge_port->l3if_id = ctc_obj_id.value;
            p_bridge_port->port_type = SAI_BRIDGE_PORT_TYPE_1D_ROUTER;
            ctc_bridge_port_id.lchip = lchip;
            ctc_bridge_port_id.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
            ctc_bridge_port_id.sub_type = SAI_BRIDGE_PORT_TYPE_1D_ROUTER;
            ctc_bridge_port_id.value = ctc_obj_id.value;
            ctc_bridge_port_id.value2 = 0;
            break;

        case SAI_BRIDGE_PORT_TYPE_TUNNEL:
            CTC_SAI_ERROR_GOTO(_ctc_sai_bridge_port_create_tunnel_port(lchip, p_bridge_port, attr_count, attr_list), status, roll_back_0);
            ctc_bridge_port_id.lchip = lchip;
            ctc_bridge_port_id.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
            ctc_bridge_port_id.sub_type = SAI_BRIDGE_PORT_TYPE_TUNNEL;
            ctc_bridge_port_id.value = p_bridge_port->logic_port;
            ctc_bridge_port_id.value2 = 0;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Unsupported bridge port type %d\n", attr_val->s32);
            status = SAI_STATUS_INVALID_ATTR_VALUE_0 + attr_idx;
            goto roll_back_0;
    }
    

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE, &attr_val, &attr_idx);
    if (status == SAI_STATUS_SUCCESS )
    {
        status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
        goto roll_back_0;

    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        admin_state = false;
    }
    else
    {
        admin_state = attr_val->booldata;
    }
    CTC_SAI_ERROR_GOTO(_ctc_sai_bridge_port_set_admin_state(lchip, p_bridge_port, admin_state), status, roll_back_1);

    CTC_SAI_ERROR_GOTO(ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, &ctc_bridge_port_id, bridge_port_id), status, roll_back_2);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *bridge_port_id, p_bridge_port), status, roll_back_2);


    if(CTC_IS_LINKAGG_PORT(p_bridge_port->gport))
    {
        lag_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_bridge_port->gport);
        p_db_lag = ctc_sai_db_get_object_property(lchip, lag_oid);
        if (NULL == p_db_lag)
        {
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto roll_back_3;
        } 
        if (bport_type == SAI_BRIDGE_PORT_TYPE_PORT ) 
        {
            p_db_lag->bind_bridge_port_type = 1;
        }
        if (bport_type == SAI_BRIDGE_PORT_TYPE_SUB_PORT)
        {
            p_db_lag->bind_bridge_port_type = 2;
        }

        ctc_sai_lag_register_member_change_cb(lchip, CTC_SAI_LAG_MEM_CHANGE_TYPE_BRIDGE_PORT, p_bridge_port->gport, _ctc_sai_bridge_port_lag_member_change_cb_fn);

    }

/*
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP, &attr_val, &attr_idx);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *bridge_port_id };
        CTC_SAI_ERROR_GOTO(ctc_sai_bridge_port_set_port_property(&key, &attr_list[attr_idx]), status, roll_back_3);
    }
*/

    CTC_SAI_DB_UNLOCK(lchip);


    return SAI_STATUS_SUCCESS;

roll_back_3:
    ctc_sai_db_remove_object_property(lchip, *bridge_port_id);

roll_back_2:
    if (admin_state)
    {
        _ctc_sai_bridge_port_set_admin_state(lchip, p_bridge_port, false);
    }
    
roll_back_1:
    if (SAI_BRIDGE_PORT_TYPE_SUB_PORT == bport_type)
    {
        _ctc_sai_bridge_port_destroy_sub_port(lchip, p_bridge_port);
    }
    else if (SAI_BRIDGE_PORT_TYPE_TUNNEL == bport_type)
    {
        _ctc_sai_bridge_port_destroy_tunnel_port(lchip, p_bridge_port);
    }

roll_back_0:
    if (CTC_SAI_ERROR(status))
    {
        _ctc_sai_bridge_port_free(p_bridge_port);
    }

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}


/**
 * @brief Remove bridge port
 *
 * @param[in] bridge_port_id Bridge port ID
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t ctc_sai_bridge_remove_bridge_port( sai_object_id_t bridge_port_id)
{
    uint8 lchip = 0;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(bridge_port_id, &lchip));
    p_bridge_port = ctc_sai_db_get_object_property(lchip, bridge_port_id);
    if (NULL == p_bridge_port)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if (p_bridge_port->admin_state && p_bridge_port->bridge_type != SAI_BRIDGE_PORT_TYPE_PORT )
    {
        _ctc_sai_bridge_port_set_admin_state(lchip, p_bridge_port, false);
    }

    if (p_bridge_port->port_type == SAI_BRIDGE_PORT_TYPE_SUB_PORT)
    {
        _ctc_sai_bridge_port_destroy_sub_port(lchip, p_bridge_port);
    }
    else if (SAI_BRIDGE_PORT_TYPE_TUNNEL == p_bridge_port->port_type)
    {
        _ctc_sai_bridge_port_destroy_tunnel_port(lchip, p_bridge_port);
    }

    ctc_sai_db_remove_object_property(lchip, bridge_port_id);
    _ctc_sai_bridge_port_free(p_bridge_port);

    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t brg_port_attr_fn_entries[] = {
    {SAI_BRIDGE_PORT_ATTR_TYPE, ctc_sai_bridge_port_get_port_property, NULL},
    {SAI_BRIDGE_PORT_ATTR_PORT_ID, ctc_sai_bridge_port_get_port_property, NULL},
    {SAI_BRIDGE_PORT_ATTR_VLAN_ID, ctc_sai_bridge_port_get_port_property, NULL},
    {SAI_BRIDGE_PORT_ATTR_RIF_ID, ctc_sai_bridge_port_get_port_property, NULL},
    {SAI_BRIDGE_PORT_ATTR_TUNNEL_ID, ctc_sai_bridge_port_get_port_property, NULL},
    {SAI_BRIDGE_PORT_ATTR_BRIDGE_ID, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {SAI_BRIDGE_PORT_ATTR_TAGGING_MODE, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, ctc_sai_bridge_port_get_port_property, ctc_sai_bridge_port_set_port_property},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
 };

/**
 * @brief Set attribute for bridge port
 *
 * @param[in] bridge_port_id Bridge port ID
 * @param[in] attr attribute to set
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t ctc_sai_bridge_set_bridge_port_attribute(sai_object_id_t bridge_port_id,
                                                    const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = bridge_port_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(bridge_port_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = bridge_port_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_BRIDGE_PORT, brg_port_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

/**
 * @brief Get attributes of bridge port
 *
 * @param[in] bridge_port_id Bridge port ID
 * @param[in] attr_count number of attributes
 * @param[inout] attr_list array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t ctc_sai_bridge_get_bridge_port_attribute( sai_object_id_t  brg_port_oid,
                                                    uint32_t            attr_count,
                                                    sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = brg_port_oid };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(brg_port_oid, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = brg_port_oid;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_BRIDGE_PORT, loop, brg_port_attr_fn_entries,&attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________Bridge______

static sai_status_t
_ctc_sai_bridge_get_port_list_from_db(ctc_sai_oid_property_t* bucket_data, sai_attribute_t* user_data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_bridge_port_t* p_bridge_port = (ctc_sai_bridge_port_t*)bucket_data->data;

    if (p_bridge_port->bridge_id == user_data->id)
    {
        user_data->value.objlist.list[user_data->value.objlist.count++] = bucket_data->oid;
    }

    return status;
}
/**
 * @brief List of bridge ports associated to this bridge
 *
 * @type sai_object_list_t
 * @objects SAI_OBJECT_TYPE_BRIDGE_PORT
 * @flags READ_ONLY
 */
static sai_status_t
ctc_sai_bridge_get_port_list(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    ctc_object_id_t ctc_oid = {0};
    sai_status_t     status = SAI_STATUS_SUCCESS;
    uint16 bridge_id = 0;
    uint32 count = 0;
    sai_attribute_t attr_temp;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);
    status = ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, key->key.object_id, &ctc_oid);
    bridge_id = ctc_oid.value;
    lchip = ctc_oid.lchip;

    CTC_SAI_ERROR_RETURN(ctc_sai_db_get_object_property_count(lchip, SAI_OBJECT_TYPE_BRIDGE_PORT, &count));
    sal_memset(&attr_temp, 0, sizeof(sai_attribute_t));
    attr_temp.value.objlist.list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*count);
    if (NULL == attr_temp.value.objlist.list)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    attr_temp.id = bridge_id;
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BRIDGE_PORT, (hash_traversal_fn)_ctc_sai_bridge_get_port_list_from_db, (void*)&attr_temp);

    CTC_SAI_ERROR_GOTO(ctc_sai_fill_object_list(sizeof(sai_object_id_t),attr_temp.value.objlist.list,attr_temp.value.objlist.count, &attr->value.objlist), status, roll_back_0);

roll_back_0:
    mem_free(attr_temp.value.objlist.list);

    return status;
}

static sai_status_t
ctc_sai_bridge_get_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 value = 0;
    uint16 fid = 0;

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, key->key.object_id, &ctc_object_id));
    CTC_SAI_LOG_INFO(SAI_API_BRIDGE, "object id %"PRIx64" get bridge attribute id %d\n", key->key.object_id, attr->id);

    if(SAI_BRIDGE_TYPE_CROSS_CONNECT == ctc_object_id.sub_type && SAI_BRIDGE_ATTR_TYPE != attr->id)
    {
        status = SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
        return status;
    }
    
    fid = ctc_object_id.value;
    switch(attr->id)
    {
        case SAI_BRIDGE_ATTR_TYPE:
            attr->value.s32 = ctc_object_id.sub_type;
            break;
        case SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
            {
                ctc_security_learn_limit_t learn_limit;
                sal_memset(&learn_limit, 0, sizeof(ctc_security_learn_limit_t));
                learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_VLAN;
                learn_limit.vlan = fid;
                CTC_SAI_ATTR_ERROR_RETURN(ctcs_mac_security_get_learn_limit(lchip, &learn_limit), attr_idx);
                attr->value.u32 = (learn_limit.limit_num==0xFFFFFFFF)?0:learn_limit.limit_num;
            }
            break;
        case SAI_BRIDGE_ATTR_LEARN_DISABLE:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_vlan_get_property(lchip, fid, CTC_VLAN_PROP_LEARNING_EN, &value), attr_idx);
            attr->value.booldata = value?0:1;
            break;
        case SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_vlan_get_property(lchip, fid, CTC_VLAN_PROP_DROP_UNKNOWN_UCAST_EN, &value), attr_idx);
            if (0 == value)
            {
                attr->value.s32 = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS;
            }
            else
            {
                attr->value.s32 = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE;
            }
            break;
        case SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;;
            break;

        case SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_vlan_get_property(lchip, fid, CTC_VLAN_PROP_DROP_UNKNOWN_MCAST_EN, &value), attr_idx);
            if (0 == value)
            {
                attr->value.s32 = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS;
            }
            else
            {
                attr->value.s32 = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE;
            }
            break;
        case SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;;
            break;

        case SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_vlan_get_property(lchip, fid, CTC_VLAN_PROP_DROP_UNKNOWN_BCAST_EN, &value), attr_idx);
            if (0 == value)
            {
                attr->value.s32 = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS;
            }
            else
            {
                attr->value.s32 = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE;
            }
            break;
        case SAI_BRIDGE_ATTR_BROADCAST_FLOOD_GROUP:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            break;

        default:
            CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "bridge attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static sai_status_t
ctc_sai_bridge_set_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 value = 0;
    uint16 fid = 0;

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, key->key.object_id, &ctc_object_id));
    CTC_SAI_LOG_INFO(SAI_API_BRIDGE, "object id %"PRIx64"set bridge attribute id %d\n", key->key.object_id, attr->id);

    if(SAI_BRIDGE_TYPE_CROSS_CONNECT == ctc_object_id.sub_type)
    {
        status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
        return status;
    }
    
    fid = ctc_object_id.value;
    switch(attr->id)
    {
        case SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
            {
                ctc_security_learn_limit_t learn_limit;
                sal_memset(&learn_limit, 0, sizeof(ctc_security_learn_limit_t));
                learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_VLAN;
                learn_limit.vlan = fid;
                value = attr->value.u32?attr->value.u32:0xFFFFFFFF;
                learn_limit.limit_num = value;
                learn_limit.limit_action = CTC_MACLIMIT_ACTION_FWD;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_mac_security_set_learn_limit(lchip, &learn_limit));
            }
            break;
        case SAI_BRIDGE_ATTR_LEARN_DISABLE:
            value = attr->value.booldata?0:1;
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_vlan_set_property(lchip, fid, CTC_VLAN_PROP_LEARNING_EN, value), 0);
            break;
        case SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
            value = attr->value.s32;
            if (SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == value)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_property(lchip, fid, CTC_VLAN_PROP_DROP_UNKNOWN_UCAST_EN, 0));
            }
            else if (SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE == value)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_property(lchip, fid, CTC_VLAN_PROP_DROP_UNKNOWN_UCAST_EN, 1));
            }
            else if ((SAI_BRIDGE_FLOOD_CONTROL_TYPE_L2MC_GROUP == value) || (SAI_BRIDGE_FLOOD_CONTROL_TYPE_COMBINED == value))
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            }
            else
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            break;
        case SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
            value = attr->value.s32;
            if (SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == value)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_property(lchip, fid, CTC_VLAN_PROP_DROP_UNKNOWN_MCAST_EN, 0));
            }
            else if (SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE == value)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_property(lchip, fid, CTC_VLAN_PROP_DROP_UNKNOWN_MCAST_EN, 1));
            }
            else if ((SAI_BRIDGE_FLOOD_CONTROL_TYPE_L2MC_GROUP == value) || (SAI_BRIDGE_FLOOD_CONTROL_TYPE_COMBINED == value))
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            }
            else
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            break;
        case SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;

        case SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
            value = attr->value.s32;
            if (SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == value)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_property(lchip, fid, CTC_VLAN_PROP_DROP_UNKNOWN_BCAST_EN, 0));
            }
            else if (SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE == value)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_property(lchip, fid, CTC_VLAN_PROP_DROP_UNKNOWN_BCAST_EN, 1));
            }
            else if ((SAI_BRIDGE_FLOOD_CONTROL_TYPE_L2MC_GROUP == value) || (SAI_BRIDGE_FLOOD_CONTROL_TYPE_COMBINED == value))
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            }
            else
            {
                return SAI_STATUS_INVALID_ATTR_VALUE_0;
            }
            break;
        case SAI_BRIDGE_ATTR_BROADCAST_FLOOD_GROUP:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;

        default:
            CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "bridge attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t brg_attr_fn_entries[] = {
    {SAI_BRIDGE_ATTR_TYPE, ctc_sai_bridge_get_property, NULL},
    {SAI_BRIDGE_ATTR_PORT_LIST, ctc_sai_bridge_get_port_list, NULL},
    {SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES, ctc_sai_bridge_get_property, ctc_sai_bridge_set_property},
    {SAI_BRIDGE_ATTR_LEARN_DISABLE, ctc_sai_bridge_get_property, ctc_sai_bridge_set_property},
    {SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, ctc_sai_bridge_get_property, ctc_sai_bridge_set_property},
    {SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP, ctc_sai_bridge_get_property, ctc_sai_bridge_set_property},
    {SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, ctc_sai_bridge_get_property, ctc_sai_bridge_set_property},
    {SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP, ctc_sai_bridge_get_property, ctc_sai_bridge_set_property},
    {SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, ctc_sai_bridge_get_property, ctc_sai_bridge_set_property},
    {SAI_BRIDGE_ATTR_BROADCAST_FLOOD_GROUP, ctc_sai_bridge_get_property, ctc_sai_bridge_set_property},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

static sai_status_t 
ctc_sai_bridge_create_bridge(
         sai_object_id_t *bridge_id,
         sai_object_id_t switch_id,
         uint32_t attr_count,
         const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint32 value = 0;
    const sai_attribute_value_t *attr_val  = NULL;
    uint32_t                     attr_idx;
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    uint32_t                     fid = 0;
    ctc_object_id_t ctc_switch_id;
    ctc_l2dflt_addr_t l2dflt_addr;
    sai_object_key_t key;
    uint8 is_vpws = 0;
    
    CTC_SAI_PTR_VALID_CHECK(bridge_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    sal_memset(&ctc_switch_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&l2dflt_addr, 0, sizeof(ctc_l2dflt_addr_t));
    sal_memset(&key, 0, sizeof(sai_object_key_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_ATTR_TYPE, &attr_val, &attr_idx));
    if(SAI_BRIDGE_TYPE_1D != attr_val->s32)
    {
        if(SAI_BRIDGE_TYPE_CROSS_CONNECT == attr_val->s32)
        {
            is_vpws = 1;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_BRIDGE,"Not supported bridge type %d\n", attr_val->s32);
            return SAI_STATUS_INVALID_PARAMETER;
        }
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SWITCH, switch_id, &ctc_switch_id));
    lchip = ctc_switch_id.lchip;
    if(0 == is_vpws)
    {
        /* alloc fid (0k~4k)  from opf    --> scl --> fid , set fid property <4k */
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_VLAN, &fid));
        CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_create_vlan(lchip, fid), status, roll_back_0);
        CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_set_fid(lchip, fid, fid), status, roll_back_1);
        CTC_SAI_DB_LOCK(lchip);
        *bridge_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_1D, 0, fid);
        CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *bridge_id, NULL), status, roll_back_2);
        /* set  vlan mac limit */
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES,
                                     &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            key.key.object_id = *bridge_id;
            CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL,
                            SAI_OBJECT_TYPE_BRIDGE, brg_attr_fn_entries, &attr_list[attr_idx]), status, roll_back_3);
        }
    
        /* set fid learn */
        value = 1;
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BRIDGE_ATTR_LEARN_DISABLE,
                                     &attr_val, &attr_idx);
        if (status == SAI_STATUS_SUCCESS)
        {
            value = attr_val->booldata?0:1;
        }
        CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_set_property(lchip, fid, CTC_VLAN_PROP_LEARNING_EN, value), status, roll_back_3);
    
        l2dflt_addr.l2mc_grp_id = fid;
        l2dflt_addr.fid = fid;
        CTC_SET_FLAG(l2dflt_addr.flag, CTC_L2_DFT_VLAN_FLAG_USE_LOGIC_PORT );
        CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_add_default_entry(lchip, &l2dflt_addr), status, roll_back_3);
    }
    else
    {
        CTC_SAI_DB_LOCK(lchip);
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_VPWS, &fid));
        *bridge_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_CROSS_CONNECT, 0, fid);
        CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *bridge_id, NULL), status, roll_back_2);
    }
    
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;
roll_back_3:
    ctc_sai_db_remove_object_property(lchip, *bridge_id);

roll_back_2:
    CTC_SAI_DB_UNLOCK(lchip);

roll_back_1:
    if(!is_vpws)
    {
        ctcs_vlan_destroy_vlan(lchip, fid);
    }

roll_back_0:
    if(!is_vpws)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_VLAN, fid);
    }
    else
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_VPWS, fid);
    }
    return status;
}

/**
 * @brief Remove bridge
 *
 * @param[in] bridge_id Bridge ID
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t
ctc_sai_bridge_remove_bridge( sai_object_id_t bridge_id)
{
    uint32 fid = 0;
    uint8 lchip = 0;
    ctc_object_id_t ctc_oid;
    ctc_l2dflt_addr_t l2dflt_addr;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_bridge_id;
    if (false == ctc_sai_db_check_object_exist(bridge_id))
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&l2dflt_addr, 0, sizeof(ctc_l2dflt_addr_t));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, bridge_id, &ctc_bridge_id);
    if(SAI_BRIDGE_TYPE_1D == ctc_bridge_id.sub_type)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_BRIDGE_TYPE_1D, bridge_id, &ctc_oid));
        lchip = ctc_oid.lchip;
        fid = ctc_oid.value & 0xFFFF;
    
        CTC_SAI_DB_LOCK(lchip);
        
        ctc_security_learn_limit_t learn_limit;
        sal_memset(&learn_limit, 0, sizeof(ctc_security_learn_limit_t));
        learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_VLAN;
        learn_limit.vlan = fid;
        learn_limit.limit_num = 0xFFFFFFFF;
        learn_limit.limit_action = CTC_MACLIMIT_ACTION_FWD;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_mac_security_set_learn_limit(lchip, &learn_limit), status, out);
                    
        ctcs_vlan_destroy_vlan(lchip, fid);
        /*free fid (0k~4k)  from opf    --> scl --> fid ,set fid property <4k*/
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_VLAN, fid);
    
        l2dflt_addr.l2mc_grp_id = fid;
        l2dflt_addr.fid = fid;
        CTC_SET_FLAG(l2dflt_addr.flag, CTC_L2_DFT_VLAN_FLAG_USE_LOGIC_PORT);
        ctcs_l2_remove_default_entry(lchip, &l2dflt_addr);
    
    }
    else if(SAI_BRIDGE_TYPE_CROSS_CONNECT == ctc_bridge_id.sub_type)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_BRIDGE_TYPE_CROSS_CONNECT, bridge_id, &ctc_oid));
        fid = ctc_oid.value & 0xFFFF;
        
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_VPWS, fid);
    }
    else
    {
        return SAI_STATUS_OBJECT_IN_USE;
    }
    ctc_sai_db_remove_object_property(lchip, bridge_id);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Failed to remove bridge %d\n", status);
    }
    return status;
}

/**
 * @brief Set attribute for bridge
 *
 * @param[in] bridge_id Bridge ID
 * @param[in] attr attribute to set
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t
ctc_sai_bridge_set_bridge_attribute( sai_object_id_t bridge_id, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = bridge_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(bridge_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = bridge_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_BRIDGE, brg_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

/**
 * @brief Get attributes of bridge
 *
 * @param[in] bridge_id Bridge ID
 * @param[in] attr_count number of attributes
 * @param[inout] attr_list array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t
ctc_sai_bridge_get_bridge_attribute( sai_object_id_t     bridge_id,
                                               uint32_t            attr_count,
                                               sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = bridge_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(bridge_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = bridge_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_BRIDGE, loop, brg_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}


/**
 * @brief Get bridge statistics counters.
 *
 * @param[in] bridge_id Bridge id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[out] counters Array of resulting counter values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_bridge_get_bridge_stats( sai_object_id_t          bridge_id,
                                           uint32_t                 number_of_counters,
                                           const sai_stat_id_t *counter_ids,
                                           uint64_t               *counters)
{
    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    return SAI_STATUS_NOT_IMPLEMENTED;
}

static sai_status_t
ctc_sai_bridge_get_bridge_stats_ext( sai_object_id_t          bridge_id,
                                           uint32_t                 number_of_counters,
                                           const sai_stat_id_t *counter_ids,
                                           sai_stats_mode_t mode,
                                           uint64_t               *counters)
{
    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    return SAI_STATUS_NOT_IMPLEMENTED;
}

/**
 * @brief Clear bridge statistics counters.
 *
 * @param[in] bridge_id Bridge id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_bridge_clear_bridge_stats( sai_object_id_t          bridge_id,
                                             uint32_t                 number_of_counters,
                                              const sai_stat_id_t *counter_ids)
{
    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    return SAI_STATUS_NOT_IMPLEMENTED;
}

sai_bridge_api_t g_ctc_sai_bridge_api = {
     ctc_sai_bridge_create_bridge,
     ctc_sai_bridge_remove_bridge,
     ctc_sai_bridge_set_bridge_attribute,
     ctc_sai_bridge_get_bridge_attribute,
     ctc_sai_bridge_get_bridge_stats,
     ctc_sai_bridge_get_bridge_stats_ext,
     ctc_sai_bridge_clear_bridge_stats,
     ctc_sai_bridge_create_bridge_port,
     ctc_sai_bridge_remove_bridge_port,
     ctc_sai_bridge_set_bridge_port_attribute,
     ctc_sai_bridge_get_bridge_port_attribute,
     ctc_sai_bridge_get_bridge_port_stats,
     ctc_sai_bridge_get_bridge_port_stats_ext,
     ctc_sai_bridge_clear_bridge_port_stats
};

#define ________INTERNAL_API________
sai_status_t
ctc_sai_bridge_get_fid(sai_object_id_t bv_id, uint16 *fid)
{
    void *p_db = NULL;
    uint8 oid_type = 0;
    uint8 lchip = 0;

    CTC_SAI_PTR_VALID_CHECK(fid);
    *fid = 0;
    ctc_sai_oid_get_lchip(bv_id, &lchip);
    oid_type = sai_object_type_query(bv_id);
    if (oid_type == SAI_OBJECT_TYPE_VLAN)
    {
        p_db = ctc_sai_db_get_object_property(lchip, bv_id);
        if (NULL == p_db)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }
        *fid = ((ctc_sai_vlan_user_t  *)p_db)->user_vlanptr;
    }
    else if(oid_type == SAI_OBJECT_TYPE_BRIDGE)
    {
        if (false == ctc_sai_db_check_object_exist(bv_id))
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }
        
        ctc_object_id_t              ctc_bridge_id;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, bv_id, &ctc_bridge_id);
        *fid = ctc_bridge_id.value;
    }
    else
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_bridge_traverse_get_bridge_port_info(uint8 lchip, uint16 bridge_id, uint16 logic_port, uint32* gport, uint16* vlan_id)
{
    ctc_sai_bridge_traverse_param_t traverse_param;

    CTC_SAI_PTR_VALID_CHECK(gport);
    CTC_SAI_PTR_VALID_CHECK(vlan_id);

    sal_memset(&traverse_param, 0, sizeof(traverse_param));
    traverse_param.lchip = lchip;
    traverse_param.sucess = 0;
    traverse_param.cmp_value1 = (void*)(&bridge_id);
    traverse_param.cmp_value2 = (void*)(&logic_port);
    traverse_param.out_value1 = (void*)gport;
    traverse_param.out_value2 = (void*)vlan_id;
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BRIDGE_PORT, (hash_traversal_fn)_ctc_sai_bridge_port_traverse_get_cb, (void*)(&traverse_param));
    if (0 == traverse_param.sucess)
    {
        return SAI_STATUS_FAILURE;
    }
    return SAI_STATUS_SUCCESS;
}




#define ________BRIDGE_WB________

static sai_status_t
_ctc_sai_bridge_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_id_t bridge_id = *(sai_object_id_t*)key;
    ctc_object_id_t ctc_oid;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, bridge_id, &ctc_oid));
    if(SAI_BRIDGE_TYPE_CROSS_CONNECT == ctc_oid.sub_type)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_VPWS, ctc_oid.value));
    }
    else
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_VLAN, ctc_oid.value));
    }

    return status;
}

static sai_status_t
_ctc_sai_bridge_port_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_bridge_port_t* p_bridge_port = (ctc_sai_bridge_port_t*)data;

    if (p_bridge_port->logic_port)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_LOGIC_PORT, p_bridge_port->logic_port));
    }
    if (p_bridge_port->nh_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_bridge_port->nh_id));
    }

    return status;
}


#define ________BRIDGE_DUMP________

static sai_status_t
_ctc_sai_bridge_dump_bridge_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  bridge_oid = 0;
    ctc_object_id_t ctc_oid;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    uint8 learn_en = 0;
    uint32 max_learn_addr = 0;
    sai_object_key_t key;
    sai_attribute_t bridge_attr;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&key, 0, sizeof(sai_object_key_t));
    sal_memset(&bridge_attr, 0, sizeof(sai_attribute_t));

    bridge_oid = bucket_data->oid;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, bridge_oid, &ctc_oid));
    if ((0 != p_dmp_grep->key.key.object_id) && (bridge_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    key.key.object_id = bridge_oid;
    bridge_attr.id = SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES;
    ctc_sai_bridge_get_property(&key, &bridge_attr, 0);
    max_learn_addr = bridge_attr.value.u32;
    bridge_attr.id = SAI_BRIDGE_ATTR_LEARN_DISABLE;
    ctc_sai_bridge_get_property(&key, &bridge_attr, 0);
    learn_en = bridge_attr.value.booldata;
    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-11s %-8d %-14d\n", num_cnt, bridge_oid, ctc_oid.sub_type?"1D_bridge":"1Q_bridge",\
           learn_en, max_learn_addr);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_bridge_dump_bridge_port_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  brg_port_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_bridge_port_t* p_brg_port = NULL;

    brg_port_oid = bucket_data->oid;
    p_brg_port = (ctc_sai_bridge_port_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (brg_port_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    if (SAI_BRIDGE_PORT_TYPE_PORT == p_brg_port->port_type)
    {
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-9s 0x%04x %-4s %-10s %-5s %-7s %-18s\n", num_cnt, brg_port_oid, "port",\
            p_brg_port->gport, "-", "-", "-", "-", "-");
    }
    else if (SAI_BRIDGE_PORT_TYPE_SUB_PORT == p_brg_port->port_type)
    {
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-9s 0x%04x %-4d %-10d %-5d %-7s %-18s\n", num_cnt, brg_port_oid, "sub_port",\
            p_brg_port->gport, p_brg_port->vlan_id, p_brg_port->logic_port, p_brg_port->nh_id, "-", "-");
    }
    else if (SAI_BRIDGE_PORT_TYPE_1Q_ROUTER == p_brg_port->port_type)
    {
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-9s %-6s %-4d %-10s %-5s %-7d %-18s\n", num_cnt, brg_port_oid, "1q_router",\
            "-", p_brg_port->vlan_id, "-", "-", p_brg_port->l3if_id, "-");
    }
    else if (SAI_BRIDGE_PORT_TYPE_1D_ROUTER == p_brg_port->port_type)
    {
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-9s %-6s %-4s %-10s %-5s %-7d %-18s\n", num_cnt, brg_port_oid, "1d_router",\
            "-", "-", "-", "-", p_brg_port->l3if_id, "-");
    }
    else if (SAI_BRIDGE_PORT_TYPE_TUNNEL == p_brg_port->port_type)
    {
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-9s %-6s %-4s %-10d %-5s %-7s 0x%016"PRIx64"\n", num_cnt, brg_port_oid, "tunnel",\
            "-", "-", p_brg_port->logic_port, "-", "-", p_brg_port->tunnel_id);
    }

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_bridge_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Bridge MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_BRIDGE))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Bridge");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_bridge_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-11s %-8s %-14s\n", "No.", "Bridge_oid", "Bridge_type", "Learn_dis", "Max_learn_addr");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BRIDGE,
                                            (hash_traversal_fn)_ctc_sai_bridge_dump_bridge_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_BRIDGE_PORT))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Bridge port");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_bridge_port_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-9s %-6s %-4s %-10s %-5s %-7s %-18s\n", "No.", "Brg_port_oid", "Type", "Gport", "Vlan", "Logic_port", "Nhid", "L3if_id", "Tunnel_id");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BRIDGE_PORT,
                                            (hash_traversal_fn)_ctc_sai_bridge_dump_bridge_port_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________BRIDGE_API________

sai_status_t
ctc_sai_bridge_get_bridge_port_oid(uint8 lchip, uint32 gport, uint8 is_logic, sai_object_id_t* bridge_port_id)
{
    ctc_object_id_t ctc_oid = {0};

    CTC_SAI_LOG_ENTER(SAI_API_BRIDGE);

    ctc_oid.lchip = lchip;
    ctc_oid.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
    ctc_oid.value2 = 0;
    ctc_oid.value = gport;
    if (is_logic)
    {
        ctc_oid.sub_type = SAI_BRIDGE_PORT_TYPE_SUB_PORT;
    }
    else
    {
        ctc_oid.sub_type = SAI_BRIDGE_PORT_TYPE_PORT;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, &ctc_oid, bridge_port_id));

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_bridge_db_init(uint8 lchip)
{
    uint8 gchip_id = 0;
    uint16 index = 0;
    ctc_global_panel_ports_t local_panel_ports;
    sai_object_id_t def_bridge_id = 0;
    sai_object_id_t bridge_port_id = 0;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_BRIDGE;
    wb_info.data_len = sizeof(ctc_sai_bridge_port_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_bridge_port_wb_reload_cb;
    CTC_SAI_ERROR_RETURN(ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_BRIDGE_PORT, (void*)(&wb_info)));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_BRIDGE;
    wb_info.data_len = 0;
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_bridge_wb_reload_cb;
    CTC_SAI_ERROR_RETURN(ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_BRIDGE, (void*)(&wb_info)));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_NOT_EXECUTED;
    }
    def_bridge_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_1Q, 0, p_switch_master->default_bridge_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_add_object_property(lchip, def_bridge_id, NULL));

    sal_memset(&local_panel_ports, 0, sizeof(local_panel_ports));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip_id));
    for (index=0;index<local_panel_ports.count; index++)
    {
        status = _ctc_sai_bridge_port_alloc(&p_bridge_port);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Failed to allocate bridge port entry\n");
            return SAI_STATUS_NO_MEMORY;
        }
        else
        {
            p_bridge_port->bridge_id = p_switch_master->default_bridge_id;
        }
        p_bridge_port->limit_num = 0xFFFFFFFF;
        p_bridge_port->limit_action = CTC_MACLIMIT_ACTION_DISCARD;
        p_bridge_port->admin_state = true;
        p_bridge_port->gport = CTC_MAP_LPORT_TO_GPORT(gchip_id, local_panel_ports.lport[index]);
        bridge_port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, SAI_BRIDGE_PORT_TYPE_PORT, 0, p_bridge_port->gport);
        CTC_SAI_ERROR_RETURN(ctc_sai_db_add_object_property(lchip, bridge_port_id, p_bridge_port));
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_bridge_api_init()
{
    ctc_sai_register_module_api(SAI_API_BRIDGE, (void*)&g_ctc_sai_bridge_api);

    return SAI_STATUS_SUCCESS;
}

