#include "ctc_sai_lag.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_port.h"
#include "ctc_sai_acl.h"



sai_status_t
_ctc_sai_lag_process_notification_member_change(uint8 lchip, uint32 lag_port, uint32 mem_port, uint32 change)
{
    sai_object_id_t oid = 0;
    ctc_sai_lag_info_t* p_lag = NULL;
    uint8 index = 0;

    oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, lag_port);
    p_lag = ctc_sai_db_get_object_property(lchip,  oid);
    if (NULL == p_lag )
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag info wrong\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    for(index=0; index<CTC_SAI_LAG_MEM_CHANGE_TYPE_MAX; index++)
    {
        if (p_lag->cb[index])
        {
            (*p_lag->cb[index])(lchip, lag_port, mem_port, change);
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t _ctc_sai_lag_create_lag_member( sai_object_id_t     * lag_member_id,
                                                   sai_object_id_t        switch_id,
                                                   uint32_t               attr_count,
                                                   const sai_attribute_t *attr_list)
{
    const sai_attribute_value_t *lag_id = NULL, *port_id = NULL, *attr1 = NULL, *attr2 = NULL;
    uint32    lag_id_index, port_index, index;
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_status_t status_in = SAI_STATUS_SUCCESS;
    sai_status_t status_out = SAI_STATUS_SUCCESS;
    uint8 lchip;
    ctc_object_id_t ctc_lag_oid ;
    ctc_object_id_t ctc_port_oid ;
    ctc_sai_lag_info_t* db_lag;
    ctc_vlantag_ctl_t vlantag_ctl_restore;
    uint32 default_pcp_restore;
    uint16 default_vlan_restore;


    if (NULL == lag_member_id || 0 == attr_count || NULL == attr_list )
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, " lag member parameter invalid\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    ctc_sai_oid_get_lchip(switch_id, &lchip);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_MEMBER_ATTR_LAG_ID, &lag_id, &lag_id_index);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "mandatory attr miss\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_MEMBER_ATTR_PORT_ID, &port_id, &port_index);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "mandatory attr miss\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    db_lag = ctc_sai_db_get_object_property(lchip,  lag_id->oid);
    if (NULL == db_lag )
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag info wrong\n");
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }


    ctc_sai_get_ctc_object_id(SAI_LAG_MEMBER_ATTR_LAG_ID, lag_id->oid, &ctc_lag_oid);
    ctc_sai_get_ctc_object_id(SAI_LAG_MEMBER_ATTR_PORT_ID, port_id->oid, &ctc_port_oid);

    /* get egress mode */
    status_out = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE, &attr1, &index);

    /* get ingress mode */
    status_in = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE, &attr2, &index);

    if ( (status_out == SAI_STATUS_SUCCESS) && (attr1->booldata == true) )
    {
        status_out = SAI_STATUS_SUCCESS;
    }
    else
    {
        status_out = SAI_STATUS_FAILURE;
    }

    if ( (status_in == SAI_STATUS_SUCCESS) && (attr2->booldata == true) )
    {
        status_in = SAI_STATUS_SUCCESS;
    }
    else
    {
        status_in = SAI_STATUS_FAILURE;
    }

    if (SAI_STATUS_SUCCESS == status_out && SAI_STATUS_SUCCESS == status_in)
    {
        CTC_BMP_SET(db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));
        CTC_BMP_SET(db_lag->Ingress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));
    }
    else if (SAI_STATUS_SUCCESS == status_out)
    {
        CTC_BMP_SET(db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, ctc_port_oid.value, CTC_PORT_PROP_GPORT, ctc_lag_oid.value), status, out);
    }
    else if(SAI_STATUS_SUCCESS == status_in)
    {
        ctcs_linkagg_add_port(lchip, (uint8)ctc_lag_oid.value, ctc_port_oid.value);
        CTC_BMP_SET(db_lag->Ingress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, ctc_port_oid.value, CTC_PORT_PROP_GPORT, ctc_port_oid.value), status, out);
    }
    else
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_linkagg_add_port(lchip, (uint8)ctc_lag_oid.value, ctc_port_oid.value), status, out);
    }



    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_get_vlan_ctl(lchip, ctc_port_oid.value, &vlantag_ctl_restore), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_get_property(lchip, ctc_port_oid.value, CTC_PORT_PROP_DEFAULT_PCP, &default_pcp_restore), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_get_default_vlan(lchip, ctc_port_oid.value, &default_vlan_restore), status, out);

    CTC_BMP_SET(db_lag->member_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));

    if (TRUE == db_lag->drop_tagged && TRUE == db_lag->drop_untagged)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_vlan_ctl(lchip, ctc_port_oid.value, CTC_VLANCTL_DROP_ALL), status, error1);
    }
    else if (TRUE == db_lag->drop_tagged)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_vlan_ctl(lchip, ctc_port_oid.value, CTC_VLANCTL_DROP_ALL_TAGGED), status, error1);
    }
    else if (TRUE == db_lag->drop_untagged)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_vlan_ctl(lchip, ctc_port_oid.value, CTC_VLANCTL_DROP_ALL_UNTAGGED), status, error1);
    }
    else
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_vlan_ctl(lchip, ctc_port_oid.value, CTC_VLANCTL_ALLOW_ALL_PACKETS), status, error1);
    }

    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_default_vlan(lchip, ctc_port_oid.value, db_lag->vlan_id), status, error2);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, ctc_port_oid.value, CTC_PORT_PROP_DEFAULT_PCP, db_lag->vlan_priority), status, error3);
    
    *lag_member_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG_MEMBER, lchip, 0, (uint16)ctc_lag_oid.value, ctc_port_oid.value);

    if (db_lag->is_binding_rif)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_phy_if_en(lchip, ctc_port_oid.value, 1), status, error4);
    }
    if (db_lag->is_binding_sub_rif)
    {
        ctc_port_scl_property_t port_scl_property;
        sal_memset(&port_scl_property, 0, sizeof(ctc_port_scl_property_t));
        port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_PORT_SVLAN;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_scl_property(lchip, ctc_port_oid.value, &port_scl_property), status, error4);
    }

    _ctc_sai_lag_process_notification_member_change(lchip, ctc_lag_oid.value, ctc_port_oid.value, true);

    return SAI_STATUS_SUCCESS;
    
    error4:
    CTC_SAI_LOG_ERROR(SAI_API_LAG, "rollback to error4\n");
    ctcs_port_set_property(lchip, ctc_port_oid.value, CTC_PORT_PROP_DEFAULT_PCP, default_pcp_restore);
    error3:
    CTC_SAI_LOG_ERROR(SAI_API_LAG, "rollback to error3\n");
    ctcs_port_set_default_vlan(lchip, ctc_port_oid.value, default_vlan_restore);
    error2:
    CTC_SAI_LOG_ERROR(SAI_API_LAG, "rollback to error2\n");
    ctcs_port_set_vlan_ctl(lchip, ctc_port_oid.value, vlantag_ctl_restore);

    error1:
    CTC_SAI_LOG_ERROR(SAI_API_LAG, "rollback to error1\n");
    CTC_BMP_UNSET(db_lag->member_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));
    if (SAI_STATUS_SUCCESS == status_out && SAI_STATUS_SUCCESS == status_in)
    {
        CTC_BMP_UNSET(db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));
        CTC_BMP_UNSET(db_lag->Ingress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));
    }
    else if (SAI_STATUS_SUCCESS == status_out)
    {
        CTC_BMP_UNSET(db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));
        ctcs_port_set_property(lchip, ctc_port_oid.value, CTC_PORT_PROP_GPORT, ctc_port_oid.value);
    }
    else if(SAI_STATUS_SUCCESS == status_in)
    {
        ctcs_linkagg_remove_port(lchip, (uint8)ctc_lag_oid.value, ctc_port_oid.value);
        CTC_BMP_UNSET(db_lag->Ingress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_port_oid.value));
    }
    else
    {
        ctcs_linkagg_remove_port(lchip, (uint8)ctc_lag_oid.value, ctc_port_oid.value);
    }

    out:
    return status;
}


