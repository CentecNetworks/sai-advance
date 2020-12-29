#include "ctc_sai_fdb.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_neighbor.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_next_hop.h"

sai_status_t  _ctc_sai_fdb_mapping_fdb_query(  sai_object_key_t      *key,
                                             ctc_l2_fdb_query_t* Query)
{
    uint16     fid = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    ctc_sai_oid_get_lchip(key->key.fdb_entry.switch_id, &lchip);
    sal_memcpy(Query->mac, key->key.fdb_entry.mac_address, sizeof(Query->mac));
    CTC_SAI_ERROR_RETURN(ctc_sai_bridge_get_fid(key->key.fdb_entry.bv_id, &fid));

    Query->fid = fid;
    Query->query_type = CTC_L2_FDB_ENTRY_OP_BY_MAC_VLAN;
    Query->query_flag = CTC_L2_FDB_ENTRY_ALL;
    return SAI_STATUS_SUCCESS;

}

sai_status_t _ctc_sai_fdb_mapping_ctc_action(uint32*flag, const  sai_attribute_t *attr)
{
    switch(attr->value.s32)
    {
    case SAI_PACKET_ACTION_FORWARD:
        CTC_UNSET_FLAG(*flag, CTC_L2_FLAG_DISCARD);
        break;
    case SAI_PACKET_ACTION_DROP:
        CTC_SET_FLAG( *flag, CTC_L2_FLAG_DISCARD);
        break;
    case SAI_PACKET_ACTION_COPY:
        CTC_SET_FLAG(*flag, CTC_L2_FLAG_COPY_TO_CPU);
        break;
    case SAI_PACKET_ACTION_COPY_CANCEL:
        CTC_UNSET_FLAG(*flag, CTC_L2_FLAG_COPY_TO_CPU);
        break;
    case SAI_PACKET_ACTION_TRAP :
        CTC_SET_FLAG( *flag, CTC_L2_FLAG_DISCARD);
        CTC_SET_FLAG(*flag, CTC_L2_FLAG_COPY_TO_CPU);
        break;
    case SAI_PACKET_ACTION_LOG:
        CTC_UNSET_FLAG( *flag, CTC_L2_FLAG_DISCARD);
        CTC_SET_FLAG( *flag, CTC_L2_FLAG_COPY_TO_CPU);
        break;
    case SAI_PACKET_ACTION_DENY:
        CTC_UNSET_FLAG(*flag , CTC_L2_FLAG_COPY_TO_CPU);
        CTC_SET_FLAG(*flag, CTC_L2_FLAG_DISCARD);
        break;
    case  SAI_PACKET_ACTION_TRANSIT:
        CTC_UNSET_FLAG(*flag,  CTC_L2_FLAG_DISCARD);
        CTC_UNSET_FLAG(*flag, CTC_L2_FLAG_COPY_TO_CPU);
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "invalid action\n");
        return SAI_STATUS_INVALID_ATTR_VALUE_0 + attr->id;;

    }
    return SAI_STATUS_SUCCESS;

}



