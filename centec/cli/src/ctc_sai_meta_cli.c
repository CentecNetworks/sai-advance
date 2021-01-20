#include "ctc_sai_meta_db.h"
#include "ctc_sai_data_utils.h"
#include "ctc_sai_data_ser.h"
#include "ctc_sai_meta_cli.h"
#include "ctc_error.h"
#include "ctc_cli.h"
#include "ctc_cli_common.h"

sai_api_query_fn ctc_sai_api_query_fn;
sai_apis_t apis;
char buf[1048576] = {0};

void ctc_sal_cli_out(char* buf)
{
    char* str = buf;
    char* line = NULL;

    do
    {
        line = sal_strchr(str, '\n');
        if (NULL != line)
        {
            *line = '\0';
            ctc_cli_out("%s\n", str);
            str = line + 1;
        }
    } while(NULL != line);

    return;
}

CTC_CLI(cli_sai_data_get_obj,
        cli_sai_data_get_obj_cmd,
        "sai get OID ATTR",
        "sai cmd",
        "sai get cmd",
        "sai object oid",
        "sai object attribute")
{
    int32 ret = 0;
    sai_object_id_t oid = 0;
    sai_attribute_t sai_attribute;
    ctc_sai_object_meta_key_t meta_key;
    ctc_object_id_t ctc_object_id = {0};
    ctc_sai_attr_metadata_t* attr_metadata = NULL;

    sal_memset(&meta_key, 0, sizeof(ctc_sai_object_meta_key_t));
    sal_memset(buf, 0, sizeof(buf));

    CTC_CLI_GET_UINT64("OID", oid, argv[0]);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, oid, &ctc_object_id);
    if (!ctc_sai_is_object_type_valid(ctc_object_id.type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "OID type is invalid!");
        return CLI_ERROR;
    }

    attr_metadata = ctc_sai_data_utils_object_get_attr_by_name(ctc_object_id.type, argv[1]);
    if (NULL == attr_metadata)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "ATTR name is invalid!");
        return CLI_ERROR;
    }
    ret = ctc_sai_data_utils_attr_alloc_mem(attr_metadata->attrvaluetype, &sai_attribute);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Fail alloc attr memory!");
        return CLI_ERROR;
    }

    meta_key.objecttype = ctc_object_id.type;
    meta_key.objectkey.key.object_id = oid;

    sai_attribute.id = attr_metadata->attrid;
    ret = ctc_sai_data_utils_object_get_attr(&meta_key, &sai_attribute);
    if (ret != SAI_STATUS_SUCCESS)
    {
        return CLI_ERROR;
    }
    sai_serialize_attribute(buf, attr_metadata, &sai_attribute);
    ctc_sal_cli_out(buf);

    ctc_sai_data_utils_attr_free_mem(attr_metadata->attrvaluetype, &sai_attribute);

    return CLI_SUCCESS;
}

