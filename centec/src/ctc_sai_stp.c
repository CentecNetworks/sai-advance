#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_stp.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_lag.h"



typedef struct ctc_sai_stp_info_s
{
    uint32 vlan_bind_bits[128]; 
    uint32 port_bind_bits[8];  // normal port bit
    uint32 vlan_bind_count;
    uint32 port_bind_count;   // lag port and normal port total count
    uint32 lag_bind_bits[8];  // lag port bit
}ctc_sai_stp_info_t;

static sai_status_t ctc_sai_stp_check_port_state(sai_stp_port_state_t state)
{
    switch (state) {
    case SAI_STP_PORT_STATE_LEARNING:
    case SAI_STP_PORT_STATE_FORWARDING:
    case SAI_STP_PORT_STATE_BLOCKING:
        return SAI_STATUS_SUCCESS;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Invalid port state\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
}
static uint8 ctc_sai_stp_map_ctc_port_state(sai_stp_port_state_t state)
{
    switch (state) {
    case SAI_STP_PORT_STATE_LEARNING:
        return CTC_STP_LEARNING;

    case SAI_STP_PORT_STATE_FORWARDING:
        return CTC_STP_FORWARDING;

    case SAI_STP_PORT_STATE_BLOCKING:
        return CTC_STP_BLOCKING;
    }

    return CTC_STP_UNAVAIL;
}
static sai_stp_port_state_t ctc_sai_stp_map_sai_port_state(uint8 state)
{
    switch (state) {
    case CTC_STP_LEARNING :
        return SAI_STP_PORT_STATE_LEARNING;

    case CTC_STP_FORWARDING :
        return SAI_STP_PORT_STATE_FORWARDING;

    case CTC_STP_BLOCKING  :
        return SAI_STP_PORT_STATE_BLOCKING;
    }

    return SAI_STP_PORT_STATE_FORWARDING;
}

sai_status_t
ctc_sai_stp_get_stp_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    ctc_object_id_t ctc_object_id;
    uint32 bit_cnt = 0;
    uint32 port_num = 0;
    uint32 vlan_num =0;
    sai_object_id_t*stp_ports;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_stp_info_t *p_db_stp;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    uint8 gchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP, key->key.object_id, &ctc_object_id);

    ctcs_get_gchip_id(ctc_object_id.lchip, &gchip);

    p_db_stp = ctc_sai_db_get_object_property(ctc_object_id.lchip, key->key.object_id);
    if (NULL == p_db_stp)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    switch(attr->id)
    {
    case SAI_STP_ATTR_VLAN_LIST:
        /* Check if has got enough memory to store the vlanlist */
        if (attr->value.vlanlist.count < p_db_stp->vlan_bind_count)
        {
            CTC_SAI_LOG_ERROR(SAI_API_STP, "not enough memory , vlanlist count:%d db entry count:%d\n", attr->value.vlanlist.count ,  p_db_stp->vlan_bind_count);
            return SAI_STATUS_BUFFER_OVERFLOW;
        }
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_stp->vlan_bind_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_stp->vlan_bind_bits, bit_cnt))
            {
                attr->value.vlanlist.list[vlan_num] =   bit_cnt;
                vlan_num++;
            }
        }
         attr->value.vlanlist.count = vlan_num;
        break;
    case  SAI_STP_ATTR_PORT_LIST:
        /* Check if has got enough memory to store the portlist */
        if (attr->value.objlist.count < p_db_stp->port_bind_count)
        {
            CTC_SAI_LOG_ERROR(SAI_API_STP, "not enough memory , objlist count:%d db entry count:%d\n", attr->value.objlist.count ,  p_db_stp->port_bind_count);
            return SAI_STATUS_BUFFER_OVERFLOW;
        }
        stp_ports =  mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*p_db_stp->port_bind_count);
        if (NULL == stp_ports)
        {
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(stp_ports, 0, sizeof(sai_object_id_t)*p_db_stp->port_bind_count);
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_stp->port_bind_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_stp->port_bind_bits, bit_cnt))
            {
                stp_ports[port_num] =  ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP_PORT, ctc_object_id.lchip, 0, ctc_object_id.value, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt));
                port_num++;
            }
        }

        for (bit_cnt = 0; bit_cnt < sizeof(p_db_stp->lag_bind_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_stp->lag_bind_bits, bit_cnt))
            {
                stp_ports[port_num] =  ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP_PORT, ctc_object_id.lchip, 0, ctc_object_id.value, CTC_MAP_LPORT_TO_GPORT(0x1f, bit_cnt));
                port_num++;
            }
        }

        status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), stp_ports, port_num, &attr->value.objlist);
        mem_free(stp_ports);
        
        break;
    case  SAI_STP_ATTR_BRIDGE_ID:
        p_switch_master = ctc_sai_get_switch_property(ctc_object_id.lchip);
        attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, ctc_object_id.lchip, SAI_BRIDGE_TYPE_1Q, 0, p_switch_master->default_bridge_id);
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_STP, "stp attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED + attr_idx;

    }

    return  status;
}