static sai_status_t
_ctc_sai_fdb_mapping_l2_addr(const sai_fdb_entry_t* fdb_entry,
                             uint32_t      attr_count,
                             const sai_attribute_t *attr_list,
                             ctc_l2_addr_t *p_l2_addr, uint32* nh_id)
{

    sai_status_t       status = SAI_STATUS_SUCCESS;
    sai_status_t       endport_status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    const sai_attribute_value_t *attr_value_endport;
    uint32                   attr_index_endport;
    uint32                   attr_index;
    uint8 lchip = 0;
    ctc_sai_bridge_port_t *port;
    uint32 action = SAI_PACKET_ACTION_FORWARD;

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    
    /*mapping mac*/
    sal_memcpy(&p_l2_addr->mac, &fdb_entry->mac_address, sizeof(p_l2_addr->mac));
    
    ctc_sai_oid_get_lchip(fdb_entry->switch_id, &lchip);

    /*mapping fid*/
    CTC_SAI_ERROR_RETURN(ctc_sai_bridge_get_fid(fdb_entry->bv_id, &p_l2_addr->fid));
    
    if (attr_count == 0 || !attr_list)
    { /*delete /querty*/
        return SAI_STATUS_SUCCESS;
    }


    /*static or dynamic*/
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_FDB_ENTRY_ATTR_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if (attr_value->s32 == SAI_FDB_ENTRY_TYPE_STATIC)
        {
            CTC_SET_FLAG(p_l2_addr->flag, CTC_L2_FLAG_IS_STATIC);
        }
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "mandatory attribute missing\n");
        return  SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_FDB_ENTRY_ATTR_META_DATA, &attr_value, &attr_index);
    if(status == SAI_STATUS_SUCCESS )
    {
        p_l2_addr->cid = CTC_SAI_META_DATA_SAI_TO_CTC(attr_value->u32);
    }

    /*mapping other property*/
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_FDB_ENTRY_ATTR_PACKET_ACTION, &attr_value, &attr_index);
    /*if error,the default action is forword*/
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_fdb_mapping_ctc_action(&p_l2_addr->flag, &attr_list[attr_index]));
        action = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, &attr_value, &attr_index);
    endport_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_FDB_ENTRY_ATTR_ENDPOINT_IP, &attr_value_endport, &attr_index_endport);    
    if (CTC_SAI_ERROR(status) || SAI_NULL_OBJECT_ID == attr_value->oid )
    {
        if ( SAI_PACKET_ACTION_FORWARD == action || SAI_PACKET_ACTION_LOG == action || SAI_PACKET_ACTION_TRANSIT == action)
        {
            CTC_SAI_LOG_ERROR(SAI_API_FDB, "must have bridge port \n");
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
    }
    else
    {
        /*no endport ip information*/
        port = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == port)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }
        /*TODO:IS SUBPORT */

        p_l2_addr->gport = port->gport;
        if(port->logic_port)
        {
            p_l2_addr->gport = port->logic_port;

            if ((SAI_BRIDGE_PORT_TYPE_TUNNEL == port->port_type) && !CTC_SAI_ERROR(endport_status))
            {
                uint32 tunnel_nh_id = 0;
                CTC_SAI_ERROR_RETURN(ctc_sai_next_hop_get_tunnel_nh(port->tunnel_id, &attr_value_endport->ipaddr, &tunnel_nh_id));
                if (port->nh_id != tunnel_nh_id)
                {
                    port->nh_id = tunnel_nh_id;
                    if (port->admin_state)
                    {
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_set_nhid_by_logic_port(lchip, port->logic_port, port->nh_id));
                    }
                }    
            }
            if(nh_id)
            {
                *nh_id = port->nh_id;
            }
        }
        else
        {
            /* use for normal fdb action SAI_PACKET_ACTION_DROP, keep port info 
             * fdb with nexthop, do not need
             */
            if(CTC_FLAG_ISSET(p_l2_addr->flag, CTC_L2_FLAG_DISCARD))
            {
                CTC_SET_FLAG(p_l2_addr->flag, CTC_L2_FLAG_ASSIGN_OUTPUT_PORT);
                p_l2_addr->assign_port = port->gport;
            }
        }
    }

    return SAI_STATUS_SUCCESS;

}