static sai_status_t _ctc_sai_lag_remove_lag_member( sai_object_id_t lag_member_id)
{
    uint16 lag_id;
    uint32  gport;
    uint8 lchip;
    sai_object_id_t lag_oid;
    ctc_sai_lag_info_t*  p_db_lag = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(lag_member_id, &lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lag_member_id(lag_member_id, &lag_id, &gport));

    lag_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, (uint32)lag_id);
    p_db_lag = ctc_sai_db_get_object_property(lchip,  lag_oid);
    if (NULL == p_db_lag  )
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag info wrong\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    if (p_db_lag->is_binding_rif)
    {
        ctcs_port_set_phy_if_en(lchip, gport, 0);
    }
    if (p_db_lag->is_binding_sub_rif)
    {
        ctc_port_scl_property_t port_scl_property;
        sal_memset(&port_scl_property, 0, sizeof(ctc_port_scl_property_t));
        port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_DISABLE;
        ctcs_port_set_scl_property(lchip, gport, &port_scl_property);
    }
    CTC_BMP_UNSET(p_db_lag->member_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport));
    CTC_BMP_UNSET(p_db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport));
    CTC_BMP_UNSET(p_db_lag->Ingress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport));

    CTC_SAI_CTC_ERROR_RETURN( ctcs_linkagg_remove_port(lchip, lag_id, gport));
    _ctc_sai_lag_process_notification_member_change(lchip, lag_id, gport, false);

    return status;
}