CTC_CLI(cli_sai_data_get_entry,
        cli_sai_data_get_entry_cmd,
        "sai get (fdb FDB_KEY|neighbor NEIGHBOR_KEY|route ROUTE_KEY|mcast-fdb MCAST_FDB_KEY |l2mc L2MC_KEY|ipmc IPMC_KEY|inseg INSEG_KEY|nat NAT_KEY) ATTR",
        "sai cmd",
        "sai get cmd",
        "fdb entry",
        "[switch_id:value,mac_address:xx:xx:xx:xx:xx:xx,bv_id:oid]",
        "neighbor entry",
        "[switch_id:value,rif_id:oid,ip_address:value]",
        "route entry",
        "[switch_id:value,vr_id:oid,destination:value/length]",
        "mcast_fdb entry",
        "[switch_id:value,mac_address:xx:xx:xx:xx:xx:xx,bv_id:oid]",
        "l2mc entry",
        "[switch_id:value,bv_id:oid,type:sai_l2mc_entry_type,destination:value/length,source:value/length]",
        "ipmc entry",
        "[switch_id:value,vr_id:oid,type:sai_ipmc_entry_type,destination:value/length,source:value/length]",
        "inseg entry",
        "[switch_id:value,label:value]",
        "nat entry",
        "[switch_id:value,vr_id:oid,type:sai_nat_type,data:[key:[src_ip:value,dst_ip:value,proto:value,l4_src_port:value,l4_dst_port:value],\n                                                        mask:[src_ip:value,dst_ip:value,proto:value,l4_src_port:value,l4_dst_port:value]]",
        "sai entry attribute")
{
    int32 ret = 0;
    sai_attribute_t sai_attribute;
    sai_object_type_t obj_type = 0;
    ctc_sai_object_meta_key_t meta_key;
    sai_object_key_entry_t object_key_entry;
    ctc_sai_attr_metadata_t* attr_metadata = NULL;

    sal_memset(&meta_key, 0, sizeof(ctc_sai_object_meta_key_t));
    sal_memset(buf, 0, sizeof(buf));

    if (CTC_CLI_STR_EQUAL_ENHANCE("fdb", 0))
    {
        obj_type = SAI_OBJECT_TYPE_FDB_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("neighbor", 0))
    {
        obj_type = SAI_OBJECT_TYPE_NEIGHBOR_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("route", 0))
    {
        obj_type = SAI_OBJECT_TYPE_ROUTE_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("mcast_fdb", 0))
    {
        obj_type = SAI_OBJECT_TYPE_MCAST_FDB_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("l2mc", 0))
    {
        obj_type = SAI_OBJECT_TYPE_L2MC_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("ipmc", 0))
    {
        obj_type = SAI_OBJECT_TYPE_IPMC_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("inseg", 0))
    {
        obj_type = SAI_OBJECT_TYPE_INSEG_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("nat", 0))
    {
        obj_type = SAI_OBJECT_TYPE_NAT_ENTRY;
    }
    sai_deserialize_object_key_entry(argv[1], obj_type, &object_key_entry);

    attr_metadata = ctc_sai_data_utils_object_get_attr_by_name(obj_type, argv[2]);
    if (NULL == attr_metadata)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "ATTR name is invalid!");
        return CLI_ERROR;
    }
    ret = ctc_sai_data_utils_attr_alloc_mem(attr_metadata->attrvaluetype, &sai_attribute);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Fail alloc attr memory!");
        return CLI_ERROR;
    }

    meta_key.objecttype = obj_type;
    sal_memcpy(&meta_key.objectkey.key, &object_key_entry, sizeof(sai_object_key_entry_t));

    sai_attribute.id = attr_metadata->attrid;
    ret = ctc_sai_data_utils_object_get_attr(&meta_key, &sai_attribute);
    if (ret != SAI_STATUS_SUCCESS)
    {
        return CLI_ERROR;
    }
    sai_serialize_attribute(buf, attr_metadata, &sai_attribute);
    ctc_sal_cli_out(buf);

    ctc_sai_data_utils_attr_free_mem(attr_metadata->attrvaluetype, &sai_attribute);

    return CLI_SUCCESS;
}

CTC_CLI(cli_sai_data_set_obj,
        cli_sai_data_set_obj_cmd,
        "sai set OID ATTR EXPR",
        "sai cmd",
        "sai set cmd",
        "sai object oid",
        "sai object attribute",
        "sai value expression")
{
    int32 ret = 0;
    sai_object_id_t oid = 0;
    sai_attribute_t sai_attribute;
    ctc_sai_object_meta_key_t meta_key;
    ctc_object_id_t ctc_object_id = {0};
    ctc_sai_attr_metadata_t* attr_metadata = NULL;

    sal_memset(&meta_key, 0, sizeof(ctc_sai_object_meta_key_t));
    sal_memset(buf, 0, sizeof(buf));

    CTC_CLI_GET_UINT64("OID", oid, argv[0]);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, oid, &ctc_object_id);
    if (!ctc_sai_is_object_type_valid(ctc_object_id.type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "OID type is invalid!");
        return CLI_ERROR;
    }

    attr_metadata = ctc_sai_data_utils_object_get_attr_by_name(ctc_object_id.type, argv[1]);
    if (NULL == attr_metadata)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "ATTR name is invalid!");
        return CLI_ERROR;
    }
    sai_attribute.id = attr_metadata->attrid;
    ret = ctc_sai_data_utils_attr_alloc_mem(attr_metadata->attrvaluetype, &sai_attribute);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Fail alloc attr memory!");
        return CLI_ERROR;
    }

    meta_key.objecttype = ctc_object_id.type;
    meta_key.objectkey.key.object_id = oid;

    sal_strncpy(buf, argv[2], sal_strlen(argv[2]));
    sai_deserialize_attribute(buf, attr_metadata, &sai_attribute);
    ret = ctc_sai_data_utils_object_set_attr(&meta_key, &sai_attribute);
    if (ret != SAI_STATUS_SUCCESS)
    {
        return CLI_ERROR;
    }
    ctc_sai_data_utils_attr_free_mem(attr_metadata->attrvaluetype, &sai_attribute);

    return CLI_SUCCESS;
}