sai_status_t  ctc_sai_fdb_get_fdb_info(  sai_object_key_t      *key,   sai_attribute_t *attr, uint32 attr_idx)
{
    ctc_l2_fdb_query_rst_t query_rst;
    ctc_l2_fdb_query_t Query;
    uint8 lchip = 0;
    ctc_l2_addr_t fdb_info;
    sai_object_id_t bridge_port_oid = SAI_NULL_OBJECT_ID;

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    ctc_sai_oid_get_lchip(key->key.fdb_entry.switch_id, &lchip);
    sal_memset(&query_rst, 0, sizeof(ctc_l2_fdb_query_rst_t));
    sal_memset(&Query, 0, sizeof(ctc_l2_fdb_query_t));
    CTC_SAI_ERROR_RETURN(_ctc_sai_fdb_mapping_fdb_query(key, &Query ));
    sal_memset(&fdb_info, 0, sizeof(fdb_info));
    query_rst.buffer_len = sizeof(ctc_l2_addr_t);
    query_rst.buffer = &fdb_info;

    CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_get_fdb_entry(lchip, &Query, &query_rst));
    if (0 == Query.count)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
    case SAI_FDB_ENTRY_ATTR_TYPE:
        if (CTC_FLAG_ISSET(query_rst.buffer->flag, CTC_L2_FLAG_IS_STATIC))
        {
            attr->value.s32 = SAI_FDB_ENTRY_TYPE_STATIC;
        }
        else
        {
            attr->value.s32 = SAI_FDB_ENTRY_TYPE_DYNAMIC;
        }
        break;

    case SAI_FDB_ENTRY_ATTR_PACKET_ACTION:
        if (CTC_FLAG_ISSET(query_rst.buffer->flag, CTC_L2_FLAG_DISCARD)&& CTC_FLAG_ISSET(query_rst.buffer->flag, CTC_L2_FLAG_COPY_TO_CPU))
        {
            attr->value.s32 = SAI_PACKET_ACTION_TRAP;
        }
        else if(CTC_FLAG_ISSET(query_rst.buffer->flag, CTC_L2_FLAG_COPY_TO_CPU))
        {
            attr->value.s32 = SAI_PACKET_ACTION_LOG;
        }
        else if(CTC_FLAG_ISSET(query_rst.buffer->flag, CTC_L2_FLAG_DISCARD))
        {
            attr->value.s32 = SAI_PACKET_ACTION_DENY;
        }
        else
        {
            attr->value.s32 = SAI_PACKET_ACTION_TRANSIT;
        }
        break;
    case SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
        if (TRUE == query_rst.buffer->is_logic_port)
        {
            bridge_port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, SAI_BRIDGE_PORT_TYPE_SUB_PORT, 0, query_rst.buffer->gport);
            if (ctc_sai_db_get_object_property(lchip, bridge_port_oid))
            {
                attr->value.oid = bridge_port_oid;
                break;
            }
            bridge_port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, SAI_BRIDGE_PORT_TYPE_TUNNEL, 0, query_rst.buffer->gport);
            if (ctc_sai_db_get_object_property(lchip, bridge_port_oid))
            {
                attr->value.oid = bridge_port_oid;
                break;
            }
            bridge_port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, SAI_BRIDGE_PORT_TYPE_FRR, 0, query_rst.buffer->gport);
            if (ctc_sai_db_get_object_property(lchip, bridge_port_oid))
            {
                attr->value.oid = bridge_port_oid;
                break;
            }
            bridge_port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, SAI_BRIDGE_PORT_TYPE_DOUBLE_VLAN_SUB_PORT, 0, query_rst.buffer->gport);
            if (ctc_sai_db_get_object_property(lchip, bridge_port_oid))
            {
                attr->value.oid = bridge_port_oid;
                break;
            }
        }
        else
        {
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, SAI_BRIDGE_PORT_TYPE_PORT, 0, query_rst.buffer->gport);
        }
        break;
    case SAI_FDB_ENTRY_ATTR_META_DATA:
        attr->value.u32 = CTC_SAI_META_DATA_CTC_TO_SAI(query_rst.buffer->cid);
        break;
    case SAI_FDB_ENTRY_ATTR_USER_TRAP_ID:
         return SAI_STATUS_ATTR_NOT_SUPPORTED_0;     
    case SAI_FDB_ENTRY_ATTR_COUNTER_ID:
         return SAI_STATUS_ATTR_NOT_SUPPORTED_0;  
    default:
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "fdb attribute not implement\n");
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_fdb_set_fdb_info(  sai_object_key_t      *key, const  sai_attribute_t *attr)
{
    ctc_l2_fdb_query_rst_t query_rst;
    ctc_l2_fdb_query_t Query;
    ctc_object_id_t ctc_object_id ;
    ctc_l2_addr_t l2_addr;
    sai_fdb_entry_type_t type = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_l2_addr_t fdb_info;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    uint32 nh_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    ctc_sai_oid_get_lchip(key->key.fdb_entry.switch_id, &lchip);
    sal_memset(&query_rst, 0, sizeof(ctc_l2_fdb_query_rst_t));
    sal_memset(&Query, 0, sizeof(ctc_l2_fdb_query_t));
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&l2_addr, 0, sizeof(ctc_l2_addr_t));
    sal_memset(&fdb_info, 0 , sizeof(ctc_l2_addr_t));
    query_rst.buffer_len = sizeof(ctc_l2_addr_t);
    query_rst.buffer = &fdb_info;
    
    CTC_SAI_ERROR_RETURN(_ctc_sai_fdb_mapping_fdb_query(key, &Query ));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_get_fdb_entry(lchip, &Query, &query_rst), status, out);

    if (0 == Query.count)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    
    switch(attr->id)
    {
    case SAI_FDB_ENTRY_ATTR_TYPE:
        if (SAI_FDB_ENTRY_TYPE_DYNAMIC == attr->value.s32
            && (CTC_FLAG_ISSET(query_rst.buffer->flag, CTC_L2_FLAG_COPY_TO_CPU) || CTC_FLAG_ISSET(query_rst.buffer->flag, CTC_L2_FLAG_DISCARD)) )
        {
            CTC_SAI_LOG_ERROR(SAI_API_FDB, "Failed to update FDB Entry Type - Dynamic entries can only have Forward action\n");
            status =  SAI_STATUS_INVALID_ATTR_VALUE_0;
            goto out;
        }

        if (CTC_FLAG_ISSET(query_rst.buffer->flag, CTC_L2_FLAG_IS_STATIC) )
        {
            type = SAI_FDB_ENTRY_TYPE_STATIC;
        }
        else
        {
            type =  SAI_FDB_ENTRY_TYPE_DYNAMIC;
        }
        if (type == attr->value.s32)
        {
            status =  SAI_STATUS_NOT_EXECUTED;
            goto out;
        }

        sal_memcpy(&l2_addr, query_rst.buffer, sizeof(ctc_l2_addr_t));
        if (SAI_FDB_ENTRY_TYPE_STATIC == attr->value.s32)
        {
            CTC_SET_FLAG(l2_addr.flag, CTC_L2_FLAG_IS_STATIC);
        }
        else
        {
            CTC_UNSET_FLAG(l2_addr.flag, CTC_L2_FLAG_IS_STATIC);
        }
        break;
    case SAI_FDB_ENTRY_ATTR_PACKET_ACTION:
        sal_memcpy(&l2_addr, query_rst.buffer, sizeof(ctc_l2_addr_t));
        CTC_SAI_ERROR_GOTO(_ctc_sai_fdb_mapping_ctc_action(&l2_addr.flag, attr), status, out);

        /* use for normal fdb action SAI_PACKET_ACTION_DROP, keep port info 
         * fdb with nexthop, do not need
         */
        if(!l2_addr.is_logic_port && CTC_FLAG_ISSET(l2_addr.flag, CTC_L2_FLAG_DISCARD))
        {
            CTC_SET_FLAG(l2_addr.flag, CTC_L2_FLAG_ASSIGN_OUTPUT_PORT);
            l2_addr.assign_port = l2_addr.gport;
        }
        break;

    case SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
        
        sal_memcpy(&l2_addr, query_rst.buffer, sizeof(ctc_l2_addr_t));

        p_bridge_port = ctc_sai_db_get_object_property(lchip, attr->value.oid);
        if (NULL == p_bridge_port)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }   
        
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, attr->value.oid, &ctc_object_id);
    
        if ((SAI_BRIDGE_PORT_TYPE_SUB_PORT == ctc_object_id.sub_type) || (SAI_BRIDGE_PORT_TYPE_TUNNEL == ctc_object_id.sub_type) 
            || (SAI_BRIDGE_PORT_TYPE_FRR == ctc_object_id.sub_type) || (SAI_BRIDGE_PORT_TYPE_DOUBLE_VLAN_SUB_PORT == ctc_object_id.sub_type))
        {
            l2_addr.is_logic_port = TRUE;
            nh_id = p_bridge_port->nh_id;
        }
        else
        {
            l2_addr.is_logic_port = FALSE;
        }
        l2_addr.gport = ctc_object_id.value;
        break;
    case SAI_FDB_ENTRY_ATTR_META_DATA:
        sal_memcpy(&l2_addr, query_rst.buffer, sizeof(ctc_l2_addr_t));
        l2_addr.cid = CTC_SAI_META_DATA_SAI_TO_CTC(attr->value.u32);
        break;
    case SAI_FDB_ENTRY_ATTR_USER_TRAP_ID:
         return SAI_STATUS_ATTR_NOT_SUPPORTED_0;     
    case SAI_FDB_ENTRY_ATTR_COUNTER_ID:
         return SAI_STATUS_ATTR_NOT_SUPPORTED_0;        
    default:
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "fdb attribute not implement\n");
        status =  SAI_STATUS_NOT_IMPLEMENTED;
        goto out;

    }

    //update non bridge port id attribute
    if((attr->id != SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID) && l2_addr.is_logic_port)
    {
        ctcs_l2_get_nhid_by_logic_port(lchip, l2_addr.gport, &nh_id);
    }

    if(l2_addr.is_logic_port)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_add_fdb_with_nexthop(lchip, &l2_addr, nh_id), status, out);
    }
    else
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_add_fdb(lchip, &l2_addr), status, out);
    }
   
    ctc_sai_neighbor_update_arp(lchip, &(key->key.fdb_entry), 0, 0);