sai_status_t
ctc_sai_lag_get_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    uint32 port_num = 0;
    sai_object_id_t*lag_members;
    uint32 bit_cnt = 0;
    sai_status_t status = 0;
    ctc_sai_lag_info_t *p_db_lag;
    sai_object_id_t *p_bounded_oid = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_LAG, key->key.object_id, &ctc_object_id);

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);

    p_db_lag = ctc_sai_db_get_object_property(ctc_object_id.lchip, key->key.object_id);
    if (NULL == p_db_lag)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    switch(attr->id)
    {
    case SAI_LAG_ATTR_PORT_LIST:
        lag_members =  mem_malloc(MEM_VLAN_MODULE, sizeof(sai_object_id_t)*sizeof(p_db_lag->member_ports_bits)*8);
        if (NULL == lag_members)
        {
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(lag_members, 0, sizeof(sai_object_id_t)*sizeof(p_db_lag->member_ports_bits)*8);
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {                
                lag_members[port_num] =  ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG_MEMBER, ctc_object_id.lchip, 0, (uint16)ctc_object_id.value, bit_cnt);
                port_num++;
            }
        }
        status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), lag_members, port_num, &attr->value.objlist);
        mem_free(lag_members);
        break;
    case  SAI_LAG_ATTR_PORT_VLAN_ID:
        attr->value.u16 = p_db_lag->vlan_id;
        break;

    case SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY:
        attr->value.u8 = p_db_lag->vlan_priority;
        break;
    case SAI_LAG_ATTR_DROP_UNTAGGED:
        attr->value.booldata = p_db_lag->drop_untagged;
        break;

    case SAI_LAG_ATTR_DROP_TAGGED:
        attr->value.booldata = p_db_lag->drop_tagged;
        break;

    case SAI_LAG_ATTR_INGRESS_ACL:
        p_bounded_oid = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND, (void*)(&key->key.object_id));
        attr->value.oid = *p_bounded_oid;
        break;
    case SAI_LAG_ATTR_MODE:
        attr->value.s32 = p_db_lag->lag_mode;
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "lag attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED + attr_idx;

    }

    return  status;
}


sai_status_t
ctc_sai_lag_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{
    uint32 bit_cnt = 0;
    sai_status_t status;
    ctc_sai_lag_info_t *p_db_lag;
    uint8 lchip = 0;
	uint8 gchip = 0;
    ctc_vlantag_ctl_t mode = 0;
    uint32 val_32 = 0;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
	ctcs_get_gchip_id(lchip, &gchip);
    p_db_lag = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_db_lag)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }


    switch(attr->id)
    {
    case  SAI_LAG_ATTR_PORT_VLAN_ID:
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_default_vlan(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), attr->value.u16));
            }
        }
        p_db_lag->vlan_id = attr->value.u16;
        break;

    case SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY:
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                status = ctcs_port_set_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), CTC_PORT_PROP_DEFAULT_PCP, (uint32)attr->value.u8);
                if (CTC_SAI_ERROR(status))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_LAG, "error:set default vlan priority error:%u", status);
                    status = ctc_sai_mapping_error_ctc(status);
                    return status;
                }
            }
        }
        p_db_lag->vlan_priority = attr->value.u8;
        break;
    case SAI_LAG_ATTR_DROP_UNTAGGED:
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_RETURN( ctcs_port_get_vlan_ctl(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), (ctc_vlantag_ctl_t*)&val_32));
                ctc_sai_port_mapping_tags_mode(CTC_SAI_PORT_DROP_UNTAGGED, attr->value.booldata, &mode, val_32);
                /*get the first member, then break for not map many times, all ports have same configure*/
                break;
            }
        }

        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_vlan_ctl(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), mode));
            }
        }
        p_db_lag->drop_untagged = attr->value.booldata;
        break;

    case SAI_LAG_ATTR_DROP_TAGGED:
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_RETURN( ctcs_port_get_vlan_ctl(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), (ctc_vlantag_ctl_t*)&val_32));
                ctc_sai_port_mapping_tags_mode(CTC_SAI_PORT_DROP_TAGGED, attr->value.booldata, &mode, val_32);
                /*get the first member, then break for not map many times, all ports have same configure*/
                break;
            }
        }

        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_vlan_ctl(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), mode));
            }
        }
        p_db_lag->drop_tagged = attr->value.booldata;
        break;
    case SAI_LAG_ATTR_MODE:
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag attribute mode create only\n");
        return SAI_STATUS_INVALID_ATTRIBUTE_0;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "lag attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED;

    }

    return  SAI_STATUS_SUCCESS;
}