static ctc_sai_attr_fn_entry_t  stp_attr_fn_entries[] =
{
    { SAI_STP_ATTR_VLAN_LIST,
      ctc_sai_stp_get_stp_info,
      NULL},
    { SAI_STP_ATTR_PORT_LIST,
      ctc_sai_stp_get_stp_info,
      NULL },
    { SAI_STP_ATTR_BRIDGE_ID,
      ctc_sai_stp_get_stp_info,
      NULL},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};


sai_status_t
ctc_sai_stp_get_port_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    ctc_object_id_t ctc_object_id;
    uint8 ctc_stp_state ;
    uint32 bit_cnt = 0;
    ctc_sai_lag_info_t *p_db_lag;
    uint8 gchip = 0;
    sai_object_id_t sai_lag_id;
    

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP_PORT, key->key.object_id, &ctc_object_id);
    ctcs_get_gchip_id(ctc_object_id.lchip, &gchip);

    switch(attr->id)
    {
    case SAI_STP_PORT_ATTR_STP:
         attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP, ctc_object_id.lchip, 0, 0, ctc_object_id.value2);
        break;
    case  SAI_STP_PORT_ATTR_BRIDGE_PORT:
        attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, ctc_object_id.lchip, 0, SAI_BRIDGE_PORT_TYPE_PORT, ctc_object_id.value);
        break;
    case  SAI_STP_PORT_ATTR_STATE:

        if(CTC_IS_LINKAGG_PORT(ctc_object_id.value))
        {   
            sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, ctc_object_id.lchip, 0, 0, ctc_object_id.value);
            p_db_lag = ctc_sai_db_get_object_property(ctc_object_id.lchip, sai_lag_id);
            if (NULL == p_db_lag)
            {
                return SAI_STATUS_INVALID_OBJECT_ID;
            }       
            for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                {
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_stp_get_state(ctc_object_id.lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), ctc_object_id.value2, &ctc_stp_state));
                    break;
                }
            }
        }
        else
        {
           CTC_SAI_CTC_ERROR_RETURN(ctcs_stp_get_state(ctc_object_id.lchip, ctc_object_id.value, ctc_object_id.value2, &ctc_stp_state));
        }
        
        attr->value.s32 = ctc_sai_stp_map_sai_port_state(ctc_stp_state);
        break;
        
    default:
        CTC_SAI_LOG_ERROR(SAI_API_STP, "stp port attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED;
    }
    return  SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_stp_set_port_info(sai_object_key_t *key,  const sai_attribute_t* attr)
{
    ctc_object_id_t ctc_object_id;
    uint8 ctc_port_state;
    uint32 bit_cnt = 0;
    ctc_sai_lag_info_t *p_db_lag;
    uint8 gchip = 0;
    sai_object_id_t sai_lag_id;
    
    CTC_SAI_LOG_ENTER(SAI_API_STP);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP_PORT, key->key.object_id, &ctc_object_id);
    ctcs_get_gchip_id(ctc_object_id.lchip, &gchip);

    
    switch(attr->id)
    {
    case  SAI_STP_PORT_ATTR_STATE:
        ctc_port_state = ctc_sai_stp_map_ctc_port_state(attr->value.s32);

        if(CTC_IS_LINKAGG_PORT(ctc_object_id.value))
        {   
            sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, ctc_object_id.lchip, 0, 0, ctc_object_id.value);
            p_db_lag = ctc_sai_db_get_object_property(ctc_object_id.lchip, sai_lag_id);
            if (NULL == p_db_lag)
            {
                return SAI_STATUS_INVALID_OBJECT_ID;
            }       
            for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
            {
                if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                {
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_stp_set_state(ctc_object_id.lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), (uint8)ctc_object_id.value2, ctc_port_state));
                }
            }
        }
        else
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_stp_set_state(ctc_object_id.lchip, ctc_object_id.value, (uint8)ctc_object_id.value2, ctc_port_state));  
        }

        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_STP, "stp port attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}



