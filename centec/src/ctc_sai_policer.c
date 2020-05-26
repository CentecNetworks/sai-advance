
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_policer.h"
#include "ctc_sai_port.h"

#define CTC_SAI_POLICER_UNUSED_ATTR   0xFF


static sai_status_t
_ctc_sai_policer_map_attr_to_db(const sai_attribute_t* attr_list, uint32 attr_count, ctc_sai_policer_db_t* p_policer)
{
    sai_status_t status = 0;
    const sai_attribute_value_t *attr_value;
    uint32                   attr_index;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_METER_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->meter_type = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_MODE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->mode = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_COLOR_SOURCE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->color_source = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_CBS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->cbs = attr_value->u64;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_CBS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->cbs = attr_value->u64;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_CIR, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->cir = attr_value->u64;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_PBS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->pbs = attr_value->u64;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_PIR, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->pir = attr_value->u64;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_GREEN_PACKET_ACTION, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->action[SAI_PACKET_COLOR_GREEN] = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_YELLOW_PACKET_ACTION, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->action[SAI_PACKET_COLOR_YELLOW] = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_POLICER_ATTR_RED_PACKET_ACTION, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_policer->action[SAI_PACKET_COLOR_RED] = attr_value->u32;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_policer_db_map_policer(uint8 lchip, ctc_sai_policer_db_t* psai_policer, ctc_qos_policer_t* pctc_policer)
{
    uint8 ii = 0;

    if (psai_policer->meter_type == SAI_METER_TYPE_PACKETS)
    {
        pctc_policer->pps_en = 1;
        pctc_policer->policer.cbs = psai_policer->cbs;
        pctc_policer->policer.cir = psai_policer->cir;
        pctc_policer->policer.pbs = psai_policer->pbs;
        pctc_policer->policer.pir = psai_policer->pir;
    }
    else if (psai_policer->meter_type == SAI_METER_TYPE_BYTES)
    {
        pctc_policer->pps_en = 0;
        pctc_policer->policer.cbs = psai_policer->cbs * 8/1000;
        pctc_policer->policer.cir = psai_policer->cir * 8/1000;
        pctc_policer->policer.pbs = psai_policer->pbs * 8/1000;
        pctc_policer->policer.pir = psai_policer->pir * 8/1000;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Invalid meter type %d !\n", psai_policer->meter_type);
        return SAI_STATUS_NOT_SUPPORTED;
    }

    if (psai_policer->mode == SAI_POLICER_MODE_SR_TCM)
    {
        pctc_policer->policer.policer_mode = CTC_QOS_POLICER_MODE_RFC2697;
    }
    else if (psai_policer->mode == SAI_POLICER_MODE_TR_TCM)
    {
        pctc_policer->policer.policer_mode = CTC_QOS_POLICER_MODE_RFC4115;
    }
    else if (psai_policer->mode == SAI_POLICER_MODE_STORM_CONTROL)
    {
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Invalid policer mode %d !\n", psai_policer->mode);
        return SAI_STATUS_NOT_SUPPORTED;
    }
    if (psai_policer->color_source == SAI_POLICER_COLOR_SOURCE_BLIND)
    {
        pctc_policer->policer.is_color_aware = 0;
    }
    else
    {
        pctc_policer->policer.is_color_aware = 1;
    }

    for (ii = SAI_PACKET_COLOR_GREEN; ii <= SAI_PACKET_COLOR_RED; ii++)
    {
        if (psai_policer->action[ii] > SAI_PACKET_ACTION_FORWARD)
        {
            CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Not support packet action %d !\n", psai_policer->action[ii]);
            return SAI_STATUS_NOT_SUPPORTED;
        }
        if (psai_policer->action[ii] == SAI_PACKET_ACTION_DROP)
        {
            if (ctcs_get_chip_type(lchip) == CTC_CHIP_DUET2)
            {
                pctc_policer->action.flag |= (CTC_QOS_POLICER_ACTION_FLAG_DROP_GREEN << ii);
            }
            else if (ii == SAI_PACKET_COLOR_YELLOW)
            {
                pctc_policer->policer.drop_color = CTC_QOS_COLOR_YELLOW;
            }
            else
            {
                pctc_policer->policer.drop_color = CTC_QOS_COLOR_RED;
            }
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_policer_set_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t policer_id = key->key.object_id;
    ctc_sai_policer_db_t* p_policer_db = NULL;
    ctc_qos_policer_t  ctc_policer;
    uint8 lchip = 0;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, policer_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_POLICER)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    p_policer_db = ctc_sai_db_get_object_property(lchip, policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer DB not Found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    sal_memset(&ctc_policer, 0, sizeof(ctc_policer));
    _ctc_sai_policer_map_attr_to_db(attr, 1, p_policer_db);

    if (p_policer_db->mode == SAI_POLICER_MODE_STORM_CONTROL)
    {
        if (p_policer_db->id.port_id != CTC_SAI_POLICER_APPLY_DEFAULT)
        {
            sai_object_id_t sai_port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, p_policer_db->id.port_id);
            ctc_sai_port_db_t* p_port_db = ctc_sai_db_get_object_property(lchip, sai_port_id);
            if (NULL == p_port_db)
            {
                return SAI_STATUS_SUCCESS;
            }
            if (p_port_db->stmctl_flood_policer_id == ctc_object_id.value)
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_policer_port_set_stmctl(lchip,
                                                            p_policer_db->id.port_id,
                                                            p_port_db->stmctl_flood_policer_id,
                                                            CTC_SAI_STMCTL_TYPE_FLOOD,
                                                            TRUE));
            }
            if (p_port_db->stmctl_bc_policer_id == ctc_object_id.value)
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_policer_port_set_stmctl(lchip,
                                                            p_policer_db->id.port_id,
                                                            p_port_db->stmctl_bc_policer_id,
                                                            CTC_SAI_STMCTL_TYPE_BCAST,
                                                            TRUE));
            }
            if (p_port_db->stmctl_mc_policer_id == ctc_object_id.value)
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_policer_port_set_stmctl(lchip,
                                                            p_policer_db->id.port_id,
                                                            p_port_db->stmctl_mc_policer_id,
                                                            CTC_SAI_STMCTL_TYPE_MCAST,
                                                            TRUE));
            }
        }
    }
    else
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_policer_db_map_policer(lchip, p_policer_db, &ctc_policer));

        if (CTC_QOS_POLICER_TYPE_PORT == p_policer_db->type)
        {
            ctc_policer.dir = CTC_INGRESS;
            ctc_policer.enable = 1;
            ctc_policer.id.gport = p_policer_db->id.port_id;
            ctc_policer.type = CTC_QOS_POLICER_TYPE_PORT;

            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_policer(lchip, &ctc_policer));
        }
        else if (CTC_QOS_POLICER_TYPE_FLOW == p_policer_db->type)
        {
            ctc_policer.dir = CTC_INGRESS;
            ctc_policer.enable = 1;
            ctc_policer.id.policer_id = p_policer_db->id.entry_id;
            ctc_policer.type = CTC_QOS_POLICER_TYPE_FLOW;

            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_policer(lchip, &ctc_policer));
        }
        else if ((ctcs_get_chip_type(lchip) == CTC_CHIP_DUET2) && (CTC_QOS_POLICER_TYPE_COPP == p_policer_db->type))
        {
            ctc_policer.dir = CTC_INGRESS;
            ctc_policer.id.policer_id = ctc_object_id.value;
            ctc_policer.type = CTC_QOS_POLICER_TYPE_COPP;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_policer(lchip, &ctc_policer));
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_policer_get_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_object_id_t policer_id = key->key.object_id;
    ctc_sai_policer_db_t* p_policer_db = NULL;
    uint8 lchip = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(policer_id, &lchip));
    p_policer_db = ctc_sai_db_get_object_property(lchip, policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer DB not Found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    switch (attr->id)
    {
        case SAI_POLICER_ATTR_METER_TYPE:
            attr->value.u32 = p_policer_db->meter_type;
            break;

        case SAI_POLICER_ATTR_MODE:
            attr->value.u32 = p_policer_db->mode;
            break;

        case SAI_POLICER_ATTR_COLOR_SOURCE:
            attr->value.u32 = p_policer_db->color_source;
            break;

        case SAI_POLICER_ATTR_CBS:
            attr->value.u64 = p_policer_db->cbs;
            break;

        case SAI_POLICER_ATTR_CIR:
            attr->value.u64 = p_policer_db->cir;
            break;

        case SAI_POLICER_ATTR_PBS:
            attr->value.u64 = p_policer_db->pbs;
            break;

        case SAI_POLICER_ATTR_PIR:
            attr->value.u64 = p_policer_db->pir;
            break;

        case SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
            attr->value.u32 = p_policer_db->action[SAI_PACKET_COLOR_GREEN];
            break;

        case SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
            attr->value.u32 = p_policer_db->action[SAI_PACKET_COLOR_YELLOW];
            break;

        case SAI_POLICER_ATTR_RED_PACKET_ACTION:
            attr->value.u32 = p_policer_db->action[SAI_PACKET_COLOR_RED];
            break;

        default:
            CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer attribute not implement\n");
            return  SAI_STATUS_NOT_IMPLEMENTED;

    }

    return SAI_STATUS_SUCCESS;
}