static ctc_sai_attr_fn_entry_t  lag_attr_fn_entries[] =
{
    { SAI_LAG_ATTR_PORT_LIST,
      ctc_sai_lag_get_info,
      NULL},
      { SAI_LAG_ATTR_INGRESS_ACL,
      ctc_sai_lag_get_info,
      ctc_sai_acl_bind_point_set},
      { SAI_LAG_ATTR_EGRESS_ACL,
      NULL,
      NULL } ,
      { SAI_LAG_ATTR_PORT_VLAN_ID,
      ctc_sai_lag_get_info,
      ctc_sai_lag_set_info },
      { SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY,
      ctc_sai_lag_get_info,
      ctc_sai_lag_set_info },
      { SAI_LAG_ATTR_DROP_UNTAGGED,
      ctc_sai_lag_get_info,
      ctc_sai_lag_set_info },
      { SAI_LAG_ATTR_DROP_TAGGED,
      ctc_sai_lag_get_info,
      ctc_sai_lag_set_info },
      { SAI_LAG_ATTR_MODE,
      ctc_sai_lag_get_info,
      ctc_sai_lag_set_info },      
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};




sai_status_t
ctc_sai_lag_get_lag_member_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_lag_info_t *p_db_lag;
    sai_object_id_t lag_oid;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_LAG_MEMBER, key->key.object_id, &ctc_object_id);

    lag_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, ctc_object_id.lchip, 0, 0, ctc_object_id.value2);
    p_db_lag = ctc_sai_db_get_object_property(ctc_object_id.lchip, lag_oid);
    if (NULL == p_db_lag)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    switch(attr->id)
    {
    case SAI_LAG_MEMBER_ATTR_LAG_ID:
        attr->value.oid = lag_oid;
        break;
    case  SAI_LAG_MEMBER_ATTR_PORT_ID:
        if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_object_id.value)))
        {
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, ctc_object_id.lchip, 0, 0, ctc_object_id.value);
        }
        else
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        break;

    case SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE:
        if (CTC_BMP_ISSET(p_db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_object_id.value)))
        {
            attr->value.booldata = TRUE;
        }
        break;
    case SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE:
        if (CTC_BMP_ISSET(p_db_lag->Ingress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(ctc_object_id.value)))
        {
            attr->value.booldata = TRUE;
        }
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "lag attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED;

    }

    return  SAI_STATUS_SUCCESS;
}