static  ctc_sai_attr_fn_entry_t stp_port_attr_fn_entries[] = {
    { SAI_STP_PORT_ATTR_STP,
      ctc_sai_stp_get_port_info,
      NULL},
    { SAI_STP_PORT_ATTR_BRIDGE_PORT,
      ctc_sai_stp_get_port_info,
      NULL },
    { SAI_STP_PORT_ATTR_STATE,
      ctc_sai_stp_get_port_info,
      ctc_sai_stp_set_port_info},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

static sai_status_t _ctc_sai_stp_create_stp_port(sai_object_id_t      *stp_port_id,
                                                sai_object_id_t        switch_id,
                                                uint32_t               attr_count,
                                                const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32   stp_index, bridge_port_index, state_index;
    const sai_attribute_value_t *stp, *bridge_port, *state;
    ctc_object_id_t   stp_oid;
    ctc_sai_stp_info_t*  p_db_stp = NULL;
    uint8 lchip;
    ctc_sai_bridge_port_t* p_bridge_port;
    uint32 gport ;
    uint8 ctc_port_state;
    uint32 bit_cnt = 0;
    ctc_sai_lag_info_t *p_db_lag;
    uint8 gchip = 0;
    sai_object_id_t  sai_lag_id;
    ctc_sai_stp_port_t* p_db_stp_port = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    if (NULL == stp_port_id || 0 == attr_count || NULL == attr_list )
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_sai_oid_get_lchip(switch_id, &lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_STP_PORT_ATTR_STP, &stp, &stp_index);
    if(SAI_STATUS_SUCCESS != status)
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_STP_PORT_ATTR_BRIDGE_PORT, &bridge_port, &bridge_port_index);
    if(SAI_STATUS_SUCCESS != status)
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_STP_PORT_ATTR_STATE, &state, &state_index);
    if(SAI_STATUS_SUCCESS != status)
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_stp_check_port_state(state->s32);
    if (status)
    {
        goto out;
    }

    ctc_port_state = ctc_sai_stp_map_ctc_port_state(state->s32);

    p_bridge_port = ctc_sai_db_get_object_property(lchip, bridge_port->oid);
    if (NULL == p_bridge_port  )
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "bridge port not found\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    if (SAI_BRIDGE_PORT_TYPE_PORT  != p_bridge_port->port_type )
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Bridge port type wrong\n");
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }

    p_db_stp = ctc_sai_db_get_object_property(lchip,  stp->oid);
    if (NULL == p_db_stp  )
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "stp instance not found \n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    gport = p_bridge_port->gport;
    ctcs_get_gchip_id(lchip, &gchip);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP, stp->oid, &stp_oid );

    if(CTC_IS_LINKAGG_PORT(gport))
    {   
        sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
        p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
        if (NULL == p_db_lag)
        {
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto out;
        }       
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_stp_set_state(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), stp_oid.value, ctc_port_state), status, out);
            }
        }
        
        CTC_BMP_SET(p_db_stp->lag_bind_bits, (uint8)gport); 
    }
    else
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_stp_set_state(lchip, gport, stp_oid.value, ctc_port_state), status, out);
        CTC_BMP_SET(p_db_stp->port_bind_bits, CTC_MAP_GPORT_TO_LPORT(gport));    
    }

    p_db_stp->port_bind_count ++;
    
    *stp_port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP_PORT, lchip, 0, stp_oid.value, gport);

     p_db_stp_port = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_stp_port_t));
    if (NULL == p_db_stp_port)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to allocate stp port db entry:%d\n", status);
        goto out;
    }
    sal_memset(p_db_stp_port, 0 , sizeof(ctc_sai_stp_port_t));

    p_db_stp_port->stp_port_state = ctc_port_state;
    
    ctc_sai_db_add_object_property(lchip, *stp_port_id, p_db_stp_port );

    CTC_BMP_SET(p_bridge_port->stp_port_bind_bits, stp_oid.value);
    p_bridge_port->stp_port_bind_count++;
    p_bridge_port->stp_port_state[stp_oid.value] = ctc_port_state;

   
    out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to create stp port :%d\n", status);
    }
    return status;

}