out:
    return status;
}

sai_status_t  ctc_sai_fdb_get_fdb_endpoint_ip(  sai_object_key_t      *key,   sai_attribute_t *attr, uint32 attr_idx)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}

static sai_status_t ctc_sai_fdb_set_fdb_endpoint_ip(  sai_object_key_t      *key, const  sai_attribute_t *attr)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}


static  ctc_sai_attr_fn_entry_t fdb_attr_fn_entries[] = {
    { SAI_FDB_ENTRY_ATTR_TYPE,
      ctc_sai_fdb_get_fdb_info,
      ctc_sai_fdb_set_fdb_info},
    { SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID,
      ctc_sai_fdb_get_fdb_info,
      ctc_sai_fdb_set_fdb_info},
    { SAI_FDB_ENTRY_ATTR_PACKET_ACTION,
      ctc_sai_fdb_get_fdb_info,
      ctc_sai_fdb_set_fdb_info},
    { SAI_FDB_ENTRY_ATTR_ENDPOINT_IP,
      ctc_sai_fdb_get_fdb_endpoint_ip,
      ctc_sai_fdb_set_fdb_endpoint_ip},
    { SAI_FDB_ENTRY_ATTR_META_DATA,
      ctc_sai_fdb_get_fdb_info,
      ctc_sai_fdb_set_fdb_info},
    { SAI_FDB_ENTRY_ATTR_USER_TRAP_ID,
      ctc_sai_fdb_get_fdb_info,
      ctc_sai_fdb_set_fdb_info},
    { SAI_FDB_ENTRY_ATTR_COUNTER_ID,
      ctc_sai_fdb_get_fdb_info,
      ctc_sai_fdb_set_fdb_info},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL}
};
#define ________INTERNAL_API________
sai_status_t
ctc_sai_fdb_flush_fdb( sai_object_id_t        switch_id,
                                                  uint32_t               attr_count,
                                                  const sai_attribute_t *attr_list)
{
    const sai_attribute_value_t *attr_value = NULL;
    uint32 attr_index = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_l2_flush_fdb_t  Flush;
    ctc_sai_bridge_port_t *bridge_port = NULL;
    uint8 port_found_flag = 0;
    uint8 bv_id_found_flag = 0;
    uint8 lchip = 0;
    sai_fdb_entry_t fdb_entry;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_attribute_t attr_event[2];
    ctc_learning_action_info_t learning_action;

    sal_memset(&learning_action, 0, sizeof(ctc_learning_action_info_t));
    sal_memset(attr_event, 0, sizeof(sai_attribute_t)*2);

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    sal_memset(&fdb_entry, 0, sizeof(fdb_entry));
    fdb_entry.switch_id = switch_id;
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch global info, invalid lchip %d!\n", lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    attr_event[0].id = SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID;
    attr_event[0].value.oid = 0;
    attr_event[1].id = SAI_FDB_ENTRY_ATTR_TYPE;
    attr_event[1].value.s32 = SAI_FDB_ENTRY_TYPE_DYNAMIC;

    sal_memset(&Flush, 0, sizeof(Flush));
    Flush.flush_type = CTC_L2_FDB_ENTRY_OP_ALL;
    Flush.flush_flag = CTC_L2_FDB_ENTRY_DYNAMIC;
    status =  ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID, &attr_value, &attr_index);
    if (!CTC_SAI_ERROR(status))
    {
        if(attr_value->oid != SAI_NULL_OBJECT_ID)
        {
            bridge_port = ctc_sai_db_get_object_property(lchip, attr_value->oid);
            if (NULL == bridge_port)
            {
                status =  SAI_STATUS_INVALID_OBJECT_ID;
                goto out;
            }
            Flush.gport = (SAI_BRIDGE_TYPE_1D == bridge_port->bridge_type) ? bridge_port->logic_port: bridge_port->gport;
            Flush.use_logic_port = (SAI_BRIDGE_TYPE_1D == bridge_port->bridge_type) ? 1:0;
            port_found_flag = TRUE;
            attr_event[0].id = SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID;
            attr_event[0].value.oid = attr_value->oid;
        }
    }

    status =  ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_FDB_FLUSH_ATTR_BV_ID, &attr_value, &attr_index);
    if (!CTC_SAI_ERROR(status))
    {
        if(attr_value->oid != SAI_NULL_OBJECT_ID)
        {
            bv_id_found_flag = TRUE;
            fdb_entry.bv_id = attr_value->oid;
            CTC_SAI_ERROR_GOTO(ctc_sai_bridge_get_fid(attr_value->oid, &Flush.fid), status, out);
        }
    }

    status =  ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_FDB_FLUSH_ATTR_ENTRY_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        switch (attr_value->u32)
        {
        case SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC:
            Flush.flush_flag = CTC_L2_FDB_ENTRY_DYNAMIC;
            break;
        case SAI_FDB_FLUSH_ENTRY_TYPE_STATIC:
            Flush.flush_flag = CTC_L2_FDB_ENTRY_STATIC;
            break;
        case SAI_FDB_FLUSH_ENTRY_TYPE_ALL:
            Flush.flush_flag = CTC_L2_FDB_ENTRY_ALL;
            break;
        default:
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
    }

    if (bv_id_found_flag && port_found_flag)
    {
        Flush.flush_type = CTC_L2_FDB_ENTRY_OP_BY_PORT_VLAN;
    }
    else if(bv_id_found_flag)
    {
        Flush.flush_type = CTC_L2_FDB_ENTRY_OP_BY_VID;
    }
    else if(port_found_flag)
    {
        Flush.flush_type = CTC_L2_FDB_ENTRY_OP_BY_PORT;
    }

    learning_action.action = CTC_LEARNING_ACTION_MAC_TABLE_FULL;
    learning_action.value = 1;
    ctcs_set_learning_action(lchip, &learning_action);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_flush_fdb(lchip, &Flush), status, out);
    ctc_sai_neighbor_update_arp(lchip, &fdb_entry, 0, 1);
    if (p_switch_master->fdb_event_cb)
    {
        sai_fdb_event_notification_data_t fdb_events;
        sal_memset(&fdb_events, 0, sizeof(sai_fdb_event_notification_data_t));
        fdb_events.event_type = SAI_FDB_EVENT_FLUSHED;
        sal_memcpy(&fdb_events.fdb_entry, &fdb_entry, sizeof(sai_fdb_entry_t));
        fdb_events.attr_count = 2;
        fdb_events.attr = attr_event;
        p_switch_master->fdb_event_cb(1, &fdb_events);
    }
    learning_action.value = 0;
    ctcs_set_learning_action(lchip, &learning_action);