static sai_status_t ctc_sai_lag_set_lag_member_info(sai_object_key_t *key,  const sai_attribute_t* attr)
{
    sai_status_t               status;
    uint32 gport;
    uint16 lag_id;
    uint8 lchip = 0;
    sai_object_id_t lag_oid;
    ctc_sai_lag_info_t *p_db_lag;
    bool egress_disable_old;
    bool ingress_disable_old;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lag_member_id(key->key.object_id, &lag_id, &gport));

    lag_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, lag_id);
    p_db_lag = ctc_sai_db_get_object_property(lchip,  lag_oid);
    if (NULL == p_db_lag  )
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag info wrong\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    if (FALSE == CTC_BMP_ISSET(p_db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "the member not in the lag :%u\n", gport);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    egress_disable_old = CTC_BMP_ISSET(p_db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport)) ? 1:0;
    ingress_disable_old = CTC_BMP_ISSET(p_db_lag->Ingress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport))?1:0;
    switch (attr->id)
    {

        case SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE:
            if (egress_disable_old == attr->value.booldata)
            {
                return SAI_STATUS_SUCCESS;
            }
            break;
        case SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE:
            if (ingress_disable_old == attr->value.booldata)
            {
                return SAI_STATUS_SUCCESS;
            }
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag member attr not implemented id:\n", attr->id);
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    switch (attr->id)
    {

        case SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE:
            if (TRUE == attr->value.booldata)
            {
                CTC_SAI_CTC_ERROR_RETURN( ctcs_linkagg_remove_port(lchip,CTC_MAP_GPORT_TO_LPORT(lag_id), gport));
                if (!ingress_disable_old)
                {
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_GPORT, lag_id), status, error1);
                }
                CTC_BMP_SET(p_db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport));
            }
            else
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_linkagg_add_port(lchip, CTC_MAP_GPORT_TO_LPORT(lag_id), gport));
                if (ingress_disable_old)
                {
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_GPORT, gport), status, error2);
                }
                CTC_BMP_UNSET(p_db_lag->Egress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport));
            }
            break;
        case SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE:
            if (TRUE == attr->value.booldata)
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_GPORT, gport), status, out);
                CTC_BMP_SET(p_db_lag->Ingress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport));
            }
            else
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_GPORT, lag_id), status, out);
                CTC_BMP_UNSET(p_db_lag->Ingress_disable_ports_bits, CTC_MAP_GPORT_TO_LPORT(gport));
            }
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag member attr not implemented id:\n", attr->id);
            return SAI_STATUS_NOT_IMPLEMENTED;

    }
    return SAI_STATUS_SUCCESS;

    error2:
    ctcs_linkagg_remove_port(lchip, CTC_MAP_GPORT_TO_LPORT(lag_id), gport);
    return status;
    error1:
    ctcs_linkagg_add_port(lchip, CTC_MAP_GPORT_TO_LPORT(lag_id), gport);
    out:
    return status;

}
static ctc_sai_attr_fn_entry_t  lag_member_attr_fn_entries[] =
{
    { SAI_LAG_MEMBER_ATTR_LAG_ID,
      ctc_sai_lag_get_lag_member_info,
      NULL},
      { SAI_LAG_MEMBER_ATTR_PORT_ID,
      ctc_sai_lag_get_lag_member_info,
      NULL },
      { SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE,
      ctc_sai_lag_get_lag_member_info,
      ctc_sai_lag_set_lag_member_info } ,
      { SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE,
      ctc_sai_lag_get_lag_member_info,
      ctc_sai_lag_set_lag_member_info},
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

#define ________SAI_DUMP________

#define CTC_SAI_LAG_PRINT_DATA_INLINE(p_file, bmp, in_line_total, fmt)\
    do{\
        uint32 loop_id = 0;\
        uint32 in_line_cnt =0;\
        uint32 member_port_cnt =0;\
        for (loop_id = 0; loop_id < sizeof(bmp)*8; loop_id++)\
        {\
            if (CTC_BMP_ISSET(bmp, loop_id))\
            {\
                member_port_cnt++;\
            }\
        }\
        CTC_SAI_LOG_DUMP(p_file, fmt, member_port_cnt);\
        for (loop_id = 0; loop_id < sizeof(bmp)*8; loop_id++)\
        {\
            if (CTC_BMP_ISSET(bmp, loop_id))\
            {\
                if (in_line_total == in_line_cnt)\
                {\
                    in_line_cnt =0;\
                    CTC_SAI_LOG_DUMP(p_file, "\n");\
                }\
                CTC_SAI_LOG_DUMP(p_file, "%-6d", loop_id);\
                in_line_cnt++;\
            }\
        }\
        CTC_SAI_LOG_DUMP(p_file, "\n");\
    }while(0)

static sai_status_t
_ctc_sai_lag_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  lag_oid_cur = 0;
    ctc_sai_lag_info_t    ctc_sai_lag_cur;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;

    sal_memset(&ctc_sai_lag_cur, 0, sizeof(ctc_sai_dump_grep_param_t));

    lag_oid_cur = bucket_data->oid;
    sal_memcpy((ctc_sai_dump_grep_param_t*)(&ctc_sai_lag_cur), bucket_data->data, sizeof(ctc_sai_dump_grep_param_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (lag_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "No.%-6d %-13s 0x%016"PRIx64"\n", num_cnt, "Lag_oid     :", lag_oid_cur);
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

    CTC_SAI_LOG_DUMP(p_file, "Vlan_id:%-4d Vlan_pri:%-2d Is_binding_rif:%-2d Is_binding_sub_rif:%-2d  Drop_tagged:%-1d  Drop_untagged:%-1d\n", \
    ctc_sai_lag_cur.vlan_id,  ctc_sai_lag_cur.vlan_priority,  ctc_sai_lag_cur.is_binding_rif, ctc_sai_lag_cur.is_binding_sub_rif, ctc_sai_lag_cur.drop_tagged, ctc_sai_lag_cur.drop_untagged);

    /*print uint32 member_ports_bits[8] ===>> port; */
    CTC_SAI_LAG_PRINT_DATA_INLINE(p_file, ctc_sai_lag_cur.member_ports_bits, IN_LINE_CNT, "Member_port:£¨total %-4d)\n");
    /*print uint32 Ingress_disable_ports_bits[8]; == = >> port; */
    CTC_SAI_LAG_PRINT_DATA_INLINE(p_file, ctc_sai_lag_cur.Ingress_disable_ports_bits, IN_LINE_CNT, "Ingress_disable_port:£¨total %-4d)\n");
    /*print uint32 Egress_disable_ports_bits[8];== = >> port;*/
    CTC_SAI_LAG_PRINT_DATA_INLINE(p_file, ctc_sai_lag_cur.Egress_disable_ports_bits, IN_LINE_CNT, "Egress_disable_port:£¨total %-4d)\n");

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________
sai_status_t ctc_sai_lag_binding_rif(sai_object_id_t sai_lag_id, uint8 is_binding, uint8 l3if_type)
{
    uint8 lchip = 0;
    ctc_sai_lag_info_t*  p_db_lag = NULL;
    ctc_sai_oid_get_lchip(sai_lag_id, &lchip);
    p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
    if (NULL == p_db_lag)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    if (CTC_L3IF_TYPE_PHY_IF == l3if_type)
    {
        p_db_lag->is_binding_rif = is_binding;
    }
    if(CTC_L3IF_TYPE_SUB_IF == l3if_type)
    {   
        /*one port bind multi sub-if*/
        if(is_binding)
        {
            p_db_lag->is_binding_sub_rif = is_binding;
            p_db_lag->binding_sub_rif_count ++;
        }
        else
        {
            p_db_lag->binding_sub_rif_count --;
            if(1 > p_db_lag->binding_sub_rif_count)
            {
                p_db_lag->is_binding_sub_rif = is_binding;
            }
        }
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_lag_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t lag_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_LAG, lag_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_LAG, CTC_MAP_GPORT_TO_LPORT(ctc_object_id.value)));

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_lag_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Linkagg MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_LAG))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Linkagg");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_lag_info_t");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_LAG,
                                            (hash_traversal_fn)_ctc_sai_lag_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________