static ctc_sai_attr_fn_entry_t  policer_attr_fn_entries[] =
{
        {SAI_POLICER_ATTR_METER_TYPE,
            _ctc_sai_policer_get_attr,
            NULL},
        {SAI_POLICER_ATTR_MODE,
            _ctc_sai_policer_get_attr,
            NULL},
        {SAI_POLICER_ATTR_COLOR_SOURCE,
            _ctc_sai_policer_get_attr,
            NULL},
        {SAI_POLICER_ATTR_CBS,
            _ctc_sai_policer_get_attr,
            _ctc_sai_policer_set_attr},
        {SAI_POLICER_ATTR_CIR,
            _ctc_sai_policer_get_attr,
            _ctc_sai_policer_set_attr},
        {SAI_POLICER_ATTR_PBS,
            _ctc_sai_policer_get_attr,
            _ctc_sai_policer_set_attr},
        {SAI_POLICER_ATTR_PIR,
            _ctc_sai_policer_get_attr,
            _ctc_sai_policer_set_attr},
        {SAI_POLICER_ATTR_GREEN_PACKET_ACTION,
            _ctc_sai_policer_get_attr,
            _ctc_sai_policer_set_attr},
        {SAI_POLICER_ATTR_YELLOW_PACKET_ACTION,
            _ctc_sai_policer_get_attr,
            _ctc_sai_policer_set_attr},
        {SAI_POLICER_ATTR_RED_PACKET_ACTION,
            _ctc_sai_policer_get_attr,
            _ctc_sai_policer_set_attr},
        {SAI_POLICER_ATTR_ENABLE_COUNTER_PACKET_ACTION_LIST,
            NULL,
            NULL},
        { CTC_SAI_FUNC_ATTR_END_ID,
          NULL,
          NULL }
};