static sai_status_t _ctc_sai_stp_remove_stp_port(sai_object_id_t stp_port_id)
{
    sai_status_t        status = SAI_STATUS_SUCCESS;
    ctc_object_id_t   ctc_stp_port_oid;
    sai_object_id_t stp_oid;
    ctc_sai_stp_info_t*  p_db_stp = NULL;
    uint8 lchip;
    ctc_sai_lag_info_t *p_db_lag;
    sai_object_id_t  sai_lag_id;
    uint32 bit_cnt = 0;
    uint8 gchip = 0;
    ctc_sai_bridge_port_t* p_bridge_port;
    sai_object_id_t  bridge_port_oid;
    ctc_sai_stp_port_t* p_db_stp_port = NULL;

    ctc_sai_oid_get_lchip(stp_port_id, &lchip);
    ctcs_get_gchip_id(lchip, &gchip);

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    if (SAI_NULL_OBJECT_ID == stp_port_id  )
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "stp port id is null\n");
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP_PORT, stp_port_id, &ctc_stp_port_oid);

    stp_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP, ctc_stp_port_oid.lchip, 0, 0, ctc_stp_port_oid.value2);
    p_db_stp = ctc_sai_db_get_object_property(ctc_stp_port_oid.lchip,  stp_oid);
    if (NULL == p_db_stp  )
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "stp instance not found \n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }


    if(CTC_IS_LINKAGG_PORT(ctc_stp_port_oid.value))
    {
        sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, ctc_stp_port_oid.value);
        p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);

        if (NULL == p_db_lag)
        {
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto out;
        }       

        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_stp_set_state(ctc_stp_port_oid.lchip, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), ctc_stp_port_oid.value2, CTC_STP_FORWARDING), status, out);
            }
        }
        
        CTC_BMP_UNSET(p_db_stp->lag_bind_bits, (uint8)ctc_stp_port_oid.value);
    }
    else
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_stp_set_state(ctc_stp_port_oid.lchip, ctc_stp_port_oid.value, ctc_stp_port_oid.value2, CTC_STP_FORWARDING), status, out);
        CTC_BMP_UNSET(p_db_stp->port_bind_bits, CTC_MAP_GPORT_TO_LPORT(ctc_stp_port_oid.value));
    }

    p_db_stp->port_bind_count--;
    
    p_db_stp_port = ctc_sai_db_get_object_property(lchip, stp_port_id);
    mem_free(p_db_stp_port);
    ctc_sai_db_remove_object_property(lchip, stp_port_id);

    bridge_port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, 0, SAI_BRIDGE_PORT_TYPE_PORT, ctc_stp_port_oid.value);
    p_bridge_port = ctc_sai_db_get_object_property(lchip, bridge_port_oid);
    
    CTC_BMP_UNSET(p_bridge_port->stp_port_bind_bits, ctc_stp_port_oid.value2);
    p_bridge_port->stp_port_bind_count--;
    p_bridge_port->stp_port_state[ctc_stp_port_oid.value2] = CTC_STP_FORWARDING;


    out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to remove stp port :%d\n", status);
    }
    return status;
}

#define ________SAI_DUMP________

