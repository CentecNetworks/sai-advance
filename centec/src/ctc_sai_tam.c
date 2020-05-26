/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_tam.h"

/*sdk include file*/
#include "ctcs_api.h"

static sai_status_t
_ctc_sai_tam_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_t* p_tam_info = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_ATTR_TELEMETRY_OBJECTS_LIST:
            break;
        case SAI_TAM_ATTR_EVENT_OBJECTS_LIST:
            break;
        case SAI_TAM_ATTR_TAM_BIND_POINT_TYPE_LIST:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_t* p_tam_info = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_ATTR_TELEMETRY_OBJECTS_LIST:
            break;
        case SAI_TAM_ATTR_EVENT_OBJECTS_LIST:
            break;
        case SAI_TAM_ATTR_TAM_BIND_POINT_TYPE_LIST:
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_math_func_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_math_func_t* p_math_func_info = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_math_func_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_math_func_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_MATH_FUNC_ATTR_TAM_TEL_MATH_FUNC_TYPE:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_math_func_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_math_func_t* p_math_func_info = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_math_func_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_math_func_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_MATH_FUNC_ATTR_TAM_TEL_MATH_FUNC_TYPE:
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_report_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_report_t* p_tam_report = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_report = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_report)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_REPORT_ATTR_TYPE:
            break;
        case SAI_TAM_REPORT_ATTR_HISTOGRAM_NUMBER_OF_BINS:
            break;
        case SAI_TAM_REPORT_ATTR_HISTOGRAM_BIN_BOUNDARY:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_report_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_report_t* p_tam_report = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_report = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_report)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_REPORT_ATTR_TYPE:
            break;
        case SAI_TAM_REPORT_ATTR_HISTOGRAM_NUMBER_OF_BINS:
            break;
        case SAI_TAM_REPORT_ATTR_HISTOGRAM_BIN_BOUNDARY:
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_event_threshold_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_event_threshold_t* p_tam_event_thre = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_event_thre = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_event_thre)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_EVENT_THRESHOLD_ATTR_HIGH_WATERMARK:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_LOW_WATERMARK:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_LATENCY:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_RATE:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_ABS_VALUE:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_UNIT:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_event_threshold_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_event_threshold_t* p_tam_event_thre = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_event_thre = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_event_thre)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_EVENT_THRESHOLD_ATTR_HIGH_WATERMARK:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_LOW_WATERMARK:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_LATENCY:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_RATE:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_ABS_VALUE:
            break;
        case SAI_TAM_EVENT_THRESHOLD_ATTR_UNIT:
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_tel_type_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_tel_type_t* p_tam_tel_type = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_tel_type = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_tel_type)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_TEL_TYPE_ATTR_TAM_TELEMETRY_TYPE:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_INGRESS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_EGRESS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_VIRTUAL_QUEUE_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_OUTPUT_QUEUE_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_MMU_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FABRIC_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FILTER_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_RESOURCE_UTILIZATION_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_FABRIC_Q:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_NE_ENABLE:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_DSCP_VALUE:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_MATH_FUNC:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_REPORT_ID:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_tel_type_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_tel_type_t* p_tam_tel_type = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_tel_type = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_tel_type)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_TEL_TYPE_ATTR_TAM_TELEMETRY_TYPE:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_INGRESS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_EGRESS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_VIRTUAL_QUEUE_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_OUTPUT_QUEUE_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_MMU_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FABRIC_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FILTER_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_RESOURCE_UTILIZATION_STATS:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_FABRIC_Q:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_NE_ENABLE:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_DSCP_VALUE:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_MATH_FUNC:
            break;
        case SAI_TAM_TEL_TYPE_ATTR_REPORT_ID:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_transport_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_transport_t* p_tam_transport = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_transport = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_transport)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_TRANSPORT_ATTR_TRANSPORT_TYPE:
            break;
        case SAI_TAM_TRANSPORT_ATTR_SRC_PORT:
            break;
        case SAI_TAM_TRANSPORT_ATTR_DST_PORT:
            break;
        case SAI_TAM_TRANSPORT_ATTR_TRANSPORT_AUTH_TYPE:
            break;
        case SAI_TAM_TRANSPORT_ATTR_MTU:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_transport_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_transport_t* p_tam_transport = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_transport = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_transport)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_TRANSPORT_ATTR_TRANSPORT_TYPE:
            break;
        case SAI_TAM_TRANSPORT_ATTR_SRC_PORT:
            break;
        case SAI_TAM_TRANSPORT_ATTR_DST_PORT:
            break;
        case SAI_TAM_TRANSPORT_ATTR_TRANSPORT_AUTH_TYPE:
            break;
        case SAI_TAM_TRANSPORT_ATTR_MTU:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_telemetry_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_telemetry_t* p_tam_transport = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_telemtry = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_telemtry)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_TELEMETRY_ATTR_TAM_TYPE_LIST:
            break;
        case SAI_TAM_TELEMETRY_ATTR_COLLECTOR_LIST:
            break;
        case SAI_TAM_TELEMETRY_ATTR_TAM_REPORTING_UNIT:
            break;
        case SAI_TAM_TELEMETRY_ATTR_REPORTING_INTERVAL:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_telemetry_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_telemetry_t* p_tam_telemtry = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_telemtry = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_telemtry)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_TELEMETRY_ATTR_TAM_TYPE_LIST:
            break;
        case SAI_TAM_TELEMETRY_ATTR_COLLECTOR_LIST:
            break;
        case SAI_TAM_TELEMETRY_ATTR_TAM_REPORTING_UNIT:
            break;
        case SAI_TAM_TELEMETRY_ATTR_REPORTING_INTERVAL:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_collector_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_collector_t* p_tam_collector = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_collector = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_collector)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_COLLECTOR_ATTR_SRC_IP:
            break;
        case SAI_TAM_COLLECTOR_ATTR_DST_IP:
            break;
        case SAI_TAM_COLLECTOR_ATTR_LOCALHOST:
            break;
        case SAI_TAM_COLLECTOR_ATTR_VIRTUAL_ROUTER_ID:
            break;
        case SAI_TAM_COLLECTOR_ATTR_TRUNCATE_SIZE:
            break;
        case SAI_TAM_COLLECTOR_ATTR_TRANSPORT:
            break;
        case SAI_TAM_COLLECTOR_ATTR_DSCP_VALUE:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_collector_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_collector_t* p_tam_collector = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_collector = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_collector)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_COLLECTOR_ATTR_SRC_IP:
            break;
        case SAI_TAM_COLLECTOR_ATTR_DST_IP:
            break;
        case SAI_TAM_COLLECTOR_ATTR_LOCALHOST:
            break;
        case SAI_TAM_COLLECTOR_ATTR_VIRTUAL_ROUTER_ID:
            break;
        case SAI_TAM_COLLECTOR_ATTR_TRUNCATE_SIZE:
            break;
        case SAI_TAM_COLLECTOR_ATTR_TRANSPORT:
            break;
        case SAI_TAM_COLLECTOR_ATTR_DSCP_VALUE:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_event_action_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_event_action_t* p_tam_event_action = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_event_action = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_event_action)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_EVENT_ACTION_ATTR_REPORT_TYPE:
            break;
        case SAI_TAM_EVENT_ACTION_ATTR_QOS_ACTION_TYPE:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_event_action_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_event_action_t* p_tam_event_action = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_event_action = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_event_action)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_EVENT_ACTION_ATTR_REPORT_TYPE:
            break;
        case SAI_TAM_EVENT_ACTION_ATTR_QOS_ACTION_TYPE:
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_event_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_event_t* p_tam_event = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_event = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_event)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_EVENT_ATTR_TYPE:
            break;
        case SAI_TAM_EVENT_ATTR_ACTION_LIST:
            break;
        case SAI_TAM_EVENT_ATTR_COLLECTOR_LIST:
            break;
        case SAI_TAM_EVENT_ATTR_THRESHOLD:
            break;
        case SAI_TAM_EVENT_ATTR_DSCP_VALUE:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static sai_status_t