CTC_CLI(cli_sai_data_set_entry,
        cli_sai_data_set_entry_cmd,
        "sai set (fdb FDB_KEY|neighbor NEIGHBOR_KEY|route ROUTE_KEY|mcast-fdb MCAST_FDB_KEY |l2mc L2MC_KEY|ipmc IPMC_KEY|inseg INSEG_KEY|nat NAT_KEY) ATTR EXPR",
        "sai cmd",
        "sai set cmd",
        "fdb entry",
        "[switch_id:value,mac_address:xx:xx:xx:xx:xx:xx,bv_id:oid]",
        "neighbor entry",
        "[switch_id:value,rif_id:oid,ip_address:value]",
        "route entry",
        "[switch_id:value,vr_id:oid,destination:value/length]",
        "mcast_fdb entry",
        "[switch_id:value,mac_address:xx:xx:xx:xx:xx:xx,bv_id:oid]",
        "l2mc entry",
        "[switch_id:value,bv_id:oid,type:sai_l2mc_entry_type,destination:value/length,source:value/length]",
        "ipmc entry",
        "[switch_id:value,vr_id:oid,type:sai_ipmc_entry_type,destination:value/length,source:value/length]",
        "inseg entry",
        "[switch_id:value,label:value]",
        "nat entry",
        "[switch_id:value,vr_id:oid,type:sai_nat_type,data:[key:[src_ip:value,dst_ip:value,proto:value,l4_src_port:value,l4_dst_port:value],\n                                                        mask:[src_ip:value,dst_ip:value,proto:value,l4_src_port:value,l4_dst_port:value]]",
        "sai entry attribute",
        "sai value expression")
{
    int32 ret = 0;
    sai_attribute_t sai_attribute;
    sai_object_type_t obj_type = 0;
    ctc_sai_object_meta_key_t meta_key;
    ctc_sai_attr_metadata_t* attr_metadata = NULL;
    sai_object_key_entry_t object_key_entry;

    sal_memset(&meta_key, 0, sizeof(ctc_sai_object_meta_key_t));
    sal_memset(buf, 0, sizeof(buf));

    if (CTC_CLI_STR_EQUAL_ENHANCE("fdb", 0))
    {
        obj_type = SAI_OBJECT_TYPE_FDB_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("neighbor", 0))
    {
        obj_type = SAI_OBJECT_TYPE_NEIGHBOR_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("route", 0))
    {
        obj_type = SAI_OBJECT_TYPE_ROUTE_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("mcast_fdb", 0))
    {
        obj_type = SAI_OBJECT_TYPE_MCAST_FDB_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("l2mc", 0))
    {
        obj_type = SAI_OBJECT_TYPE_L2MC_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("ipmc", 0))
    {
        obj_type = SAI_OBJECT_TYPE_IPMC_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("inseg", 0))
    {
        obj_type = SAI_OBJECT_TYPE_INSEG_ENTRY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("nat", 0))
    {
        obj_type = SAI_OBJECT_TYPE_NAT_ENTRY;
    }
    sai_deserialize_object_key_entry(argv[1], obj_type, &object_key_entry);

    attr_metadata = ctc_sai_data_utils_object_get_attr_by_name(obj_type, argv[2]);
    if (NULL == attr_metadata)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "ATTR name is invalid!");
        return CLI_ERROR;
    }
    sai_attribute.id = attr_metadata->attrid;
    ret = ctc_sai_data_utils_attr_alloc_mem(attr_metadata->attrvaluetype, &sai_attribute);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Fail alloc attr memory!");
        return CLI_ERROR;
    }

    meta_key.objecttype = obj_type;
    sal_memcpy(&meta_key.objectkey.key, &object_key_entry, sizeof(sai_object_key_entry_t));

    sal_strncpy(buf, argv[3], sal_strlen(argv[3]));
    sai_deserialize_attribute(buf, attr_metadata, &sai_attribute);
    ret = ctc_sai_data_utils_object_set_attr(&meta_key, &sai_attribute);
    if (ret != SAI_STATUS_SUCCESS)
    {
        return CLI_ERROR;
    }
    ctc_sai_data_utils_attr_free_mem(attr_metadata->attrvaluetype, &sai_attribute);

    return CLI_SUCCESS;
}