static sai_status_t
_ctc_sai_policer_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t             policer_id  = bucket_data->oid;
    ctc_sai_policer_db_t*       p_db        = (ctc_sai_policer_db_t*)bucket_data->data;
    ctc_sai_dump_grep_param_t*  p_dump      = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file      = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt         = (uint32 *)(p_cb_data->value1);

    if (p_dump->key.key.object_id && (policer_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" 0x%-8x %-6d %-6d %-4d %-9s G%-d/Y%-d/R%-d %-10d %-10d %-10d %-10d\n",
                            *cnt,policer_id,p_db->id.port_id,p_db->meter_type,
                            p_db->type,p_db->mode,p_db->color_source?"AWARE":"BLIND",
                            p_db->action[0], p_db->action[1], p_db->action[2],
                            p_db->cir,p_db->cbs,p_db->pir,p_db->pbs);
    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________

sai_status_t
ctc_sai_policer_port_set_stmctl(uint8 lchip, uint32 gport, uint32 policer_id, ctc_sai_stmctl_type_t stm_type, bool enable)
{
    ctc_sai_policer_db_t* p_policer_db = NULL;
    ctc_security_stmctl_cfg_t ctc_stmctl;
    sai_object_id_t sai_policer_id;


    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    CTC_SAI_LOG_INFO(SAI_API_POLICER, "[PARA] gport:0x%x, policer_id:%u, enable:%d\n", gport, policer_id, enable?1:0);

    sal_memset(&ctc_stmctl, 0, sizeof(ctc_stmctl));

    sai_policer_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_POLICER, lchip, 0, 0, policer_id);
    p_policer_db = ctc_sai_db_get_object_property(lchip, sai_policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer DB not Found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_policer_db->mode != SAI_POLICER_MODE_STORM_CONTROL)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer mode not match %d!\n", p_policer_db->mode);
        return SAI_STATUS_INVALID_PARAMETER;
    }

    switch (stm_type)
    {
        case CTC_SAI_STMCTL_TYPE_FLOOD:
            ctc_stmctl.type = CTC_SECURITY_STORM_CTL_UNKNOWN_UCAST;
            break;
        case CTC_SAI_STMCTL_TYPE_BCAST:
            ctc_stmctl.type = CTC_SECURITY_STORM_CTL_BCAST;
            break;
        case CTC_SAI_STMCTL_TYPE_MCAST:
            ctc_stmctl.type = CTC_SECURITY_STORM_CTL_KNOWN_MCAST;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Invalid stormctl type %d!\n", stm_type);
            return SAI_STATUS_INVALID_PARAMETER;
    }

    if (enable)
    {
        if (gport == p_policer_db->id.port_id)
        {
        }
        else if (p_policer_db->id.port_id != CTC_SAI_POLICER_APPLY_DEFAULT)
        {
            CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Object in use 0x%x!\n", p_policer_db->id.port_id);
            return SAI_STATUS_OBJECT_IN_USE;
        }

        ctc_stmctl.gport = gport;
        ctc_stmctl.op = CTC_SECURITY_STORM_CTL_OP_PORT;
        ctc_stmctl.storm_en = 1;
        ctc_stmctl.mode = (p_policer_db->meter_type == SAI_METER_TYPE_PACKETS) ?
                   CTC_SECURITY_STORM_CTL_MODE_PPS : CTC_SECURITY_STORM_CTL_MODE_BPS;
        ctc_stmctl.threshold = p_policer_db->cir;

        CTC_SAI_CTC_ERROR_RETURN(ctcs_storm_ctl_set_cfg(lchip, &ctc_stmctl));
        if (stm_type == CTC_SAI_STMCTL_TYPE_FLOOD)
        {
            ctc_stmctl.type = CTC_SECURITY_STORM_CTL_UNKNOWN_MCAST;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_storm_ctl_set_cfg(lchip, &ctc_stmctl));
        }
        p_policer_db->id.port_id = gport;
    }
    else
    {
        if (CTC_SAI_POLICER_APPLY_DEFAULT == p_policer_db->id.port_id)
        {
            return SAI_STATUS_SUCCESS;
        }
        if (gport != p_policer_db->id.port_id)
        {
            CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Port not apply the policer!\n");
            return SAI_STATUS_INVALID_PARAMETER;
        }
        ctc_stmctl.gport = gport;
        ctc_stmctl.op = CTC_SECURITY_STORM_CTL_OP_PORT;
        ctc_stmctl.storm_en = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_storm_ctl_set_cfg(lchip, &ctc_stmctl));
        if (stm_type == CTC_SAI_STMCTL_TYPE_FLOOD)
        {
            ctc_stmctl.type = CTC_SECURITY_STORM_CTL_UNKNOWN_MCAST;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_storm_ctl_set_cfg(lchip, &ctc_stmctl));
        }
        p_policer_db->id.port_id = CTC_SAI_POLICER_APPLY_DEFAULT;
    }

    return SAI_STATUS_SUCCESS;
}