out:
    return status;
}

uint32
ctc_sai_fdb_get_fdb_count(uint8 lchip)
{
    ctc_l2_fdb_query_t fdb_query;
    sal_memset(&fdb_query, 0, sizeof(ctc_l2_fdb_query_t));
    fdb_query.query_type = CTC_L2_FDB_ENTRY_OP_ALL;
    fdb_query.query_flag = CTC_L2_FDB_ENTRY_ALL;
    ctcs_l2_get_fdb_count(lchip, &fdb_query);
    return fdb_query.count;
}

sai_status_t
ctc_sai_fdb_dump_fdb_entrys(uint8 lchip, uint32_t object_count, sai_object_key_t *object_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 index = 0;
    uint32 actual_cnt = 0;
    ctc_l2_fdb_query_t query;
    ctc_l2_fdb_query_rst_t query_rst;
    sai_object_id_t switch_id;
    sai_object_id_t bv_id;
    uint8 gchip = 0;
    
    if(NULL == object_list)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    if (object_count < ctc_sai_fdb_get_fdb_count(lchip))
    {
        return SAI_STATUS_BUFFER_OVERFLOW;
    }

    sal_memset(&query, 0, sizeof(ctc_l2_fdb_query_t));
    sal_memset(&query_rst, 0, sizeof(ctc_l2_fdb_query_rst_t));
    query.query_type = CTC_L2_FDB_ENTRY_OP_ALL;
    query.query_flag = CTC_L2_FDB_ENTRY_ALL;

    query_rst.buffer_len = sizeof(ctc_l2_addr_t) * 100;
    query_rst.buffer = (ctc_l2_addr_t*)mem_malloc(MEM_FDB_MODULE, query_rst.buffer_len);
    if (NULL == query_rst.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(query_rst.buffer, 0, query_rst.buffer_len);
    ctcs_get_gchip_id(lchip, &gchip);
    switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
    do
    {
        query_rst.start_index = query_rst.next_query_index;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_get_fdb_entry(lchip, &query, &query_rst), status, done);
        for (index = 0; index < query.count; index++)
        {
            object_list[actual_cnt].key.fdb_entry.switch_id = switch_id;
            sal_memcpy(&object_list[actual_cnt].key.fdb_entry.mac_address, query_rst.buffer[index].mac, sizeof(mac_addr_t));
            bv_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, query_rst.buffer[index].fid);
            if (NULL == ctc_sai_db_get_object_property(lchip, bv_id))/*bridge db no data*/
            {
                bv_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, 0, 0, query_rst.buffer[index].fid);
            }
            object_list[actual_cnt].key.fdb_entry.bv_id = bv_id;
            actual_cnt++;
            sal_memset(&query_rst.buffer[index], 0, sizeof(ctc_l2_addr_t));
        }
        sal_task_sleep(100);
    }
    while (query_rst.is_end == 0);