_ctc_sai_tam_event_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    /*ctc_sai_tam_event_t* p_tam_event = NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_tam_event = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tam_event)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }*/

    switch (attr->id)
    {
        case SAI_TAM_EVENT_ATTR_TYPE:
            break;
        case SAI_TAM_EVENT_ATTR_ACTION_LIST:
            break;
        case SAI_TAM_EVENT_ATTR_COLLECTOR_LIST:
            break;
        case SAI_TAM_EVENT_ATTR_THRESHOLD:
            break;
        case SAI_TAM_EVENT_ATTR_DSCP_VALUE:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    return status;
}

static  ctc_sai_attr_fn_entry_t tam_attr_fn_entries[] = {
    {SAI_TAM_ATTR_TELEMETRY_OBJECTS_LIST,
     _ctc_sai_tam_get_attr,
     _ctc_sai_tam_set_attr},
    {SAI_TAM_ATTR_EVENT_OBJECTS_LIST,
     _ctc_sai_tam_get_attr,
     _ctc_sai_tam_set_attr},
    {SAI_TAM_ATTR_TAM_BIND_POINT_TYPE_LIST,
     _ctc_sai_tam_get_attr,
     _ctc_sai_tam_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
static  ctc_sai_attr_fn_entry_t math_func_attr_fn_entries[] = {
    {SAI_TAM_MATH_FUNC_ATTR_TAM_TEL_MATH_FUNC_TYPE,
     _ctc_sai_tam_math_func_get_attr,
     _ctc_sai_tam_math_func_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
static  ctc_sai_attr_fn_entry_t tam_report_attr_fn_entries[] = {
    {SAI_TAM_REPORT_ATTR_TYPE,
     _ctc_sai_tam_report_get_attr,
     _ctc_sai_tam_report_set_attr},
    {SAI_TAM_REPORT_ATTR_HISTOGRAM_NUMBER_OF_BINS,
     _ctc_sai_tam_report_get_attr,
     _ctc_sai_tam_report_set_attr},
    {SAI_TAM_REPORT_ATTR_HISTOGRAM_BIN_BOUNDARY,
     _ctc_sai_tam_report_get_attr,
     _ctc_sai_tam_report_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
static  ctc_sai_attr_fn_entry_t tam_event_threshold_attr_fn_entries[] = {
    {SAI_TAM_EVENT_THRESHOLD_ATTR_HIGH_WATERMARK,
     _ctc_sai_tam_event_threshold_get_attr,
     _ctc_sai_tam_event_threshold_set_attr},
    {SAI_TAM_EVENT_THRESHOLD_ATTR_LOW_WATERMARK,
     _ctc_sai_tam_event_threshold_get_attr,
     _ctc_sai_tam_event_threshold_set_attr},
    {SAI_TAM_EVENT_THRESHOLD_ATTR_LATENCY,
     _ctc_sai_tam_event_threshold_get_attr,
     _ctc_sai_tam_event_threshold_set_attr},
    {SAI_TAM_EVENT_THRESHOLD_ATTR_RATE,
     _ctc_sai_tam_event_threshold_get_attr,
     _ctc_sai_tam_event_threshold_set_attr},
    {SAI_TAM_EVENT_THRESHOLD_ATTR_ABS_VALUE,
     _ctc_sai_tam_event_threshold_get_attr,
     _ctc_sai_tam_event_threshold_set_attr},
    {SAI_TAM_EVENT_THRESHOLD_ATTR_UNIT,
     _ctc_sai_tam_event_threshold_get_attr,
     _ctc_sai_tam_event_threshold_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
static  ctc_sai_attr_fn_entry_t tam_tel_type_attr_fn_entries[] = {
    {SAI_TAM_TEL_TYPE_ATTR_TAM_TELEMETRY_TYPE,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_INGRESS,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_EGRESS,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_VIRTUAL_QUEUE_STATS,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_OUTPUT_QUEUE_STATS,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_MMU_STATS,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FABRIC_STATS,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FILTER_STATS,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_RESOURCE_UTILIZATION_STATS,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_FABRIC_Q,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_NE_ENABLE,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_DSCP_VALUE,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_MATH_FUNC,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {SAI_TAM_TEL_TYPE_ATTR_REPORT_ID,
     _ctc_sai_tam_tel_type_get_attr,
     _ctc_sai_tam_tel_type_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
static  ctc_sai_attr_fn_entry_t tam_transport_attr_fn_entries[] = {
    {SAI_TAM_TRANSPORT_ATTR_TRANSPORT_TYPE,
     _ctc_sai_tam_transport_get_attr,
     _ctc_sai_tam_transport_set_attr},
    {SAI_TAM_TRANSPORT_ATTR_SRC_PORT,
     _ctc_sai_tam_transport_get_attr,
     _ctc_sai_tam_transport_set_attr},
    {SAI_TAM_TRANSPORT_ATTR_DST_PORT,
     _ctc_sai_tam_transport_get_attr,
     _ctc_sai_tam_transport_set_attr},
    {SAI_TAM_TRANSPORT_ATTR_TRANSPORT_AUTH_TYPE,
     _ctc_sai_tam_transport_get_attr,
     _ctc_sai_tam_transport_set_attr},
    {SAI_TAM_TRANSPORT_ATTR_MTU,
     _ctc_sai_tam_transport_get_attr,
     _ctc_sai_tam_transport_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
static  ctc_sai_attr_fn_entry_t tam_telemetry_attr_fn_entries[] = {
    {SAI_TAM_TELEMETRY_ATTR_TAM_TYPE_LIST,
     _ctc_sai_tam_telemetry_get_attr,
     _ctc_sai_tam_telemetry_set_attr},
    {SAI_TAM_TELEMETRY_ATTR_COLLECTOR_LIST,
     _ctc_sai_tam_telemetry_get_attr,
     _ctc_sai_tam_telemetry_set_attr},
    {SAI_TAM_TELEMETRY_ATTR_TAM_REPORTING_UNIT,
     _ctc_sai_tam_telemetry_get_attr,
     _ctc_sai_tam_telemetry_set_attr},
    {SAI_TAM_TELEMETRY_ATTR_REPORTING_INTERVAL,
     _ctc_sai_tam_telemetry_get_attr,
     _ctc_sai_tam_telemetry_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
static  ctc_sai_attr_fn_entry_t tam_collector_attr_fn_entries[] = {
    {SAI_TAM_COLLECTOR_ATTR_SRC_IP,
     _ctc_sai_tam_collector_get_attr,
     _ctc_sai_tam_collector_set_attr},
    {SAI_TAM_COLLECTOR_ATTR_DST_IP,
     _ctc_sai_tam_collector_get_attr,
     _ctc_sai_tam_collector_set_attr},
    {SAI_TAM_COLLECTOR_ATTR_LOCALHOST,
     _ctc_sai_tam_collector_get_attr,
     _ctc_sai_tam_collector_set_attr},
    {SAI_TAM_COLLECTOR_ATTR_VIRTUAL_ROUTER_ID,
     _ctc_sai_tam_collector_get_attr,
     _ctc_sai_tam_collector_set_attr},
    {SAI_TAM_COLLECTOR_ATTR_TRUNCATE_SIZE,
     _ctc_sai_tam_collector_get_attr,
     _ctc_sai_tam_collector_set_attr},
    {SAI_TAM_COLLECTOR_ATTR_TRANSPORT,
     _ctc_sai_tam_collector_get_attr,
     _ctc_sai_tam_collector_set_attr},
    {SAI_TAM_COLLECTOR_ATTR_DSCP_VALUE,
     _ctc_sai_tam_collector_get_attr,
     _ctc_sai_tam_collector_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
static  ctc_sai_attr_fn_entry_t tam_event_action_attr_fn_entries[] = {
    {SAI_TAM_EVENT_ACTION_ATTR_REPORT_TYPE,
     _ctc_sai_tam_event_action_get_attr,
     _ctc_sai_tam_event_action_set_attr},
    {SAI_TAM_EVENT_ACTION_ATTR_QOS_ACTION_TYPE,
     _ctc_sai_tam_event_action_get_attr,
     _ctc_sai_tam_event_action_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
static  ctc_sai_attr_fn_entry_t tam_event_attr_fn_entries[] = {
    {SAI_TAM_EVENT_ATTR_TYPE,
     _ctc_sai_tam_event_get_attr,
     _ctc_sai_tam_event_set_attr},
    {SAI_TAM_EVENT_ATTR_ACTION_LIST,
     _ctc_sai_tam_event_get_attr,
     _ctc_sai_tam_event_set_attr},
    {SAI_TAM_EVENT_ATTR_COLLECTOR_LIST,
     _ctc_sai_tam_event_get_attr,
     _ctc_sai_tam_event_set_attr},
    {SAI_TAM_EVENT_ATTR_THRESHOLD,
     _ctc_sai_tam_event_get_attr,
     _ctc_sai_tam_event_set_attr},
    {SAI_TAM_EVENT_ATTR_DSCP_VALUE,
     _ctc_sai_tam_event_get_attr,
     _ctc_sai_tam_event_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
#define ________INTERNAL_API________


#define ________SAI_API________
static sai_status_t
ctc_sai_tam_create_tam(sai_object_id_t *tam_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam(sai_object_id_t tam_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_attribute(sai_object_id_t tam_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM,  tam_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_attribute(sai_object_id_t tam_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM, loop, tam_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_create_tam_math_func(sai_object_id_t *tam_math_func_id, sai_object_id_t switch_id,
                                                                                    uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam_math_func(sai_object_id_t tam_math_func_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_math_func_attribute(sai_object_id_t tam_math_func_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_math_func_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_math_func_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_MATH_FUNC,  math_func_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_math_func_attribute(sai_object_id_t tam_math_func_id, uint32_t attr_count,
                                                                                                       sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_math_func_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_math_func_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_MATH_FUNC, loop, math_func_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_create_tam_report(sai_object_id_t *tam_report_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam_report(sai_object_id_t tam_report_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_report_attribute(sai_object_id_t tam_report_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_report_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_report_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_REPORT,  tam_report_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_report_attribute(sai_object_id_t tam_report_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_report_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_report_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_REPORT, loop, tam_report_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_create_tam_event_threshold(sai_object_id_t *tam_event_threshold_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam_event_threshold(sai_object_id_t tam_event_threshold_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_event_threshold_attribute(sai_object_id_t tam_event_threshold_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_event_threshold_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_event_threshold_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_EVENT_THRESHOLD,  tam_event_threshold_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_event_threshold_attribute(sai_object_id_t tam_event_threshold_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_event_threshold_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_event_threshold_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_EVENT_THRESHOLD, loop, tam_event_threshold_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_create_tam_tel_type(sai_object_id_t *tam_tel_type_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam_tel_type(sai_object_id_t tam_tel_type_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_tel_type_attribute(sai_object_id_t tam_tel_type_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_tel_type_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_tel_type_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_TEL_TYPE,  tam_tel_type_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_tel_type_attribute(sai_object_id_t tam_tel_type_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_tel_type_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_tel_type_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_TEL_TYPE, loop, tam_tel_type_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_create_tam_transport(sai_object_id_t *tam_transport_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam_transport(sai_object_id_t tam_transport_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_transport_attribute(sai_object_id_t tam_transport_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_transport_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_transport_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_TRANSPORT,  tam_transport_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_transport_attribute(sai_object_id_t tam_transport_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_transport_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_transport_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_TRANSPORT, loop, tam_transport_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_create_tam_telemetry(sai_object_id_t *tam_telemetry_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam_telemetry(sai_object_id_t tam_telemetry_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_telemetry_attribute(sai_object_id_t tam_telemetry_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_telemetry_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_telemetry_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_TRANSPORT,  tam_telemetry_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_telemetry_attribute(sai_object_id_t tam_telemetry_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_telemetry_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_telemetry_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_TELEMETRY, loop, tam_telemetry_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_create_tam_collector(sai_object_id_t *tam_collector_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam_collector(sai_object_id_t tam_collector_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_collector_attribute(sai_object_id_t tam_collector_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_collector_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_collector_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_COLLECTOR,  tam_collector_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_collector_attribute(sai_object_id_t tam_collector_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_collector_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_collector_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_COLLECTOR, loop, tam_collector_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_create_tam_event_action(sai_object_id_t *tam_event_action_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam_event_action(sai_object_id_t tam_event_action_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_event_action_attribute(sai_object_id_t tam_event_action_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_event_action_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_event_action_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_EVENT_ACTION,  tam_event_action_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_event_action_attribute(sai_object_id_t tam_event_action_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_event_action_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_event_action_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_EVENT_ACTION, loop, tam_event_action_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_create_tam_event(sai_object_id_t *tam_event_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_remove_tam_event(sai_object_id_t tam_event_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    return status;
}

static sai_status_t
ctc_sai_tam_set_tam_event_attribute(sai_object_id_t tam_event_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_event_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_event_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_EVENT,  tam_event_attr_fn_entries, attr), status, out);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tam_get_tam_event_attribute(sai_object_id_t tam_event_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tam_event_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_TAM);
    key.key.object_id = tam_event_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_TAM_EVENT, loop, tam_event_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_tam_api_t ctc_sai_tam_api = {
    ctc_sai_tam_create_tam,
    ctc_sai_tam_remove_tam,
    ctc_sai_tam_set_tam_attribute,
    ctc_sai_tam_get_tam_attribute,
    ctc_sai_tam_create_tam_math_func,
    ctc_sai_tam_remove_tam_math_func,
    ctc_sai_tam_set_tam_math_func_attribute,
    ctc_sai_tam_get_tam_math_func_attribute,
    ctc_sai_tam_create_tam_report,
    ctc_sai_tam_remove_tam_report,
    ctc_sai_tam_set_tam_report_attribute,
    ctc_sai_tam_get_tam_report_attribute,
    ctc_sai_tam_create_tam_event_threshold,
    ctc_sai_tam_remove_tam_event_threshold,
    ctc_sai_tam_set_tam_event_threshold_attribute,
    ctc_sai_tam_get_tam_event_threshold_attribute,
    ctc_sai_tam_create_tam_tel_type,
    ctc_sai_tam_remove_tam_tel_type,
    ctc_sai_tam_set_tam_tel_type_attribute,
    ctc_sai_tam_get_tam_tel_type_attribute,
    ctc_sai_tam_create_tam_transport,
    ctc_sai_tam_remove_tam_transport,
    ctc_sai_tam_set_tam_transport_attribute,
    ctc_sai_tam_get_tam_transport_attribute,
    ctc_sai_tam_create_tam_telemetry,
    ctc_sai_tam_remove_tam_telemetry,
    ctc_sai_tam_set_tam_telemetry_attribute,
    ctc_sai_tam_get_tam_telemetry_attribute,
    ctc_sai_tam_create_tam_collector,
    ctc_sai_tam_remove_tam_collector,
    ctc_sai_tam_set_tam_collector_attribute,
    ctc_sai_tam_get_tam_collector_attribute,
    ctc_sai_tam_create_tam_event_action,
    ctc_sai_tam_remove_tam_event_action,
    ctc_sai_tam_set_tam_event_action_attribute,
    ctc_sai_tam_get_tam_event_action_attribute,
    ctc_sai_tam_create_tam_event,
    ctc_sai_tam_remove_tam_event,
    ctc_sai_tam_set_tam_event_attribute,
    ctc_sai_tam_get_tam_event_attribute,
};

sai_status_t
ctc_sai_tam_api_init()
{
    ctc_sai_register_module_api(SAI_API_TAM, (void*)&ctc_sai_tam_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_tam_db_init(uint8 lchip)
{
    /*ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_TAM;
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;
    wb_info.wb_reload_cb1 = NULL;
    wb_info.data_len = sizeof(ctc_sai_tam_t);
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TAM, (void*)(&wb_info));
    wb_info.data_len = sizeof(ctc_sai_math_func_t);
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TAM_MATH_FUNC, (void*)(&wb_info));
    wb_info.data_len = sizeof(ctc_sai_event_threshold_t);
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TAM_EVENT_THRESHOLD, (void*)(&wb_info));
    wb_info.data_len = sizeof(ctc_sai_tel_type_t);
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TAM_TEL_TYPE, (void*)(&wb_info));
    wb_info.data_len = sizeof(ctc_sai_transport_t);
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TAM_TRANSPORT, (void*)(&wb_info));
    wb_info.data_len = sizeof(ctc_sai_telemetry_t);
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TAM_TELEMETRY, (void*)(&wb_info));
    wb_info.data_len = sizeof(ctc_sai_collector_t);
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TAM_COLLECTOR, (void*)(&wb_info));
    wb_info.data_len = sizeof(ctc_sai_event_action_t);
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TAM_EVENT_ACTION, (void*)(&wb_info));
    wb_info.data_len = sizeof(ctc_sai_event_t);
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TAM_EVENT, (void*)(&wb_info));*/
    return SAI_STATUS_SUCCESS;
}