//policer_id is alloced by opf, not the object_id
sai_status_t
ctc_sai_policer_port_set_policer(uint8 lchip, uint32 gport, uint32 policer_id, bool enable)
{
    sai_object_id_t sai_policer_id;
    ctc_sai_policer_db_t* p_policer_db = NULL;
    ctc_qos_policer_t  ctc_policer;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    CTC_SAI_LOG_INFO(SAI_API_POLICER, "gport:0x%x  ctc_policer_id:0x%x OP:%s\n",gport, policer_id, enable?"SET":"UNSET");
    sal_memset(&ctc_policer, 0, sizeof(ctc_qos_policer_t));

    sai_policer_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_POLICER, lchip, 0, 0, policer_id);
    p_policer_db = ctc_sai_db_get_object_property(lchip, sai_policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer DB not Found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_policer_db->mode == SAI_POLICER_MODE_STORM_CONTROL)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer mode is stormctl!\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_policer.dir = CTC_INGRESS;
    ctc_policer.id.gport = gport;
    ctc_policer.type = CTC_QOS_POLICER_TYPE_PORT;
    if (enable)
    {
        if (gport == p_policer_db->id.port_id)
        {
            if (p_policer_db->type != CTC_QOS_POLICER_TYPE_PORT)
            {
                return SAI_STATUS_OBJECT_IN_USE;
            }
        }
        else if (CTC_SAI_POLICER_APPLY_DEFAULT != p_policer_db->id.port_id)
        {
            return SAI_STATUS_OBJECT_IN_USE;
        }

        CTC_SAI_ERROR_RETURN(_ctc_sai_policer_db_map_policer(lchip, p_policer_db, &ctc_policer));
        ctc_policer.enable = 1;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_policer(lchip, &ctc_policer));

        p_policer_db->id.port_id = gport;
        p_policer_db->type = CTC_QOS_POLICER_TYPE_PORT;
    }
    else
    {

        if (CTC_SAI_POLICER_APPLY_DEFAULT == p_policer_db->id.port_id)
        {
            return SAI_STATUS_SUCCESS;
        }
        if (gport != p_policer_db->id.port_id)
        {
            CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Port not apply the policer!\n");
            return SAI_STATUS_INVALID_PARAMETER;
        }

        ctc_policer.enable = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_policer(lchip, &ctc_policer));

        p_policer_db->id.port_id = CTC_SAI_POLICER_APPLY_DEFAULT;
        p_policer_db->type = CTC_QOS_POLICER_TYPE_MAX;
    }

    return SAI_STATUS_SUCCESS;
}