#define CTC_SAI_STP_PRINT_DATA_INLINE(p_file, bmp, in_line_total, fmt, arg...)\
    do{\
        uint32 loop_id = 0;\
        uint32 in_line_cnt =0;\
        CTC_SAI_LOG_DUMP(p_file, fmt, ##arg);\
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
_ctc_sai_stp_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  stp_oid_cur = 0;
    ctc_sai_stp_info_t    ctc_sai_stp_cur;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;

    sal_memset(&ctc_sai_stp_cur, 0, sizeof(ctc_sai_stp_info_t));

    stp_oid_cur = bucket_data->oid;
    sal_memcpy((ctc_sai_stp_info_t*)(&ctc_sai_stp_cur), bucket_data->data, sizeof(ctc_sai_stp_info_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (stp_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "No.%-6d %-13s 0x%016"PRIx64"\n", num_cnt, "Stp_oid     :", stp_oid_cur);
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

    /*print uint32 vlan_bind_bits[128]; ===>> vlan_id; */
    CTC_SAI_STP_PRINT_DATA_INLINE(p_file, ctc_sai_stp_cur.vlan_bind_bits, IN_LINE_CNT, "vlan_binded:(total %d)\n", ctc_sai_stp_cur.vlan_bind_count);
    /*print uint32 port_bind_bits[8]; ===>> port; */
    CTC_SAI_STP_PRINT_DATA_INLINE(p_file, ctc_sai_stp_cur.port_bind_bits, IN_LINE_CNT, "port_binded:(total %d)\n", ctc_sai_stp_cur.port_bind_count);

    CTC_SAI_STP_PRINT_DATA_INLINE(p_file, ctc_sai_stp_cur.lag_bind_bits, IN_LINE_CNT, "lag_binded:(total %d)\n", ctc_sai_stp_cur.port_bind_count);
    

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________
sai_status_t ctc_sai_stp_set_instance(uint8 lchip, uint16 vlan_id, uint16 vlan_ptr, sai_object_id_t stp_oid, uint8 is_add)
{
    ctc_sai_stp_info_t *p_db_stp = NULL;
    ctc_object_id_t ctc_object_id;
    
    p_db_stp = ctc_sai_db_get_object_property(lchip,  stp_oid);
    if (NULL == p_db_stp  )
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "stp instance not found \n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP, stp_oid, &ctc_object_id);
    if (is_add)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_stp_set_vlan_stpid(lchip, vlan_ptr, (uint8)ctc_object_id.value));
        if (ctc_object_id.value) 
        {
            CTC_BMP_SET(p_db_stp->vlan_bind_bits, vlan_id);
            p_db_stp->vlan_bind_count ++;
        }
    }
    else
    {
        if (ctc_object_id.value) 
        {
            CTC_BMP_UNSET(p_db_stp->vlan_bind_bits, vlan_id);
            p_db_stp->vlan_bind_count --;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_stp_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t sai_stp_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, sai_stp_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_STP, ctc_object_id.value));

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_stp_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI STP MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_STP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Stp");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_stp_info_t");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_STP,
                                            (hash_traversal_fn)_ctc_sai_stp_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________
/**
 * @brief Create stp instance with default port state as blocking.
 *
 * @param[out] sai_stp_id stp instance id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Value of attributes
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
static sai_status_t ctc_sai_stp_create_stp(sai_object_id_t      *sai_stp_id,
                                           sai_object_id_t        switch_id,
                                           uint32_t               attr_count,
                                           const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 stp_id = 0;
    ctc_sai_stp_info_t*  p_db_stp = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    if (NULL == sai_stp_id)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_STP, &stp_id);
    if (status)
    {
        goto out;
    }
    *sai_stp_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP, lchip, 0, 0, stp_id);

    p_db_stp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_stp_info_t));
    if (NULL == p_db_stp)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to allocate stp db entry:%d\n", status);
        goto error0;
    }
    sal_memset(p_db_stp, 0 , sizeof(ctc_sai_stp_info_t));
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *sai_stp_id, p_db_stp ), status, error1);
    goto out;

error1:
    mem_free(p_db_stp);
error0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_STP, stp_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to create stp :%d\n", status);
    }
    return status;

}

/**
 * @brief Remove stp instance.
 *
 * @param[in] sai_stp_id Stp instance id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
static sai_status_t ctc_sai_stp_remove_stp(sai_object_id_t sai_stp_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_object_id_t  ctc_object_id;
    ctc_sai_stp_info_t*  p_db_stp = NULL;
    

    sal_memset(&ctc_object_id, 0 ,sizeof(ctc_object_id_t));
    CTC_SAI_LOG_ENTER(SAI_API_STP);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP, sai_stp_id, &ctc_object_id);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_stp_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    p_db_stp = ctc_sai_db_get_object_property(lchip, sai_stp_id);    
    if (NULL == p_db_stp)
    {
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }

    if (p_db_stp->vlan_bind_count) 
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to remove stp , because have vlans binding such stpid \n");
        status = SAI_STATUS_FAILURE;
        goto out;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_remove_object_property(lchip, sai_stp_id ), status, out);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_STP, ctc_object_id.value), status, error0);
    mem_free(p_db_stp);
    goto out;

error0:
    ctc_sai_db_add_object_property(lchip, sai_stp_id, p_db_stp);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to remove stp :%d\n", status);
    }
    return status;
}



/**
 * @brief Create stp port object
 *
 * @param[out] stp_port_id stp port id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Value of attributes
 * @return SAI_STATUS_SUCCESS if operation is successful otherwise a different
 *  error code is returned.
 */
static sai_status_t ctc_sai_stp_create_stp_port(sai_object_id_t      *stp_port_id,
                                                sai_object_id_t        switch_id,
                                                uint32_t               attr_count,
                                                const sai_attribute_t *attr_list)

{
    sai_status_t  status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    if (NULL == stp_port_id || 0 == attr_count || NULL == attr_list )
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, " stp port parameter invalid\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = _ctc_sai_stp_create_stp_port(stp_port_id, switch_id, attr_count, attr_list);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to create stp port:%d\n", status);
    }
    return status;
}