static sai_status_t   ctc_sai_lag_create_lag( sai_object_id_t     * sai_lag_id,
                                             sai_object_id_t        switch_id,
                                             uint32_t               attr_count,
                                             const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    sai_status_t status = 0;
    ctc_linkagg_group_t linkagg_grp;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX];
    uint32 lag_id_tmp = 0;
    ctc_sai_lag_info_t*  p_db_lag = NULL;
    const sai_attribute_value_t *attr = NULL;
    uint32 attr_index = 0;
    uint32 lag_gport = 0;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    if (NULL == sai_lag_id)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "NULL lag id param\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    sal_memset(capability, 0 , sizeof(capability));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability));
    CTC_SAI_DB_LOCK(lchip);

    sal_memset(&linkagg_grp, 0, sizeof(linkagg_grp));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_ATTR_MODE, &attr, &attr_index);
    if (SAI_STATUS_SUCCESS == status)
    {
        switch (attr->s32)
        {
            case SAI_LAG_MODE_STATIC:
                linkagg_grp.linkagg_mode = CTC_LINKAGG_MODE_STATIC;
                linkagg_grp.member_num = 255;
                break;
            case SAI_LAG_MODE_STATIC_FAILOVER:
                linkagg_grp.linkagg_mode = CTC_LINKAGG_MODE_STATIC_FAILOVER;
                linkagg_grp.member_num = 24;
                break;
            case SAI_LAG_MODE_RR:
                linkagg_grp.linkagg_mode = CTC_LINKAGG_MODE_RR;
                linkagg_grp.member_num = 24;
                break;
            case SAI_LAG_MODE_DLB:
                linkagg_grp.linkagg_mode = CTC_LINKAGG_MODE_DLB;
                linkagg_grp.member_num = 256;
                break;
            case SAI_LAG_MODE_RH:
                linkagg_grp.linkagg_mode = CTC_LINKAGG_MODE_RESILIENT;
                linkagg_grp.member_num = 256;
                break;
            default:
                CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag mode not support\n");
                return  SAI_STATUS_NOT_IMPLEMENTED;
        }
    }
    else
    {
        linkagg_grp.linkagg_mode = CTC_LINKAGG_MODE_STATIC;
        linkagg_grp.member_num = 255;
    }
    //linkagg_grp.member_num = capability[CTC_GLOBAL_CAPABILITY_LINKAGG_MEMBER_NUM];
    linkagg_grp.member_num = 16;
    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_LAG, &lag_id_tmp);
    if (status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "alloc lag id error \n");
        CTC_SAI_DB_UNLOCK(lchip);
        return  status;
    }
    linkagg_grp.tid = lag_id_tmp;

    status = ctcs_linkagg_create(lchip, &linkagg_grp);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "create lag error:%d\n", status);
        status = ctc_sai_mapping_error_ctc(status);
        goto error0;
    }

    p_db_lag = mem_malloc(MEM_LINKAGG_MODULE, sizeof(ctc_sai_lag_info_t));
    if (NULL == p_db_lag)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to allocate lag db entry:%d\n", status);
        goto error1;
    }
    sal_memset(p_db_lag, 0 , sizeof(ctc_sai_lag_info_t));
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_ATTR_PORT_VLAN_ID, &attr, &attr_index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_db_lag->vlan_id = attr->u16;
    }
    else
    {
        p_db_lag->vlan_id = 1;
    }

    status =  ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY, &attr, &attr_index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_db_lag->vlan_priority = attr->u8;
    }
    else
    {
        p_db_lag->vlan_priority = 0;
    }

    status =  ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_ATTR_DROP_UNTAGGED, &attr, &attr_index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_db_lag->drop_untagged = attr->booldata;
    }
    else
    {
        p_db_lag->drop_untagged = false;
    }

    status =  ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_ATTR_DROP_TAGGED, &attr, &attr_index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_db_lag->drop_tagged = attr->booldata;
    }
    else
    {
        p_db_lag->drop_tagged = false;
    }
    status =  ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_LAG_ATTR_MODE, &attr, &attr_index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_db_lag->lag_mode = attr->s32;
    }
    else
    {
        p_db_lag->lag_mode = CTC_LINKAGG_MODE_STATIC;
    }
    /*0x1f | lag_id*/
    lag_gport = CTC_MAP_LPORT_TO_GPORT(0x1f, lag_id_tmp);
    *sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, lag_gport);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *sai_lag_id, p_db_lag ), status, error2);
    goto out;