//policer_id is alloced by opf, not the object_id
sai_status_t
ctc_sai_policer_acl_set_policer(uint8 lchip, uint32 entry_id, uint32 policer_id, bool enable)
{
    sai_object_id_t sai_policer_id;
    ctc_sai_policer_db_t* p_policer_db = NULL;
    ctc_qos_policer_t  ctc_policer;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    CTC_SAI_LOG_INFO(SAI_API_POLICER, "entry_id:0x%x  ctc_policer_id:0x%x OP:%s\n",entry_id, policer_id, enable?"SET":"UNSET");
    sal_memset(&ctc_policer, 0, sizeof(ctc_qos_policer_t));

    sai_policer_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_POLICER, lchip, 0, 0, policer_id);
    p_policer_db = ctc_sai_db_get_object_property(lchip, sai_policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer DB not Found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_policer_db->mode == SAI_POLICER_MODE_STORM_CONTROL)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer mode is stormctl!\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_policer.dir = CTC_INGRESS;
    ctc_policer.id.policer_id = policer_id;
    ctc_policer.type = CTC_QOS_POLICER_TYPE_FLOW;
    if (enable)//attach policer on acl entry
    {
        if (entry_id == p_policer_db->id.entry_id)
        {
            if (p_policer_db->type != CTC_QOS_POLICER_TYPE_FLOW)
            {
                return SAI_STATUS_OBJECT_IN_USE;
            }
        }
        else if (CTC_SAI_POLICER_APPLY_DEFAULT != p_policer_db->id.entry_id)
        {
            return SAI_STATUS_OBJECT_IN_USE;
        }
        CTC_SAI_ERROR_RETURN(_ctc_sai_policer_db_map_policer(lchip, p_policer_db, &ctc_policer));
        ctc_policer.enable = 1;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_policer(lchip, &ctc_policer));
        p_policer_db->id.entry_id = entry_id;
        p_policer_db->type = CTC_QOS_POLICER_TYPE_FLOW;
    }
    else
    {
        if (CTC_SAI_POLICER_APPLY_DEFAULT == p_policer_db->id.entry_id)
        {
            return SAI_STATUS_SUCCESS;
        }
        if (entry_id != p_policer_db->id.entry_id)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        ctc_policer.enable = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_policer(lchip, &ctc_policer));
        p_policer_db->id.entry_id = CTC_SAI_POLICER_APPLY_DEFAULT;
        p_policer_db->type = CTC_QOS_POLICER_TYPE_MAX;
    }

    return SAI_STATUS_SUCCESS;
}

//policer_id is alloced by opf, not the object_id
sai_status_t
ctc_sai_policer_set_copp_policer(uint8 lchip, uint32 policer_id, bool enable)
{
    sai_object_id_t sai_policer_id;
    ctc_sai_policer_db_t* p_policer_db = NULL;
    ctc_qos_policer_t  ctc_policer;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    CTC_SAI_LOG_INFO(SAI_API_POLICER, "ctc_policer_id:0x%x OP:%s\n",policer_id, enable?"SET":"UNSET");
    sal_memset(&ctc_policer, 0, sizeof(ctc_qos_policer_t));

    sai_policer_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_POLICER, lchip, 0, 0, policer_id);
    p_policer_db = ctc_sai_db_get_object_property(lchip, sai_policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer DB not Found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_policer_db->mode == SAI_POLICER_MODE_STORM_CONTROL)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer mode is stormctl!\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_policer.dir = CTC_INGRESS;
    ctc_policer.id.policer_id = policer_id;
    ctc_policer.type = CTC_QOS_POLICER_TYPE_COPP;
    if (enable)//attach copp policer
    {
        if ((CTC_SAI_POLICER_APPLY_DEFAULT != p_policer_db->id.entry_id) || (p_policer_db->type != CTC_QOS_POLICER_TYPE_COPP))
        {
            return SAI_STATUS_OBJECT_IN_USE;
        }
        CTC_SAI_ERROR_RETURN(_ctc_sai_policer_db_map_policer(lchip, p_policer_db, &ctc_policer));
        ctc_policer.enable = 1;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_policer(lchip, &ctc_policer));
        p_policer_db->type = CTC_QOS_POLICER_TYPE_COPP;
    }
    else
    {
        if (p_policer_db->type != CTC_QOS_POLICER_TYPE_COPP)
        {
            CTC_SAI_LOG_ERROR(SAI_API_POLICER, "policer type isNot copp!\n");
            return SAI_STATUS_INVALID_PARAMETER;
        }
        ctc_policer.enable = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_policer(lchip, &ctc_policer));
        p_policer_db->id.entry_id = CTC_SAI_POLICER_APPLY_DEFAULT;
        p_policer_db->type = CTC_QOS_POLICER_TYPE_MAX;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_policer_revert_policer(uint8 lchip, uint32 policer_id)
{
    sai_object_id_t sai_policer_id;
    ctc_sai_policer_db_t* p_policer_db = NULL;

    sai_policer_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_POLICER, lchip, 0, 0, policer_id);
    p_policer_db = ctc_sai_db_get_object_property(lchip, sai_policer_id);
    if (NULL == p_policer_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    p_policer_db->id.entry_id = CTC_SAI_POLICER_APPLY_DEFAULT;
    p_policer_db->type = CTC_QOS_POLICER_TYPE_MAX;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_policer_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t policer_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, policer_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_POLICER, ctc_object_id.value));
    return SAI_STATUS_SUCCESS;
}


