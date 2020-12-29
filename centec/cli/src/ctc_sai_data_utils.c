#include "saistatus.h"
#include "ctc_sai_data_utils.h"

bool ctc_sai_data_util_is_object_type_valid(sai_object_type_t object_type)
{
    return object_type > SAI_OBJECT_TYPE_NULL && object_type < SAI_OBJECT_TYPE_MAX;
}

ctc_sai_object_type_info_t* ctc_sai_data_utils_get_object_type_info(sai_object_type_t object_type)
{
    if (ctc_sai_data_util_is_object_type_valid(object_type))
    {
        return ctc_sai_metadata_all_object_type_infos[object_type];
    }

    return NULL;
}

bool ctc_sai_data_utils_is_object_type_oid(sai_object_type_t object_type)
{
    ctc_sai_object_type_info_t* oti = ctc_sai_data_utils_get_object_type_info(object_type);

    if (oti != NULL)
    {
        return oti->isobjectid;
    }

    return false;
}

ctc_sai_attr_metadata_t* ctc_sai_data_utils_get_attr_metadata(sai_object_type_t object_type, sai_attr_id_t attrid)
{
    uint32 index = 0;

    if (ctc_sai_data_util_is_object_type_valid(object_type))
    {
        ctc_sai_attr_metadata_t** md = ctc_sai_metadata_attr_by_object_type[object_type];

        for (; md[index] != NULL; index++)
        {
            if (md[index]->attrid == attrid)
            {
                return md[index];
            }
        }
    }

    return NULL;
}

ctc_sai_attr_metadata_t*
ctc_sai_data_utils_object_get_attr_by_name(sai_object_type_t object_type, char *attr_name)
{
    uint32 i = 0;
    ctc_sai_enum_metadata_t* enum_metadata = NULL;
    ctc_sai_attr_metadata_t** attr_metadata = NULL;

    if (!ctc_sai_data_util_is_object_type_valid(object_type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "OID type is invalid!");
        return NULL;
    }

    enum_metadata = ctc_sai_metadata_all_object_type_infos[object_type]->enummetadata;
    attr_metadata = ctc_sai_metadata_all_object_type_infos[object_type]->attrmetadata;
    for (i = 0; i < enum_metadata->valuescount; i++)
    {
        if (!sal_strncmp(attr_name, enum_metadata->valuesnames[i], sal_strlen(attr_name))
           && (sal_strlen(attr_name) == sal_strlen(enum_metadata->valuesnames[i])))
        {
            return attr_metadata[i];
        }
    }

    return NULL;
}

ctc_sai_attr_metadata_t*
ctc_sai_data_utils_object_get_attr_by_id(sai_object_type_t object_type, sai_attr_id_t id)
{
    uint32 i = 0;
    ctc_sai_enum_metadata_t* enum_metadata = NULL;
    ctc_sai_attr_metadata_t** attr_metadata = NULL;

    if (!ctc_sai_data_util_is_object_type_valid(object_type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "OID type is invalid!");
        return NULL;
    }

    enum_metadata = ctc_sai_metadata_all_object_type_infos[object_type]->enummetadata;
    attr_metadata = ctc_sai_metadata_all_object_type_infos[object_type]->attrmetadata;
    for (i = 0; i < enum_metadata->valuescount; i++)
    {
        if (enum_metadata->values[i] == id)
        {
            return attr_metadata[i];
        }
    }

    return NULL;
}