done:
    mem_free(query_rst.buffer);
    return status;
}


sai_status_t
ctc_sai_fdb_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 index = 0;
    ctc_l2_fdb_query_t query;
    ctc_l2_fdb_query_rst_t query_rst;
    sai_object_id_t bv_id;
    char mac_buf[20] ={0};
    uint32 num_cnt = 1;

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI FDB MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_FDB_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "FDB");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "No db now, just dump key and action.");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s  %-14s  %-18s  %-8s  %-13s\n", \
            "No.", "Mac_address", "Bv_id", "Dst_port", "Is_logic_port");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sal_memset(&query, 0, sizeof(ctc_l2_fdb_query_t));
        sal_memset(&query_rst, 0, sizeof(ctc_l2_fdb_query_rst_t));
        query.query_type = CTC_L2_FDB_ENTRY_OP_ALL;
        query.query_flag = CTC_L2_FDB_ENTRY_ALL;
        query_rst.buffer_len = sizeof(ctc_l2_addr_t) * 100;
        query_rst.buffer = (ctc_l2_addr_t*)mem_malloc(MEM_FDB_MODULE, query_rst.buffer_len);
        if (NULL == query_rst.buffer)
        {
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(query_rst.buffer, 0, query_rst.buffer_len);
        do
        {
            query_rst.start_index = query_rst.next_query_index;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_get_fdb_entry(lchip, &query, &query_rst), status, done);
            for (index = 0; index < query.count; index++)
            {
                ctc_sai_get_mac_str(query_rst.buffer[index].mac, mac_buf);

                bv_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, query_rst.buffer[index].fid);
                if (NULL == ctc_sai_db_get_object_property(lchip, bv_id))/*bridge db no data*/
                {
                    bv_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, 0, 0, query_rst.buffer[index].fid);
                }
                CTC_SAI_LOG_DUMP(p_file, "%-4d  %-14s  0x%016"PRIx64 "  %-8d  %-13d\n", num_cnt, mac_buf, bv_id, \
                query_rst.buffer[index].gport, query_rst.buffer[index].is_logic_port);
                sal_memset(&query_rst.buffer[index], 0, sizeof(ctc_l2_addr_t));
                num_cnt++;
            }
            
            sal_task_sleep(100);
        }
        while (query_rst.is_end == 0);
    }
    done:
    mem_free(query_rst.buffer);
    return status;
}

#define ________SAI_API________