#define ________SAI_DUMP________

void
ctc_sai_policer_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI Policer MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_POLICER))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Policer");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_policer_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-10s %-6s %-6s %-4s %-9s %-8s %-10s %-10s %-10s %-10s\n", "No.","Policer_Oid","Used_Id","M_type","P_type","Mode","Color_src","Action","Cir","Cbs","Pir","Pbs");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_POLICER,
                                                (hash_traversal_fn)_ctc_sai_policer_dump_print_cb, (void*)(&sai_cb_data));
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}

#define ________SAI_API________

sai_status_t
ctc_sai_policer_create_policer_id(
        _Out_ sai_object_id_t *policer_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    sai_status_t status = 0;
    sai_object_id_t policer_oid;
    ctc_sai_policer_db_t* p_policer_db = NULL;
    uint32  ctc_policer_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    CTC_SAI_PTR_VALID_CHECK(policer_id);
    *policer_id = 0;

    sal_memset(&policer_oid, 0, sizeof(policer_oid));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    p_policer_db = (ctc_sai_policer_db_t*)mem_malloc(MEM_QUEUE_MODULE, sizeof(ctc_sai_policer_db_t));
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "No memory!\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error_0;
    }
    sal_memset(p_policer_db, 0, sizeof(ctc_sai_policer_db_t));

    /*default value for checking if the attribute set*/
    p_policer_db->meter_type    = CTC_SAI_POLICER_UNUSED_ATTR;
    p_policer_db->mode          = CTC_SAI_POLICER_UNUSED_ATTR;
    p_policer_db->color_source  = SAI_POLICER_COLOR_SOURCE_AWARE;
    p_policer_db->action[SAI_PACKET_COLOR_GREEN]  = SAI_PACKET_ACTION_FORWARD;
    p_policer_db->action[SAI_PACKET_COLOR_YELLOW] = SAI_PACKET_ACTION_FORWARD;
    p_policer_db->action[SAI_PACKET_COLOR_RED]    = SAI_PACKET_ACTION_FORWARD;
    p_policer_db->id.port_id  = CTC_SAI_POLICER_APPLY_DEFAULT;
    p_policer_db->type = CTC_QOS_POLICER_TYPE_MAX;

    _ctc_sai_policer_map_attr_to_db(attr_list, attr_count, p_policer_db);

    //opf alloc policer id
    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_POLICER, &ctc_policer_id);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Opf alloc id failed!\n");
        goto error_1;
    }
    policer_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_POLICER, lchip, 0, 0, ctc_policer_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, policer_oid, p_policer_db), status, error_2);
    *policer_id = policer_oid;

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_POLICER, ctc_policer_id);
error_1:
    mem_free(p_policer_db);
