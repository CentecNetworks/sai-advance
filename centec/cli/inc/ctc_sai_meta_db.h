#ifndef _CTC_SAI_META_DB_H
#define _CTC_SAI_META_DB_H

#include "ctc_sai.h"

typedef struct _ctc_sai_object_meta_key_t
{
    /**
     * @brief Object type.
     */
    sai_object_type_t           objecttype;

    /**
     * @brief The key.
     *
     * @passparam objecttype
     */
    sai_object_key_t            objectkey;

} ctc_sai_object_meta_key_t;

typedef sai_status_t (*ctc_sai_meta_generic_create_fn)(
        _Inout_ ctc_sai_object_meta_key_t *meta_key,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

typedef sai_status_t (*ctc_sai_meta_generic_remove_fn)(
        _In_ const ctc_sai_object_meta_key_t *meta_key);

typedef sai_status_t (*ctc_sai_meta_generic_set_fn)(
        _In_ const ctc_sai_object_meta_key_t *meta_key,
        _In_ const sai_attribute_t *attr);

typedef sai_status_t (*ctc_sai_meta_generic_get_fn)(
        _In_ const ctc_sai_object_meta_key_t *meta_key,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

typedef enum _ctc_sai_attr_value_type_t
{
    /**
     * @brief Attribute value is bool.
     */
    CTC_SAI_ATTR_VALUE_TYPE_BOOL,

    /**
     * @brief Attribute value is char data.
     */
    CTC_SAI_ATTR_VALUE_TYPE_CHARDATA,

    /**
     * @brief Attribute value is 8 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_UINT8,

    /**
     * @brief Attribute value is 8 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_INT8,

    /**
     * @brief Attribute value is 16 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_UINT16,

    /**
     * @brief Attribute value is 16 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_INT16,

    /**
     * @brief Attribute value is 32 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_UINT32,

    /**
     * @brief Attribute value is 32 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_INT32,

    /**
     * @brief Attribute value is 64 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_UINT64,

    /**
     * @brief Attribute value is 64 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_INT64,

    /**
     * @brief Attribute value is pointer address.
     */
    CTC_SAI_ATTR_VALUE_TYPE_POINTER,

    /**
     * @brief Attribute value is MAC address.
     */
    CTC_SAI_ATTR_VALUE_TYPE_MAC,

    /**
     * @brief Attribute value is IPv4.
     */
    CTC_SAI_ATTR_VALUE_TYPE_IPV4,

    /**
     * @brief Attribute value is IPv6.
     */
    CTC_SAI_ATTR_VALUE_TYPE_IPV6,

    /**
     * @brief Attribute value is IP address.
     */
    CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS,

    /**
     * @brief Attribute value is IP prefix
     */
    CTC_SAI_ATTR_VALUE_TYPE_IP_PREFIX,

    /**
     * @brief Attribute value is object id.
     */
    CTC_SAI_ATTR_VALUE_TYPE_OBJECT_ID,

    /**
     * @brief Attribute value is object list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_OBJECT_LIST,

    /**
     * @brief Attribute value is bool list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_BOOL_LIST,

    /**
     * @brief Attribute value is list of 8 bit unsigned integers.
     */
    CTC_SAI_ATTR_VALUE_TYPE_UINT8_LIST,

    /**
     * @brief Attribute value is list of 8 bit signed integers.
     */
    CTC_SAI_ATTR_VALUE_TYPE_INT8_LIST,

    /**
     * @brief Attribute value is list of 16 bit unsigned integers.
     */
    CTC_SAI_ATTR_VALUE_TYPE_UINT16_LIST,

    /**
     * @brief Attribute value is list of 16 bit signed integers.
     */
    CTC_SAI_ATTR_VALUE_TYPE_INT16_LIST,

    /**
     * @brief Attribute value is list of 32 bit unsigned integers.
     */
    CTC_SAI_ATTR_VALUE_TYPE_UINT32_LIST,

    /**
     * @brief Attribute value is list of 32 bit signed integers.
     */
    CTC_SAI_ATTR_VALUE_TYPE_INT32_LIST,

    /**
     * @brief Attribute value is 32 bit unsigned integer range.
     */
    CTC_SAI_ATTR_VALUE_TYPE_UINT32_RANGE,

    /**
     * @brief Attribute value is 32 bit signed integer range.
     */
    CTC_SAI_ATTR_VALUE_TYPE_INT32_RANGE,

    /**
     * @brief Attribute value is ACL field bool.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_BOOL,

    /**
     * @brief Attribute value is ACL field 8 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8,

    /**
     * @brief Attribute value is ACL field 8 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT8,

    /**
     * @brief Attribute value is ACL field 16 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT16,

    /**
     * @brief Attribute value is ACL field 16 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT16,

    /**
     * @brief Attribute value is ACL field 32 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT32,

    /**
     * @brief Attribute value is ACL field 32 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT32,

    /**
     * @brief Attribute value is ACL field 64 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT64,

    /**
     * @brief Attribute value is ACL field MAC address.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_MAC,

    /**
     * @brief Attribute value is ACL field IPv4.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV4,

    /**
     * @brief Attribute value is ACL field IPv6.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV6,

    /**
     * @brief Attribute value is MACsec rule match field SCI.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_MACSEC_SCI,

    /**
     * @brief Attribute value is ACL field object id.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_ID,

    /**
     * @brief Attribute value is ACL field object list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_LIST,

    /**
     * @brief Attribute value is ACL field list of 8 bit unsigned integers.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST,

    /**
     * @brief Attribute value is ACL action bool.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_BOOL,

    /**
     * @brief Attribute value is ACL action 8 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT8,

    /**
     * @brief Attribute value is ACL action 8 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT8,

    /**
     * @brief Attribute value is ACL action 16 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT16,

    /**
     * @brief Attribute value is ACL action 16 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT16,

    /**
     * @brief Attribute value is ACL action 32 bit unsigned integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT32,

    /**
     * @brief Attribute value is ACL action 32 bit signed integer.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT32,

    /**
     * @brief Attribute value is ACL action MAC address.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_MAC,

    /**
     * @brief Attribute value is ACL action IPv4.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV4,

    /**
     * @brief Attribute value is ACL action IPv6.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV6,

    /**
     * @brief Attribute value is ACL action IP address.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IP_ADDRESS,

    /**
     * @brief Attribute value is ACL action object id.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_ID,

    /**
     * @brief Attribute value is ACL action object list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_LIST,

    /**
     * @brief Attribute value is ACL capability.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_CAPABILITY,

    /**
     * @brief Attribute value is ACL resource.
     */
    CTC_SAI_ATTR_VALUE_TYPE_ACL_RESOURCE_LIST,

    /**
     * @brief Attribute value is generic map list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_MAP_LIST,

    /**
     * @brief Attribute value is vlan list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_VLAN_LIST,

    /**
     * @brief Attribute value is QOS map list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_QOS_MAP_LIST,

    /**
     * @brief Attribute value is Segment Route Type Length Value list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_TLV_LIST,

    /**
     * @brief Attribute value is Segment Route Segment list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_SEGMENT_LIST,

    /**
     * @brief Attribute value is IP address list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS_LIST,

    /**
     * @brief Attribute value is port eye values list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_PORT_EYE_VALUES_LIST,

    /**
     * @brief Attribute value is timespec.
     */
    CTC_SAI_ATTR_VALUE_TYPE_TIMESPEC,

    /**
     * @brief Attribute value is NAT data.
     */
    CTC_SAI_ATTR_VALUE_TYPE_NAT_ENTRY_DATA,

    /**
     * @brief Attribute value is MACsec SCI.
     */
    CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SCI,

    /**
     * @brief Attribute value is MACsec SSCI.
     */
    CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SSCI,

    /**
     * @brief Attribute value is MACsec SAK.
     */
    CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SAK,

    /**
     * @brief Attribute value is MACsec Authentication Key.
     */
    CTC_SAI_ATTR_VALUE_TYPE_MACSEC_AUTH_KEY,

    /**
     * @brief Attribute value is MACsec SALT.
     */
    CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SALT,

    /**
     * @brief Attribute value is System Port Configuration.
     */
    CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG,

    /**
     * @brief Attribute value is System Port Configuration list.
     */
    CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG_LIST,

    /**
     * @brief Attribute value is Fabric Port Reachability.
     */
    CTC_SAI_ATTR_VALUE_TYPE_FABRIC_PORT_REACHABILITY,

    /**
     * @brief Attribute value is fabric port error status.
     */
    CTC_SAI_ATTR_VALUE_TYPE_PORT_ERR_STATUS_LIST,

    /**
     * @brief Attribute value is captured timespec.
     */
    CTC_SAI_ATTR_VALUE_TYPE_CAPTURED_TIMESPEC,

    /**
     * @brief Attribute value is time offset.
     */
    CTC_SAI_ATTR_VALUE_TYPE_TIMEOFFSET,

} ctc_sai_attr_value_type_t;

/**
 * @brief Defines enum metadata information.
 */
typedef struct _ctc_sai_enum_metadata_t
{
    /**
     * @brief String representation of enum type definition.
     */
    char*                     name;

    /**
     * @brief Values count in enum.
     */
    size_t                    valuescount;

    /**
     * @brief Array of enum values.
     */
    int*                      values;

    /**
     * @brief Array of enum values string names.
     */
    char**                    valuesnames;

} ctc_sai_enum_metadata_t;

/**
 * @brief Defines attribute metadata.
 */
typedef struct _ctc_sai_attr_metadata_t
{
    /**
     * @brief Specifies valid SAI object type.
     */
    sai_object_type_t                           objecttype;

    /**
     * @brief Specifies valid attribute id for this object type.
     */
    sai_attr_id_t                               attrid;

    /**
     * @brief Specifies valid attribute id name for this object type.
     */
    char*                                       attridname;

    /**
     * @brief Extracted brief description from Doxygen comment.
     */
    char*                                       brief;

    /**
     * @brief Specifies attribute value type for this attribute.
     */
    ctc_sai_attr_value_type_t                       attrvaluetype;

    /**
     * @brief Indicates whether attribute is enum value.
     *
     * Attribute type must be set as INT32.
     *
     * @note Could be deduced from enum type string or
     * enum vector values and attr value type.
     */
    bool                                        isenum;

    /**
     * @brief Indicates whether attribute is enum list value.
     *
     * Attribute value must be set INT32 LIST.
     *
     * @note Could be deduced from enum type string or
     * enum vector values and attr value type.
     */
    bool                                        isenumlist;

    /**
     * @brief Provides enum metadata if attribute
     * is enum or enum list.
     */
    ctc_sai_enum_metadata_t*                        enummetadata;

    /**
     * @brief Determines whether value is vlan.
     *
     * Can only be set on sai_uint16_t value type.
     */
    bool                                        isvlan;

    /**
     * @brief Determines whether attribute is ACL field
     *
     * This will become handy for fast determination whether
     * default value is present.
     */
    bool                                        isaclfield;

    /**
     * @brief Determines whether attribute is ACL action
     *
     * This will become handy for fast determination whether
     * default value is present.
     */
    bool                                        isaclaction;

} ctc_sai_attr_metadata_t;

/**
 * @brief SAI object type information
 */
typedef struct _ctc_sai_object_type_info_t
{
    /**
     * @brief Object Type
     */
    sai_object_type_t                               objecttype;

    /**
     * @brief Object Type name
     */
    char*                                          objecttypename;

    /**
     * @brief Indicates if object is OID object
     */
    bool                                            isobjectid;

    /**
     * @brief Create function pointer.
     */
    ctc_sai_meta_generic_create_fn                      create;

    /**
     * @brief Remove function pointer.
     */
    ctc_sai_meta_generic_remove_fn                      remove;

    /**
     * @brief Set function pointer.
     */
    ctc_sai_meta_generic_set_fn                         set;

    /**
     * @brief Get function pointer
     */
    ctc_sai_meta_generic_get_fn                         get;

    /**
     * @brief Provides enum metadata if attribute
     * is enum or enum list.
     */
    ctc_sai_enum_metadata_t*                        enummetadata;

    /**
     * @brief Attributes metadata
     */
    ctc_sai_attr_metadata_t**                       attrmetadata;

} ctc_sai_object_type_info_t;

typedef struct _sai_apis_t {
    sai_switch_api_t* switch_api;
    sai_port_api_t* port_api;
    sai_fdb_api_t* fdb_api;
    sai_vlan_api_t* vlan_api;
    sai_virtual_router_api_t* virtual_router_api;
    sai_route_api_t* route_api;
    sai_next_hop_api_t* next_hop_api;
    sai_next_hop_group_api_t* next_hop_group_api;
    sai_router_interface_api_t* router_interface_api;
    sai_neighbor_api_t* neighbor_api;
    sai_acl_api_t* acl_api;
    sai_hostif_api_t* hostif_api;
    sai_mirror_api_t* mirror_api;
    sai_samplepacket_api_t* samplepacket_api;
    sai_stp_api_t* stp_api;
    sai_lag_api_t* lag_api;
    sai_policer_api_t* policer_api;
    sai_wred_api_t* wred_api;
    sai_qos_map_api_t* qos_map_api;
    sai_queue_api_t* queue_api;
    sai_scheduler_api_t* scheduler_api;
    sai_scheduler_group_api_t* scheduler_group_api;
    sai_buffer_api_t* buffer_api;
    sai_hash_api_t* hash_api;
    sai_udf_api_t* udf_api;
    sai_tunnel_api_t* tunnel_api;
    sai_l2mc_api_t* l2mc_api;
    sai_ipmc_api_t* ipmc_api;
    sai_rpf_group_api_t* rpf_group_api;
    sai_l2mc_group_api_t* l2mc_group_api;
    sai_ipmc_group_api_t* ipmc_group_api;
    sai_mcast_fdb_api_t* mcast_fdb_api;
    sai_bridge_api_t* bridge_api;
    sai_tam_api_t* tam_api;
    sai_segmentroute_api_t* segmentroute_api;
    sai_mpls_api_t* mpls_api;
    sai_dtel_api_t* dtel_api;
    sai_bfd_api_t* bfd_api;
    sai_isolation_group_api_t* isolation_group_api;
    sai_nat_api_t* nat_api;
    sai_counter_api_t* counter_api;
    sai_debug_counter_api_t* debug_counter_api;
    sai_macsec_api_t* macsec_api;
    sai_system_port_api_t* system_port_api;
    sai_twamp_api_t* twamp_api;
    sai_npm_api_t* npm_api;
    sai_es_api_t* es_api;
    sai_y1731_api_t* y1731_api;
    sai_ptp_api_t* ptp_api;
    sai_synce_api_t* synce_api;
    sai_monitor_api_t* monitor_api;
} sai_apis_t;

typedef sai_status_t (*sai_api_query_fn)(sai_api_t sai_api_id, void** api_method_table);

extern ctc_sai_object_type_info_t* ctc_sai_metadata_all_object_type_infos[];
extern ctc_sai_attr_metadata_t** ctc_sai_metadata_attr_by_object_type[];

#endif