error2:
    mem_free(p_db_lag);
error1:
    ctcs_linkagg_destroy(lchip, lag_id_tmp);
error0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_LAG, lag_id_tmp);

out:
    CTC_SAI_DB_UNLOCK((uint8)lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to create lag entry:%d\n", status);
    }
    return status;
}
static sai_status_t ctc_sai_lag_remove_lag( sai_object_id_t lag_id)
{
    ctc_object_id_t ctc_object_id ;
    sai_status_t status = 0;
    ctc_sai_lag_info_t *p_db_lag = NULL ;
    uint32 lag_id_tmp = 0;

    sal_memset(&ctc_object_id, 0 , sizeof(ctc_object_id));

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_LAG, lag_id, &ctc_object_id);
    CTC_SAI_DB_LOCK(ctc_object_id.lchip);
    p_db_lag = ctc_sai_db_get_object_property(ctc_object_id.lchip, lag_id);
    if (NULL == p_db_lag)
    {
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }
    if ((p_db_lag->is_binding_rif)||(p_db_lag->is_binding_sub_rif))
    {
        status = SAI_STATUS_OBJECT_IN_USE;
        goto out;
    }
    lag_id_tmp =  CTC_MAP_GPORT_TO_LPORT(ctc_object_id.value);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_free_id(ctc_object_id.lchip, CTC_SAI_DB_ID_TYPE_LAG, lag_id_tmp), status, out);
    ctcs_linkagg_destroy(ctc_object_id.lchip, (uint8)lag_id_tmp);
    mem_free(p_db_lag);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_remove_object_property(ctc_object_id.lchip, lag_id ), status, out);
    goto out;

out:
    CTC_SAI_DB_UNLOCK(ctc_object_id.lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to remove lag entry%d\n", status);
    }
    return status;
}

static sai_status_t ctc_sai_lag_set_lag_attribute( sai_object_id_t lag_id,  const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = lag_id };
    sai_status_t           status = 0;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(lag_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_LAG,  lag_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to set lag attr:%d, status:%d\n", attr->id, status);
    }
    return status;
}
static sai_status_t ctc_sai_lag_get_lag_attribute( sai_object_id_t     lag_id,
                                            uint32_t            attr_count,
                                           sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = lag_id
    }
    ;
    sai_status_t    status = 0;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(lag_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_LAG, loop, lag_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to get lag attr:%d, attr_id:%d\n", status, attr_list[loop].id);
    }
    return status;
}
static sai_status_t ctc_sai_lag_create_lag_member( sai_object_id_t     * lag_member_id,
                                            sai_object_id_t        switch_id,
                                            uint32_t               attr_count,
                                            const sai_attribute_t *attr_list)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    if (NULL == lag_member_id || 0 == attr_count || NULL == attr_list )
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, " lag member parameter invalid\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = _ctc_sai_lag_create_lag_member(lag_member_id, switch_id, attr_count, attr_list);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to create  lag member:%d\n", status);
    }
    return status;
}
static sai_status_t ctc_sai_lag_remove_lag_member( sai_object_id_t lag_member_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(lag_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = _ctc_sai_lag_remove_lag_member(lag_member_id);
    CTC_SAI_DB_UNLOCK(lchip);
     if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to remove  lag member:%d\n", status);
    }
    return status;
}