sai_status_t
ctc_sai_data_utils_object_set_attr(const ctc_sai_object_meta_key_t *meta_key, const sai_attribute_t* attr)
{
    if (!ctc_sai_data_util_is_object_type_valid(meta_key->objecttype))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "OID type is invalid!");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_metadata_all_object_type_infos[meta_key->objecttype]->set(meta_key, attr));

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_data_utils_object_get_attr(const ctc_sai_object_meta_key_t *meta_key, sai_attribute_t* attr)
{
    if (!ctc_sai_data_util_is_object_type_valid(meta_key->objecttype))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "OID type is invalid!");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_metadata_all_object_type_infos[meta_key->objecttype]->get(meta_key, 1, attr));

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_data_utils_attr_alloc_mem(ctc_sai_attr_value_type_t attr_value_type, sai_attribute_t* attr)
{
    if (CTC_SAI_ATTR_VALUE_TYPE_OBJECT_LIST == attr_value_type)
    {
        attr->value.objlist.list = (sai_object_id_t*)sal_malloc(sizeof(sai_object_id_t)*4096);
        if (NULL == attr->value.objlist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_BOOL_LIST == attr_value_type)
    {
        attr->value.boollist.list = (bool*)sal_malloc(sizeof(bool)*4096);
        if (NULL == attr->value.boollist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_UINT8_LIST == attr_value_type)
    {
        attr->value.u8list.list = (uint8_t*)sal_malloc(sizeof(uint8_t)*4096);
        if (NULL == attr->value.u8list.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_INT8_LIST == attr_value_type)
    {
        attr->value.s8list.list = (int8_t*)sal_malloc(sizeof(int8_t)*4096);
        if (NULL == attr->value.s8list.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_UINT16_LIST == attr_value_type)
    {
        attr->value.u16list.list = (uint16_t*)sal_malloc(sizeof(uint16_t)*4096);
        if (NULL == attr->value.u16list.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_INT16_LIST == attr_value_type)
    {
        attr->value.s16list.list = (int16_t*)sal_malloc(sizeof(int16_t)*4096);
        if (NULL == attr->value.s16list.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_UINT32_LIST == attr_value_type)
    {
        attr->value.u32list.list = (uint32_t*)sal_malloc(sizeof(uint32_t)*4096);
        if (NULL == attr->value.u32list.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_INT32_LIST == attr_value_type)
    {
        attr->value.s32list.list = (int32_t*)sal_malloc(sizeof(int32_t)*4096);
        if (NULL == attr->value.s32list.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_VLAN_LIST == attr_value_type)
    {
        attr->value.vlanlist.list = (sai_vlan_id_t*)sal_malloc(sizeof(sai_vlan_id_t)*4096);
        if (NULL == attr->value.vlanlist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_LIST == attr_value_type)
    {
        attr->value.aclfield.data.objlist.list = (sai_object_id_t*)sal_malloc(sizeof(sai_object_id_t)*4096);
        if (NULL == attr->value.aclfield.data.objlist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST == attr_value_type)
    {
        attr->value.aclfield.data.u8list.list = (uint8_t*)sal_malloc(sizeof(uint8_t)*4096);
        if (NULL == attr->value.aclfield.data.u8list.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }

        attr->value.aclfield.mask.u8list.list = (uint8_t*)sal_malloc(sizeof(uint8_t)*4096);
        if (NULL == attr->value.aclfield.mask.u8list.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
            sal_free(attr->value.aclfield.data.u8list.list);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_LIST == attr_value_type)
    {
        attr->value.aclaction.parameter.objlist.list = (sai_object_id_t*)sal_malloc(sizeof(sai_object_id_t)*4096);
        if (NULL == attr->value.aclaction.parameter.objlist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_PORT_EYE_VALUES_LIST == attr_value_type)
    {
        attr->value.porteyevalues.list = (sai_port_lane_eye_values_t*)sal_malloc(sizeof(sai_port_lane_eye_values_t)*4096);
        if (NULL == attr->value.porteyevalues.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG_LIST == attr_value_type)
    {
        attr->value.sysportconfiglist.list = (sai_system_port_config_t*)sal_malloc(sizeof(sai_system_port_config_t)*4096);
        if (NULL == attr->value.sysportconfiglist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_PORT_ERR_STATUS_LIST == attr_value_type)
    {
        attr->value.porterror.list = (sai_port_err_status_t*)sal_malloc(sizeof(sai_port_err_status_t)*4096);
        if (NULL == attr->value.porterror.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_TLV_LIST == attr_value_type)
    {
        attr->value.tlvlist.list = (sai_tlv_t*)sal_malloc(sizeof(sai_tlv_t)*4096);
        if (NULL == attr->value.tlvlist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_QOS_MAP_LIST == attr_value_type)
    {
        attr->value.qosmap.list = (sai_qos_map_t*)sal_malloc(sizeof(sai_qos_map_t)*4096);
        if (NULL == attr->value.qosmap.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_MAP_LIST == attr_value_type)
    {
        attr->value.maplist.list = (sai_map_t*)sal_malloc(sizeof(sai_map_t)*4096);
        if (NULL == attr->value.maplist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_ACL_RESOURCE_LIST == attr_value_type)
    {
        attr->value.aclresource.list = (sai_acl_resource_t*)sal_malloc(sizeof(sai_acl_resource_t)*4096);
        if (NULL == attr->value.aclresource.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_SEGMENT_LIST == attr_value_type)
    {
        attr->value.segmentlist.list = (sai_ip6_t*)sal_malloc(sizeof(sai_ip6_t)*4096);
        if (NULL == attr->value.segmentlist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS_LIST == attr_value_type)
    {
        attr->value.ipaddrlist.list = (sai_ip_address_t*)sal_malloc(sizeof(sai_ip_address_t)*4096);
        if (NULL == attr->value.ipaddrlist.list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "%s %d, out of memory\n", __FUNCTION__, __LINE__);
        }
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_data_utils_attr_free_mem(ctc_sai_attr_value_type_t attr_value_type, sai_attribute_t* attr)
{
    if (CTC_SAI_ATTR_VALUE_TYPE_OBJECT_LIST == attr_value_type)
    {
        if (NULL != attr->value.objlist.list)
        {
            sal_free(attr->value.objlist.list);
            attr->value.objlist.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_BOOL_LIST == attr_value_type)
    {
        if (NULL != attr->value.boollist.list)
        {
            sal_free(attr->value.boollist.list);
            attr->value.boollist.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_UINT8_LIST == attr_value_type)
    {
        if (NULL != attr->value.u8list.list)
        {
            sal_free(attr->value.u8list.list);
            attr->value.u8list.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_INT8_LIST == attr_value_type)
    {
        if (NULL != attr->value.s8list.list)
        {
            sal_free(attr->value.s8list.list);
            attr->value.s8list.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_UINT16_LIST == attr_value_type)
    {
        if (NULL != attr->value.u16list.list)
        {
            sal_free(attr->value.u16list.list);
            attr->value.u16list.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_INT16_LIST == attr_value_type)
    {
        if (NULL != attr->value.s16list.list)
        {
            sal_free(attr->value.s16list.list);
            attr->value.s16list.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_UINT32_LIST == attr_value_type)
    {
        if (NULL != attr->value.u32list.list)
        {
            sal_free(attr->value.u32list.list);
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_INT32_LIST == attr_value_type)
    {
        if (NULL != attr->value.s32list.list)
        {
            sal_free(attr->value.s32list.list);
            attr->value.s32list.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_LIST == attr_value_type)
    {
        if (NULL != attr->value.aclfield.data.objlist.list)
        {
            sal_free(attr->value.aclfield.data.objlist.list);
            attr->value.aclfield.data.objlist.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST == attr_value_type)
    {
        if (NULL != attr->value.aclfield.data.u8list.list)
        {
            sal_free(attr->value.aclfield.data.u8list.list);
            attr->value.aclfield.data.u8list.list = NULL;
        }
        if (NULL != attr->value.aclfield.mask.u8list.list)
        {
            sal_free(attr->value.aclfield.mask.u8list.list);
            attr->value.aclfield.mask.u8list.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_LIST == attr_value_type)
    {
        if (NULL != attr->value.aclaction.parameter.objlist.list)
        {
            sal_free(attr->value.aclaction.parameter.objlist.list);
            attr->value.aclaction.parameter.objlist.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_PORT_EYE_VALUES_LIST == attr_value_type)
    {
        if (NULL != attr->value.porteyevalues.list)
        {
            sal_free(attr->value.porteyevalues.list);
            attr->value.porteyevalues.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG_LIST == attr_value_type)
    {
        if (NULL != attr->value.sysportconfiglist.list)
        {
            sal_free(attr->value.sysportconfiglist.list);
            attr->value.sysportconfiglist.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_PORT_ERR_STATUS_LIST == attr_value_type)
    {
        if (NULL != attr->value.porterror.list)
        {
            sal_free(attr->value.porterror.list);
            attr->value.porterror.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_TLV_LIST == attr_value_type)
    {
        if (NULL != attr->value.tlvlist.list)
        {
            sal_free(attr->value.tlvlist.list);
            attr->value.tlvlist.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_VLAN_LIST == attr_value_type)
    {
        if (NULL != attr->value.vlanlist.list)
        {
            sal_free(attr->value.vlanlist.list);
            attr->value.vlanlist.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_QOS_MAP_LIST == attr_value_type)
    {
        if (NULL != attr->value.qosmap.list)
        {
            sal_free(attr->value.qosmap.list);
            attr->value.qosmap.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_MAP_LIST == attr_value_type)
    {
        if (NULL != attr->value.maplist.list)
        {
            sal_free(attr->value.maplist.list);
            attr->value.maplist.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_ACL_RESOURCE_LIST == attr_value_type)
    {
        if (NULL != attr->value.aclresource.list)
        {
            sal_free(attr->value.aclresource.list);
            attr->value.aclresource.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_SEGMENT_LIST == attr_value_type)
    {
        if (NULL != attr->value.segmentlist.list)
        {
            sal_free(attr->value.segmentlist.list);
            attr->value.segmentlist.list = NULL;
        }
    }
    else if (CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS_LIST == attr_value_type)
    {
        if (NULL != attr->value.ipaddrlist.list)
        {
            sal_free(attr->value.ipaddrlist.list);
            attr->value.ipaddrlist.list = NULL;
        }
    }

    return SAI_STATUS_SUCCESS;
}