/*
 * Routine Description:
 *    Remove all FDB entries by attribute set in sai_fdb_flush_attr
 *
 * Arguments:
 *    [in] attr_count - number of attributes
 *    [in] attr_list - array of attributes
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t ctc_sai_fdb_flush_fdb_entries( sai_object_id_t        switch_id,
                                                  uint32_t               attr_count,
                                                  const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    CTC_SAI_LOG_ENTER(SAI_API_FDB);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_fdb_flush_fdb(switch_id, attr_count, attr_list);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}
/*
 * Routine Description:
 *    Set fdb entry attribute value
 *
 * Arguments:
 *    [in] fdb_entry - fdb entry
 *    [in] attr - attribute
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t ctc_sai_fdb_set_fdb_entry_attribute(const  sai_fdb_entry_t* fdb_entry,
                                                   const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    sal_memset(&key, 0, sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    if (NULL == fdb_entry || NULL == attr)
    {
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "set fdb attr, invalid parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    sal_memcpy(&key.key.fdb_entry, fdb_entry, sizeof(*fdb_entry));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(fdb_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key,NULL,
                        SAI_OBJECT_TYPE_FDB_ENTRY,  fdb_attr_fn_entries,attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "Failed to set fdb entry :%d\n", status);
    }
    return status;
}




/*
 * Routine Description:
 *    Get fdb entry attribute value
 *
 * Arguments:
 *    [in] fdb_entry - fdb entry
 *    [in] attr_count - number of attributes
 *    [inout] attr_list - array of attributes
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t ctc_sai_fdb_get_fdb_entry_attribute( const sai_fdb_entry_t* fdb_entry,
                                                        uint32_t               attr_count,
                                                        sai_attribute_t    *attr_list)
{
    sai_object_key_t key ;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 loop = 0;
    uint8 lchip = 0;

    sal_memset(&key, 0, sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    if (NULL == fdb_entry || NULL == attr_list || 0 == attr_count)
    {
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "get fdb attr, invalid parameter:%d\n", status);
        return SAI_STATUS_INVALID_PARAMETER;
    }
    sal_memcpy(&key.key.fdb_entry, fdb_entry, sizeof(sai_fdb_entry_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(fdb_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_FDB_ENTRY, loop, fdb_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "Failed to get fdb entry attr status:%d,id:%u\n", status, attr_list[loop].id);
    }
    return status;
}



/*
 * Routine Description:
 *    Create FDB entry
 *
 * Arguments:
 *    [in] fdb_entry - fdb entry
 *    [in] attr_count - number of attributes
 *    [in] attr_list - array of attributes
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t ctc_sai_fdb_create_fdb_entry(  const sai_fdb_entry_t* fdb_entry,
                                                 uint32_t               attr_count,
                                                 const sai_attribute_t *attr_list)
{
    sai_status_t  status = SAI_STATUS_SUCCESS;
    ctc_l2_addr_t l2_addr;
    uint8 lchip = 0;
    uint32 nh_id = 0;

    if (!fdb_entry || !attr_list || (attr_count == 0))
    {
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "NULL fdb entry param\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(fdb_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    sal_memset(&l2_addr, 0 , sizeof(l2_addr));
    CTC_SAI_ERROR_GOTO(_ctc_sai_fdb_mapping_l2_addr(fdb_entry, attr_count, attr_list, &l2_addr, &nh_id), status, out);
    if (nh_id)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_add_fdb_with_nexthop(lchip, &l2_addr, nh_id) , status, out);
    }
    else
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_add_fdb(lchip, &l2_addr) , status, out);
    }
    ctc_sai_neighbor_update_arp(lchip, fdb_entry, 0, 0);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "Failed to create fdb entry:%d\n", status);
    }
    return status;
}



/*
 * Routine Description:
 *    Remove FDB entry
 *
 * Arguments:
 *    [in] fdb_entry - fdb entry
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t ctc_sai_fdb_remove_fdb_entry( const sai_fdb_entry_t* fdb_entry)
{

    sai_status_t  status = SAI_STATUS_SUCCESS;
    ctc_l2_addr_t l2_addr;
    uint8 lchip = 0;

    if (!fdb_entry )
    {
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "NULL fdb entry param\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(fdb_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    sal_memset(&l2_addr, 0 ,sizeof(l2_addr));
    CTC_SAI_ERROR_GOTO(_ctc_sai_fdb_mapping_l2_addr(fdb_entry, 0, NULL, &l2_addr, NULL), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_l2_remove_fdb(lchip, &l2_addr), status, out);
    ctc_sai_neighbor_update_arp(lchip, fdb_entry, 1, 0);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_FDB, "Failed to remove  fdb entry:%d\n", status);
    }
    return status;
}

 static sai_status_t
 ctc_sai_fdb_create_fdb_entries(
        _In_ uint32_t object_count,
        _In_ const sai_fdb_entry_t *fdb_entry,
        _In_ const uint32_t *attr_count,
        _In_ const sai_attribute_t **attr_list,
        _In_ sai_bulk_op_error_mode_t mode,
        _Out_ sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    CTC_SAI_PTR_VALID_CHECK(fdb_entry);
    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    for (i = 0; i < object_count; i++)
    {
       object_statuses[i] = SAI_STATUS_NOT_EXECUTED;
    }
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(fdb_entry[i].switch_id, &lchip));
        //CTC_SAI_DB_LOCK(lchip);
        p_switch_master = ctc_sai_get_switch_property(lchip);
        object_statuses[i] = ctc_sai_fdb_create_fdb_entry(&(fdb_entry[i]), attr_count[i], (attr_list[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            //CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_FAILURE;
        }
        else if (CTC_SAI_ERROR(object_statuses[i]))
        {
           status = SAI_STATUS_FAILURE;
        }
        //CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

static sai_status_t
ctc_sai_fdb_remove_fdb_entries(
        _In_ uint32_t object_count,
        _In_ const sai_fdb_entry_t *fdb_entry,
        _In_ sai_bulk_op_error_mode_t mode,
        _Out_ sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    CTC_SAI_PTR_VALID_CHECK(fdb_entry);
    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    for (i = 0; i < object_count; i++)
    {
       object_statuses[i] = SAI_STATUS_NOT_EXECUTED;
    }
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(fdb_entry[i].switch_id, &lchip));
        //CTC_SAI_DB_LOCK(lchip);
        p_switch_master = ctc_sai_get_switch_property(lchip);
        object_statuses[i] = ctc_sai_fdb_remove_fdb_entry(&(fdb_entry[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            //CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_FAILURE;
        }
        else if (CTC_SAI_ERROR(object_statuses[i]))
        {
           status = SAI_STATUS_FAILURE;
        }

        //CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

static sai_status_t
ctc_sai_fdb_set_fdb_entries_attribute(
        _In_ uint32_t object_count,
        _In_ const sai_fdb_entry_t *fdb_entry,
        _In_ const sai_attribute_t *attr_list,
        _In_ sai_bulk_op_error_mode_t mode,
        _Out_ sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i = 0;

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    for (i = 0; i < object_count; i++)
    {
       object_statuses[i] = SAI_STATUS_NOT_EXECUTED;
    }
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(fdb_entry[i].switch_id, &lchip));
        //CTC_SAI_DB_LOCK(lchip);
        object_statuses[i] = ctc_sai_fdb_set_fdb_entry_attribute(&(fdb_entry[i]), &(attr_list[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            //CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_FAILURE;
        }
        else if (CTC_SAI_ERROR(object_statuses[i]))
        {
           status = SAI_STATUS_FAILURE;
        }

        //CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

static sai_status_t
ctc_sai_fdb_get_fdb_entries_attribute(
        _In_ uint32_t object_count,
        _In_ const sai_fdb_entry_t *fdb_entry,
        _In_ const uint32_t *attr_count,
        _Inout_ sai_attribute_t **attr_list,
        _In_ sai_bulk_op_error_mode_t mode,
        _Out_ sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i = 0;

    CTC_SAI_LOG_ENTER(SAI_API_FDB);
    for (i = 0; i < object_count; i++)
    {
        object_statuses[i] = SAI_STATUS_NOT_EXECUTED;
    }
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(fdb_entry[i].switch_id, &lchip));
        //CTC_SAI_DB_LOCK(lchip);
        object_statuses[i] = ctc_sai_fdb_get_fdb_entry_attribute(&(fdb_entry[i]), attr_count[i], (attr_list[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            //CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_FAILURE;
        }
        else if (CTC_SAI_ERROR(object_statuses[i]))
        {
            status = SAI_STATUS_FAILURE;
        }

        //CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}


sai_fdb_api_t g_ctc_sai_fdb_api = {
    ctc_sai_fdb_create_fdb_entry,
    ctc_sai_fdb_remove_fdb_entry,
    ctc_sai_fdb_set_fdb_entry_attribute,
    ctc_sai_fdb_get_fdb_entry_attribute,
    ctc_sai_fdb_flush_fdb_entries,
    ctc_sai_fdb_create_fdb_entries,
    ctc_sai_fdb_remove_fdb_entries,
    ctc_sai_fdb_set_fdb_entries_attribute,
    ctc_sai_fdb_get_fdb_entries_attribute
};

sai_status_t
ctc_sai_fdb_api_init()
{
    ctc_sai_register_module_api(SAI_API_FDB, (void*)&g_ctc_sai_fdb_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_fdb_db_init(uint8 lchip)
{
    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);
    CTC_SAI_CTC_ERROR_RETURN(ctcs_aging_set_property(lchip, CTC_AGING_TBL_MAC, CTC_AGING_PROP_INTERVAL, 5*60));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_aging_set_property(lchip, CTC_AGING_TBL_MAC, CTC_AGING_PROP_AGING_SCAN_EN, 1));
    return SAI_STATUS_SUCCESS;
}