static sai_status_t ctc_sai_lag_set_lag_member_attribute( sai_object_id_t lag_member_id,  const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = lag_member_id };
    sai_status_t status = SAI_STATUS_SUCCESS;
    char key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(lag_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_LAG,  lag_member_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to set lag member attr:%d, status:%d\n", attr->id, status);
    }
    return status;
}
static sai_status_t ctc_sai_lag_get_lag_member_attribute( sai_object_id_t     lag_member_id,
                                                         uint32_t            attr_count,
                                                         sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = lag_member_id
    }
    ;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_LAG);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(lag_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_LAG, loop, lag_member_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to get lag member attr:%d, attr_id:%d\n", status, attr_list[loop].id);
    }
    return status;
}
static sai_status_t ctc_sai_lag_create_lag_members( sai_object_id_t          switch_id,
                                                   uint32_t                 object_count,
                                                   const uint32_t          *attr_count,
                                                   const sai_attribute_t  **attr_list,
                                                   sai_bulk_op_error_mode_t mode,
                                                   sai_object_id_t        *object_id,
                                                   sai_status_t           *object_statuses)
{
    uint32 index = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 is_found_error;
    uint8 lchip = 0 ;

    if (NULL == object_id || NULL == attr_count || NULL == attr_list || NULL == object_statuses || 0 == object_count)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, " lag member invalid parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    for (index = 0; index < object_count; index++)
    {
        status = _ctc_sai_lag_create_lag_member(&object_id[index], switch_id, attr_count[index], attr_list[index]);
        object_statuses[index] =  status;

        if (status != SAI_STATUS_SUCCESS  )
        {
            is_found_error = TRUE;
        }

        if (status != SAI_STATUS_SUCCESS  && SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode )
        {
            break;
        }
    }

    if (status != SAI_STATUS_SUCCESS  && SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode )
    {
        for (index++; index < object_count; index++)
        {
            object_statuses[index] = SAI_STATUS_NOT_EXECUTED;
        }
    }

    if (TRUE == is_found_error)
    {
        status = SAI_STATUS_FAILURE;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to create  lag members :%d\n", status);
    }
    return status;
}

static sai_status_t ctc_sai_lag_remove_lag_members( uint32_t                 object_count,
                                             const sai_object_id_t   *object_id,
                                             sai_bulk_op_error_mode_t mode,
                                             sai_status_t           *object_statuses)
{

    uint32 index = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 is_found_error = 0;
    uint8 lchip = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(object_id[index], &lchip));
    CTC_SAI_DB_LOCK(lchip);
    for (index = 0; index < object_count; index++)
    {
        status = _ctc_sai_lag_remove_lag_member(object_id[index]);
        object_statuses[index] =  status;

        if (status != SAI_STATUS_SUCCESS  )
        {
            is_found_error = TRUE;
        }

        if (status != SAI_STATUS_SUCCESS  && SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode )
        {
            break;
        }
    }


    if (status != SAI_STATUS_SUCCESS  && SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode )
    {
        for (index++; index < object_count; index++)
        {
            object_statuses[index] = SAI_STATUS_NOT_EXECUTED;
        }
    }

    if (TRUE == is_found_error)
    {
        status = SAI_STATUS_FAILURE;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Failed to remove  lag members:%d\n", status);
    }
    return status;
}

const sai_lag_api_t g_ctc_sai_lag_api =
{
    ctc_sai_lag_create_lag,
    ctc_sai_lag_remove_lag,
    ctc_sai_lag_set_lag_attribute,
    ctc_sai_lag_get_lag_attribute,
    ctc_sai_lag_create_lag_member,
    ctc_sai_lag_remove_lag_member,
    ctc_sai_lag_set_lag_member_attribute,
    ctc_sai_lag_get_lag_member_attribute,
    ctc_sai_lag_create_lag_members,
    ctc_sai_lag_remove_lag_members,
};

sai_status_t
ctc_sai_lag_register_member_change_cb(uint8 lchip, ctc_sai_lag_mem_change_type_t type, uint32 lag_port, ctc_sai_lag_member_change_notification_fn cb)
{
    sai_object_id_t oid = 0;
    ctc_sai_lag_info_t* p_lag = NULL;

    oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, lag_port);
    p_lag = ctc_sai_db_get_object_property(lchip, oid);
    if (NULL == p_lag )
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag info wrong\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_lag->cb[type] = cb;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_lag_notification_all_members_change(uint8 lchip, ctc_sai_lag_mem_change_type_t type, uint32 lag_port, uint32 change)
{
    sai_object_id_t oid = 0;
    ctc_sai_lag_info_t* p_lag = NULL;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;

    ctcs_get_gchip_id(lchip, &gchip);
    oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, lag_port);
    p_lag = ctc_sai_db_get_object_property(lchip,  oid);
    if (NULL == p_lag )
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "lag info wrong\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if (p_lag->cb[type])
    {
        for (bit_cnt = 0; bit_cnt < sizeof(p_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_lag->member_ports_bits, bit_cnt))
            {
                (p_lag->cb[type])(lchip, lag_port, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), change);
            }
        }
    }

    if (false == change)
    {
        p_lag->cb[type] = NULL;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_lag_api_init()
{
    ctc_sai_register_module_api(SAI_API_LAG, (void*)&g_ctc_sai_lag_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_lag_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_LAG;
    wb_info.data_len = sizeof(ctc_sai_lag_info_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_lag_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_LAG, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