CTC_CLI(cli_sai_data_test,
        cli_sai_data_test_cmd,
        "sai test (bool|chardata|uint8|int8|uint16|int16|uint32|int32|uint64|int64|pointer|mac|ipv4|ipv6|ip_address|ip_prefix|object_id|object_list|bool_list|uint8_list|int8_list|uint16_list|int16_list|uint32_list|int32_list|uint32_range|int32_range|vlan_list|qos_map_list|map_list|aclfield (bool|uint8|int8|uint16|int16|uint32|int32|uint64|mac|ipv4|ipv6|macsec_sci|object_id|object_list)|aclaction (bool|uint8|int8|uint16|int16|uint32|int32|mac|ipv4|ipv6|macsec_sci|object_id|object_list|uint8_list)|acl_capability|acl_resource_list|tlv_list|segment_list|ip_address_list|port_eye_values_list|timespec|macsec_sak|macsec_auth_key|macsec_salt|system_port_config|system_port_config_list|fabric_port_reachability|port_err_status_list|captured_timespec|timeoffset) VALUE",
        "sai cmd",
        "sai test cmd",
        "bool data",
        "chardata data",
        "uint8 data",
        "int8 data",
        "uint16 data",
        "int16 data",
        "uint32 data",
        "int32 data",
        "uint64 data",
        "int64 data",
        "pointer data",
        "mac data",
        "ipv4 data",
        "ipv6 data",
        "ip_address data",
        "ip_prefix data",
        "object_id data",
        "object_list data",
        "bool_list data",
        "uint8_list data",
        "int8_list data",
        "uint16_list data",
        "int16_list data",
        "uint32_list data",
        "int32_list data",
        "uint32_range data",
        "int32_range data",
        "vlan_list data",
        "qos_map_list data",
        "map_list data",
        "aclfield data",
        "aclfield data bool",
        "aclfield data uint8",
        "aclfield data int8",
        "aclfield data uint16",
        "aclfield data int16",
        "aclfield data uint32",
        "aclfield data int32",
        "aclfield data uint64",
        "aclfield data mac",
        "aclfield data ipv4",
        "aclfield data ipv6",
        "aclfield data macsec_sci",
        "aclfield data object_id",
        "aclfield data object_list",
        "aclfield data uint8_list",
        "aclaction data",
        "aclaction data bool",
        "aclaction data uint8",
        "aclaction data int8",
        "aclaction data uint16",
        "aclaction data int16",
        "aclaction data uint32",
        "aclaction data int32",
        "aclaction data mac",
        "aclaction data ipv4",
        "aclaction data ipv6",
        "aclaction data macsec_sci",
        "aclaction data object_id",
        "aclaction data object_list",
        "acl_capability data",
        "acl_resource_list data",
        "tlv_list data",
        "segment_list data",
        "ip_address_list data",
        "port_eye_values_list data",
        "timespec data",
        "macsec_sak data",
        "macsec_auth_key data",
        "macsec_salt data",
        "system_port_config data",
        "system_port_config_list data",
        "fabric_port_reachability data",
        "port_err_status_list data",
        "captured_timespec data",
        "timeoffset data",
        "VALUE")
{
    int32 ret = 0;
    sai_attribute_t sai_attribute;
    ctc_sai_attr_metadata_t attr_metadata;

    sal_memset(&attr_metadata, 0, sizeof(ctc_sai_attr_metadata_t));
    if (CTC_CLI_STR_EQUAL_ENHANCE("bool", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_BOOL;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("chardata", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_CHARDATA;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("uint8", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_UINT8;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("int8", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_INT8;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("uint16", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_UINT16;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("int16", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_INT16;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("uint32", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_UINT32;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("int32", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_INT32;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("uint64", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_UINT64;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("int64", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_INT64;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("pointer", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_POINTER;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("mac", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_MAC;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("ipv4", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_IPV4;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("ipv6", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_IPV6;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("ip_address", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("ip_prefix", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_IP_PREFIX;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("object_id", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_OBJECT_ID;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("object_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_OBJECT_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("bool_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_BOOL_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("uint8_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_UINT8_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("int8_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_INT8_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("uint16_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_UINT16_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("int16_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_INT16_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("uint32_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_UINT32_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("int32_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_INT32_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("uint32_range", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_UINT32_RANGE;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("int32_range", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_INT32_RANGE;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("vlan_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_VLAN_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("qos_map_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_QOS_MAP_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("map_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_MAP_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("aclfield", 0))
    {
        attr_metadata.isaclfield = 1;

        if (CTC_CLI_STR_EQUAL_ENHANCE("bool", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_BOOL;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("uint8", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("int8", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT8;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("uint16", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT16;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("int16", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT16;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("uint32", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT32;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("int32", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT32;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("uint64", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT64;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("mac", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_MAC;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("ipv4", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV4;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("ipv6", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV6;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("macsec_sci", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_MACSEC_SCI;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("object_id", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_ID;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("object_list", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_LIST;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("uint8_list", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST;
        }
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("aclaction", 0))
    {
        attr_metadata.isaclaction = 1;

        if (CTC_CLI_STR_EQUAL_ENHANCE("bool", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_BOOL;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("uint8", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT8;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("int8", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT8;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("uint16", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT16;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("int16", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT16;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("uint32", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT32;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("int32", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT32;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("mac", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_MAC;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("ipv4", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV4;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("ipv6", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV6;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("ip_address", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IP_ADDRESS;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("object_id", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_ID;
        }
        else if (CTC_CLI_STR_EQUAL_ENHANCE("object_list", 1))
        {
            attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_LIST;
        }
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("acl_capability", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_CAPABILITY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("acl_resource_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_ACL_RESOURCE_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("tlv_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_TLV_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("segment_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_SEGMENT_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("ip_address_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("port_eye_values_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_PORT_EYE_VALUES_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("timespec", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_TIMESPEC;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("macsec_sak", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SAK;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("macsec_auth_key", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_MACSEC_AUTH_KEY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("macsec_salt", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SALT;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("system_port_config", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("system_port_config_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("fabric_port_reachability", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_FABRIC_PORT_REACHABILITY;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("port_err_status_list", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_PORT_ERR_STATUS_LIST;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("captured_timespec", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_CAPTURED_TIMESPEC;
    }
    else if (CTC_CLI_STR_EQUAL_ENHANCE("timeoffset", 0))
    {
        attr_metadata.attrvaluetype = CTC_SAI_ATTR_VALUE_TYPE_TIMEOFFSET;
    }

    sal_memset(buf, 0, sizeof(buf));
    if (argc == 2)
    {
        sal_strcpy(buf, argv[1]);
    }
    else
    {
        sal_strcpy(buf, argv[2]);
    }

    ret = ctc_sai_data_utils_attr_alloc_mem(attr_metadata.attrvaluetype, &sai_attribute);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Fail alloc attr memory!");
        return CLI_ERROR;
    }

    attr_metadata.enummetadata = NULL;
    ret = sai_deserialize_attribute_value(buf, &attr_metadata, &sai_attribute.value);
    if (ret == SAI_SERIALIZE_ERROR)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Fail deserialize attribute value!");
        return CLI_ERROR;
    }

    sal_memset(buf, 0, sizeof(buf));
    sai_serialize_attribute_value(buf, &attr_metadata, &sai_attribute.value);
    ctc_sal_cli_out(buf);
    ctc_sai_data_utils_attr_free_mem(attr_metadata.attrvaluetype, &sai_attribute);

    return CLI_SUCCESS;
}

int32
ctc_sai_cli_init(void)
{
    ctc_sai_metadata_apis_query(sai_api_query, &apis);

    /* sai cli under sdk mode */
    install_element(CTC_SDK_MODE, &cli_sai_data_set_obj_cmd);
    install_element(CTC_SDK_MODE, &cli_sai_data_set_entry_cmd);
    install_element(CTC_SDK_MODE, &cli_sai_data_get_obj_cmd);
    install_element(CTC_SDK_MODE, &cli_sai_data_get_entry_cmd);
    install_element(CTC_SDK_MODE, &cli_sai_data_test_cmd);

    return CLI_SUCCESS;
}