/**
 * @brief Remove stp port object.
 *
 * @param[in] stp_port_id stp object id
 * @return SAI_STATUS_SUCCESS if operation is successful otherwise a different
 *  error code is returned.
 */
static sai_status_t ctc_sai_stp_remove_stp_port(sai_object_id_t stp_port_id)
{
    sai_status_t  status = SAI_STATUS_SUCCESS;
    uint8 lchip;

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(stp_port_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = _ctc_sai_stp_remove_stp_port(stp_port_id);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to remove  stp port:%d\n", status);
    }
    return status;
}

/**
 * @brief Set the attribute of STP instance.
 *
 * @param[in] sai_stp_id Stp instance id
 * @param[in] attr attribute value
 * @return SAI_STATUS_SUCCESS if operation is successful otherwise a different
 *  error code is returned.
 */
sai_status_t ctc_sai_stp_set_stp_attribute(sai_object_id_t sai_stp_id, const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = sai_stp_id };
    sai_status_t  status = SAI_STATUS_SUCCESS;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_stp_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_STP,  stp_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to set stp attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}

/**
 * @brief Get the attribute of STP instance.
 *
 * @param[in] sai_stp_id stp instance id
 * @param[in] attr_count number of the attribute
 * @param[in] attr_list attribute value
 * @return SAI_STATUS_SUCCESS if operation is successful otherwise a different
 *  error code is returned.
 */
static sai_status_t ctc_sai_stp_get_stp_attribute( const sai_object_id_t sai_stp_id,
                                           uint32_t              attr_count,
                                           sai_attribute_t   *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = sai_stp_id
    }
    ;
    sai_status_t  status = SAI_STATUS_SUCCESS;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_stp_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_STP, loop, stp_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to get stp attr. status:%d, attr_id:%d\n", status, attr_list[loop].id);
    }
    return status;
}


sai_status_t ctc_sai_stp_set_stp_port_attribute(sai_object_id_t sai_stp_id, const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = sai_stp_id };
    sai_status_t  status = SAI_STATUS_SUCCESS;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_stp_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_STP_PORT,  stp_port_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to set stp port attr_id:%d, status:%d\n", attr->id,status);
    }
    return status;
}

static sai_status_t ctc_sai_stp_get_stp_port_attribute( const sai_object_id_t sai_stp_id,
                                           uint32_t              attr_count,
                                           sai_attribute_t   *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = sai_stp_id
    }
    ;
    sai_status_t  status = SAI_STATUS_SUCCESS;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_STP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_stp_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_STP_PORT, loop, stp_port_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to get stp port attr. status:%d, attr_id:%d\n", status, attr_list[loop].id);
    }
    return status;
}