error_0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_policer_remove_policer_id(
        _In_ sai_object_id_t policer_id)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_policer_db_t* p_policer_db = NULL;
    sai_status_t status = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, policer_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_POLICER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Object Type isNot SAI_OBJECT_TYPE_POLICER!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    p_policer_db = ctc_sai_db_get_object_property(lchip, policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Policer DB not found!\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error_return;
    }
    if ((p_policer_db->id.port_id != CTC_SAI_POLICER_APPLY_DEFAULT) || (p_policer_db->type != CTC_QOS_POLICER_TYPE_MAX))
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Object Id in used!\n");
        status = SAI_STATUS_OBJECT_IN_USE;
        goto error_return;
    }
    mem_free(p_policer_db);
    ctc_sai_db_remove_object_property(lchip, policer_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_POLICER, ctc_object_id.value);

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_policer_set_policer_attribute(
        _In_ sai_object_id_t policer_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = policer_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    CTC_PTR_VALID_CHECK(attr);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, policer_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_POLICER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Object Type isNot SAI_OBJECT_TYPE_POLICER!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_POLICER,  policer_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Failed to set policer attr:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_policer_get_policer_attribute(
        _In_ sai_object_id_t policer_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key ={ .key.object_id = policer_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            loop = 0;
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    CTC_PTR_VALID_CHECK(attr_list);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, policer_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_POLICER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Object Type isNot SAI_OBJECT_TYPE_POLICER!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_POLICER, loop, policer_attr_fn_entries, &attr_list[loop]), status, error_return);
        loop++ ;
    }

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Failed to get policer attr:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_policer_get_stats(
        _In_ sai_object_id_t policer_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _Out_ uint64_t *counters)
{
    uint32         attr_idx    = 0;
    ctc_qos_policer_stats_t policer_stats;
    ctc_sai_policer_db_t         *p_policer_db = NULL;
    ctc_object_id_t ctc_object_id;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    sal_memset(&policer_stats, 0x0, sizeof(ctc_qos_policer_stats_t));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, policer_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_POLICER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Object Type isNot SAI_OBJECT_TYPE_POLICER!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_policer_db = ctc_sai_db_get_object_property(lchip, policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "DB not found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if ((SAI_POLICER_MODE_STORM_CONTROL == p_policer_db->mode)
        || (CTC_SAI_POLICER_APPLY_DEFAULT == p_policer_db->id.port_id))
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Error getting stats, Mode:%d!\n", p_policer_db->mode);
        return SAI_STATUS_NOT_IMPLEMENTED;
    }

    if (CTC_QOS_POLICER_TYPE_PORT == p_policer_db->type)
    {
        policer_stats.type = CTC_QOS_POLICER_TYPE_PORT;
        policer_stats.dir = CTC_INGRESS;
        policer_stats.id.gport = p_policer_db->id.port_id;
    }
    else
    {
        policer_stats.type = CTC_QOS_POLICER_TYPE_FLOW;
        policer_stats.dir = CTC_INGRESS;
        policer_stats.id.policer_id = p_policer_db->id.entry_id;
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_query_policer_stats(lchip, &policer_stats));

    for(attr_idx = 0; attr_idx < number_of_counters; attr_idx++)
    {
        switch(counter_ids[attr_idx])
        {
            case SAI_POLICER_STAT_PACKETS:
                counters[attr_idx] = policer_stats.stats.confirm_pkts + policer_stats.stats.exceed_pkts + policer_stats.stats.violate_pkts;
                break;
            case SAI_POLICER_STAT_ATTR_BYTES:
                counters[attr_idx] = policer_stats.stats.confirm_bytes + policer_stats.stats.exceed_bytes + policer_stats.stats.violate_bytes;
                break;
            case SAI_POLICER_STAT_GREEN_PACKETS:
                counters[attr_idx] = policer_stats.stats.confirm_pkts;
                break;
            case SAI_POLICER_STAT_GREEN_BYTES:
                counters[attr_idx] = policer_stats.stats.confirm_bytes;
                break;
            case SAI_POLICER_STAT_YELLOW_PACKETS:
                counters[attr_idx] = policer_stats.stats.exceed_pkts;
                break;
            case SAI_POLICER_STAT_YELLOW_BYTES:
                counters[attr_idx] = policer_stats.stats.exceed_bytes;
                break;
            case SAI_POLICER_STAT_RED_PACKETS:
                counters[attr_idx] = policer_stats.stats.violate_pkts;
                break;
            case SAI_POLICER_STAT_RED_BYTES:
                counters[attr_idx] = policer_stats.stats.violate_bytes;
                break;
            default:
                break;
        }
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_policer_get_stats_ext(
        _In_ sai_object_id_t policer_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _In_ sai_stats_mode_t mode,
        _Out_ uint64_t *counters)
{
    uint32         attr_idx    = 0;
    ctc_qos_policer_stats_t policer_stats;
    ctc_sai_policer_db_t         *p_policer_db = NULL;
    ctc_object_id_t ctc_object_id;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    CTC_SAI_MAX_VALUE_CHECK(mode, SAI_STATS_MODE_READ_AND_CLEAR);
    sal_memset(&policer_stats, 0x0, sizeof(ctc_qos_policer_stats_t));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, policer_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_POLICER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Object Type isNot SAI_OBJECT_TYPE_POLICER!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_policer_db = ctc_sai_db_get_object_property(lchip, policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "DB not found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if ((SAI_POLICER_MODE_STORM_CONTROL == p_policer_db->mode)
        || (CTC_SAI_POLICER_APPLY_DEFAULT == p_policer_db->id.port_id))
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Error getting stats, Mode:%d!\n", p_policer_db->mode);
        return SAI_STATUS_NOT_IMPLEMENTED;
    }

    if (CTC_QOS_POLICER_TYPE_PORT == p_policer_db->type)
    {
        policer_stats.type = CTC_QOS_POLICER_TYPE_PORT;
        policer_stats.dir = CTC_INGRESS;
        policer_stats.id.gport = p_policer_db->id.port_id;
    }
    else
    {
        policer_stats.type = CTC_QOS_POLICER_TYPE_FLOW;
        policer_stats.dir = CTC_INGRESS;
        policer_stats.id.policer_id = p_policer_db->id.entry_id;
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_query_policer_stats(lchip, &policer_stats));

    for(attr_idx = 0; attr_idx < number_of_counters; attr_idx++)
    {
        switch(counter_ids[attr_idx])
        {
            case SAI_POLICER_STAT_PACKETS:
                counters[attr_idx] = policer_stats.stats.confirm_pkts + policer_stats.stats.exceed_pkts + policer_stats.stats.violate_pkts;
                break;
            case SAI_POLICER_STAT_ATTR_BYTES:
                counters[attr_idx] = policer_stats.stats.confirm_bytes + policer_stats.stats.exceed_bytes + policer_stats.stats.violate_bytes;
                break;
            case SAI_POLICER_STAT_GREEN_PACKETS:
                counters[attr_idx] = policer_stats.stats.confirm_pkts;
                break;
            case SAI_POLICER_STAT_GREEN_BYTES:
                counters[attr_idx] = policer_stats.stats.confirm_bytes;
                break;
            case SAI_POLICER_STAT_YELLOW_PACKETS:
                counters[attr_idx] = policer_stats.stats.exceed_pkts;
                break;
            case SAI_POLICER_STAT_YELLOW_BYTES:
                counters[attr_idx] = policer_stats.stats.exceed_bytes;
                break;
            case SAI_POLICER_STAT_RED_PACKETS:
                counters[attr_idx] = policer_stats.stats.violate_pkts;
                break;
            case SAI_POLICER_STAT_RED_BYTES:
                counters[attr_idx] = policer_stats.stats.violate_bytes;
                break;
            default:
                break;
        }
    }

    if (SAI_STATS_MODE_READ_AND_CLEAR == mode)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_clear_policer_stats(lchip, &policer_stats));
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_policer_clear_stats(
        _In_ sai_object_id_t policer_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids)
{
    ctc_qos_policer_stats_t policer_stats;
    ctc_sai_policer_db_t         *p_policer_db = NULL;
    ctc_object_id_t ctc_object_id;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_POLICER);
    if (number_of_counters != 1)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    if ((NULL == counter_ids) || (counter_ids[0] != SAI_POLICER_STAT_PACKETS))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    sal_memset(&policer_stats, 0x0, sizeof(ctc_qos_policer_stats_t));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, policer_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_POLICER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Object Type isNot SAI_OBJECT_TYPE_POLICER!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_policer_db = ctc_sai_db_get_object_property(lchip, policer_id);
    if (NULL == p_policer_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "DB not found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if ((SAI_POLICER_MODE_STORM_CONTROL == p_policer_db->mode)
        || (CTC_SAI_POLICER_APPLY_DEFAULT == p_policer_db->id.port_id))
    {
        CTC_SAI_LOG_ERROR(SAI_API_POLICER, "Error getting stats, Mode:%d!\n", p_policer_db->mode);
        return SAI_STATUS_NOT_IMPLEMENTED;
    }

    if (CTC_QOS_POLICER_TYPE_PORT == p_policer_db->type)
    {
        policer_stats.type = CTC_QOS_POLICER_TYPE_PORT;
        policer_stats.dir = CTC_INGRESS;
        policer_stats.id.gport = p_policer_db->id.port_id;
    }
    else
    {
        policer_stats.type = CTC_QOS_POLICER_TYPE_FLOW;
        policer_stats.dir = CTC_INGRESS;
        policer_stats.id.policer_id = p_policer_db->id.entry_id;
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_clear_policer_stats(lchip, &policer_stats));
    return SAI_STATUS_SUCCESS;
}

sai_policer_api_t g_ctc_sai_policer_api = {
    ctc_sai_policer_create_policer_id,
    ctc_sai_policer_remove_policer_id,
    ctc_sai_policer_set_policer_attribute,
    ctc_sai_policer_get_policer_attribute,
    ctc_sai_policer_get_stats,
    ctc_sai_policer_get_stats_ext,
    ctc_sai_policer_clear_stats
};

sai_status_t
ctc_sai_policer_api_init()
{
    ctc_sai_register_module_api(SAI_API_POLICER, (void*)&g_ctc_sai_policer_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_policer_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_POLICER;
    wb_info.data_len = sizeof(ctc_sai_policer_db_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_policer_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_POLICER, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