/**
 * @brief Bulk stp ports creation.
 *
 * @param[in] switch_id SAI Switch object id
 * @param[in] object_count Number of objects to create
 * @param[in] attr_count List of attr_count. Caller passes the number
 *    of attribute for each object to create.
 * @param[in] attr_list List of attributes for every object.
 * @param[in] mode Bulk operation error handling mode.
 *
 * @param[out] object_id List of object ids returned
 * @param[out] object_statuses List of status for every object. Caller needs to allocate the buffer.
 *
 * @return #SAI_STATUS_SUCCESS on success when all objects are created or #SAI_STATUS_FAILURE when
 * any of the objects fails to create. When there is failure, Caller is expected to go through the
 * list of returned statuses to find out which fails and which succeeds.
 */
sai_status_t ctc_sai_stp_create_stp_ports(sai_object_id_t          switch_id,
                                   uint32_t                 object_count,
                                   const uint32_t          *attr_count,
                                   const sai_attribute_t  **attr_list,
                                   sai_bulk_op_error_mode_t mode,
                                   sai_object_id_t        *object_id,
                                   sai_status_t           *object_statuses)
{
    uint32 index = 0;
    sai_status_t  status = SAI_STATUS_SUCCESS;
    uint8 is_found_error = 0;
    uint8 lchip = 0 ;


    if (NULL == object_id || NULL == attr_count || NULL == attr_list || NULL == object_statuses || 0 == object_count)
    {
        CTC_SAI_LOG_ERROR(SAI_API_STP, " stp ports invalid parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    for (index = 0; index < object_count; index++)
    {
        status = _ctc_sai_stp_create_stp_port(&object_id[index], switch_id, attr_count[index], attr_list[index]);
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
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to create stp ports :%d\n", status);
    }
    return status;
}


/**
 * @brief Bulk stp ports removal.
 *
 * @param[in] object_count Number of objects to create
 * @param[in] object_id List of object ids
 * @param[in] type bulk operation type.
 * @param[out] object_statuses List of status for every object. Caller needs to allocate the buffer.
 *
 * @return #SAI_STATUS_SUCCESS on success when all objects are removed or #SAI_STATUS_FAILURE when
 * any of the objects fails to remove. When there is failure, Caller is expected to go through the
 * list of returned statuses to find out which fails and which succeeds.
 */
sai_status_t ctc_sai_stp_remove_stp_ports(uint32_t                 object_count,
                                   const sai_object_id_t   *object_id,
                                   sai_bulk_op_error_mode_t mode,
                                   sai_status_t           *object_statuses)
{

    uint32 index = 0;
    sai_status_t  status = SAI_STATUS_SUCCESS;
    uint8 is_found_error = 0;
    uint8 lchip = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(object_id[index], &lchip));
    CTC_SAI_DB_LOCK(lchip);
    for (index = 0; index < object_count; index++)
    {
        status = _ctc_sai_stp_remove_stp_port(object_id[index]);
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
        CTC_SAI_LOG_ERROR(SAI_API_STP, "Failed to remove stp ports:%d\n", status);
    }
    return status;
}

const sai_stp_api_t g_ctc_sai_stp_api =
{
    ctc_sai_stp_create_stp,
    ctc_sai_stp_remove_stp,
    ctc_sai_stp_set_stp_attribute,
    ctc_sai_stp_get_stp_attribute,
    ctc_sai_stp_create_stp_port,
    ctc_sai_stp_remove_stp_port,
    ctc_sai_stp_set_stp_port_attribute,
    ctc_sai_stp_get_stp_port_attribute,
    ctc_sai_stp_create_stp_ports,
    ctc_sai_stp_remove_stp_ports,
};

sai_status_t
ctc_sai_stp_api_init()
{
    ctc_sai_register_module_api(SAI_API_STP, (void*)&g_ctc_sai_stp_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_stp_db_init(uint8 lchip)
{
    sai_object_id_t    sai_stp_id = 0;
    sai_object_id_t        switch_id = 0;
    ctc_sai_db_wb_t wb_info;
    uint8 gchip = 0;
    
    ctcs_get_gchip_id(lchip, &gchip);
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_STP;
    wb_info.data_len = sizeof(ctc_sai_stp_info_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_stp_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_STP, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);
    switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32) gchip);
    CTC_SAI_ERROR_RETURN(ctc_sai_stp_create_stp(&sai_stp_id, switch_id, 0, NULL));
    return SAI_STATUS_SUCCESS;
}
