/*
Copyright 2013-present Barefoot Networks, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/


namespace py switch_sai
namespace cpp switch_sai

#typedef byte i8
typedef i64 sai_thrift_object_id_t
typedef i64 sai_thrift_uint64_t
typedef i16 sai_thrift_vlan_id_t
typedef string sai_thrift_mac_t
typedef i8 sai_thrift_vlan_tagging_mode_t
typedef i32 sai_thrift_status_t
typedef string sai_thrift_ip4_t
typedef string sai_thrift_ip6_t
typedef i8 sai_thrift_ip_addr_family_t
typedef i8 sai_thrift_port_stp_port_state_t
typedef i32 sai_thrift_hostif_trap_id_t
typedef i32 sai_thrift_next_hop_type_t
typedef i32 sai_thrift_vlan_stat_counter_t
typedef i32 sai_thrift_twamp_stat_counter_t
typedef i32 sai_thrift_npm_stat_counter_t
typedef i32 sai_thrift_bridge_port_stat_counter_t
typedef i32 sai_thrift_router_interface_stat_counter_t
typedef i32 sai_thrift_policer_stat_counter_t
typedef i32 sai_thrift_port_stat_counter_t
typedef i32 sai_thrift_queue_stat_counter_t
typedef i32 sai_thrift_pg_stat_counter_t
typedef i32 sai_thrift_policer_stat_t
typedef i32 sai_thrift_stat_id_t
typedef i32 sai_thrift_l4port_t
typedef i8 sai_thrift_ipmc_entry_type_t
typedef i8 sai_thrift_l2mc_entry_type_t

struct sai_thrift_fdb_entry_t {
    1: sai_thrift_mac_t mac_address;
    2: sai_thrift_object_id_t bv_id;
}

struct sai_thrift_vlan_port_t {
    1: sai_thrift_object_id_t port_id;
    2: sai_thrift_vlan_tagging_mode_t tagging_mode;
}

union sai_thrift_ip_t {
    1: sai_thrift_ip4_t ip4;
    2: sai_thrift_ip6_t ip6;
}

struct sai_thrift_ip_address_t {
    1: sai_thrift_ip_addr_family_t addr_family;
    2: sai_thrift_ip_t addr;
}

struct sai_thrift_ip_prefix_t {
    1: sai_thrift_ip_addr_family_t addr_family;
    2: sai_thrift_ip_t addr;
    3: sai_thrift_ip_t mask;
}

struct sai_thrift_object_list_t {
    1: i32 count;
    2: list<sai_thrift_object_id_t> object_id_list;
}

struct sai_thrift_vlan_list_t {
    1: i32 vlan_count;
    2: list<sai_thrift_vlan_id_t> vlan_list;
}

struct sai_thrift_s32_list_t {
    1: i32 count;
    2: list<i32> s32list;
}

struct sai_thrift_status_list_t {
    1: i32 count;
    2: list<sai_thrift_status_t> status_list;
}

struct sai_thrift_route_entry_list_t {
    1: i32 count;
    2: list<sai_thrift_route_entry_t> thrift_route_entry_list;
}

struct sai_thrift_bool_list_t {
    1: i32 count;
    2: list<bool> boollist;
}
 /*##################################*/
struct sai_thrift_u8_list_t {
    1: i32 count;
    2: list<i8> u8list;
}

 /*##################################*/
struct sai_thrift_s8_list_t {
    1: i32 count;
    2: list<i8> s8list;
}

struct sai_thrift_u32_list_t {
    1: i32 count;
    2: list<i32> u32list;
}

union sai_thrift_acl_mask_t {
    1: i8 u8;
    2: i8 s8;
    3: i16 u16;
    4: i16 s16;
    5: i32 u32;
    6: i32 s32;
    7: sai_thrift_mac_t mac;
    8: sai_thrift_ip4_t ip4;
    9: sai_thrift_ip6_t ip6;
    10: sai_thrift_u8_list_t u8list;
}

union sai_thrift_acl_data_t {
    1: i8 u8;
    2: i8 s8;
    3: i16 u16;
    4: i16 s16;
    5: i32 u32;
    6: i32 s32;
    7: sai_thrift_mac_t mac;
    8: sai_thrift_ip4_t ip4;
    9: sai_thrift_ip6_t ip6;
    10: sai_thrift_object_id_t oid;
    11: sai_thrift_object_list_t objlist;
    12: sai_thrift_u8_list_t u8list;
}

struct sai_thrift_acl_field_data_t
{
    1: bool enable;
    2: sai_thrift_acl_mask_t mask;
    3: sai_thrift_acl_data_t data;
}

union sai_thrift_acl_parameter_t {
    1: i8 u8;
    2: i8 s8;
    3: i16 u16;
    4: i16 s16;
    5: i32 u32;
    6: i32 s32;
    7: sai_thrift_mac_t mac;
    8: sai_thrift_ip4_t ip4;
    9: sai_thrift_ip6_t ip6;
    10: sai_thrift_object_id_t oid;
    11: sai_thrift_object_list_t objlist;
}

struct sai_thrift_acl_action_data_t {
    1: bool enable;
    2: sai_thrift_acl_parameter_t parameter;
}

struct sai_thrift_qos_map_params_t {
    1: i8 tc;
    2: i8 dscp;
    3: i8 dot1p;
    4: i8 prio;
    5: i8 pg;
    6: i8 queue_index;
    7: i8 color;
    8: i8 mpls_exp;
}

struct sai_thrift_qos_map_t {
    1: sai_thrift_qos_map_params_t key;
    2: sai_thrift_qos_map_params_t value;
}

struct sai_thrift_qos_map_list_t {
    1: i32 count;
    2: list<sai_thrift_qos_map_t> map_list;
}

struct sai_thrift_u32_range_t {
    1: i32 min;
    2: i32 max;
}

struct sai_thrift_timeoffset_t {
    1: i8 flag;
    2: i32 value;
}

struct sai_thrift_timespec_t {
    1: i64 tv_sec;
    2: i32 tv_nsec;
}

struct sai_thrift_captured_timespec_t {
    1: sai_thrift_timespec_t timestamp;
    2: i16 secquence_id;
	3: sai_thrift_object_id_t port_id;
}

union sai_thrift_attribute_value_t {
    1:  bool booldata;
    2:  string chardata;
    3:  i8 u8;
    4:  i8 s8;
    5:  i16 u16;
    6:  i16 s16;
    7:  i32 u32;
    8:  i32 s32;
    9:  i64 u64;
    10: i64 s64;
    11: sai_thrift_mac_t mac;
    12: sai_thrift_object_id_t oid;
    13: sai_thrift_ip4_t ip4;
    14: sai_thrift_ip6_t ip6;
    15: sai_thrift_ip_address_t ipaddr;
    16: sai_thrift_object_list_t objlist;
    17: sai_thrift_vlan_list_t vlanlist;
    18: sai_thrift_acl_field_data_t aclfield;
    19: sai_thrift_acl_action_data_t aclaction;
	20: sai_thrift_u8_list_t u8list;       /*##################################*/
	21: sai_thrift_s8_list_t s8list;       /*##################################*/
    22: sai_thrift_u32_list_t u32list;
    23: sai_thrift_s32_list_t s32list;
    24: sai_thrift_qos_map_list_t qosmap;
	25: sai_thrift_u32_range_t u32range;
    26: sai_thrift_timeoffset_t timeoffset;
	27: sai_thrift_timespec_t timespec;
	28: sai_thrift_captured_timespec_t captured_timespec;
    29: sai_thrift_bool_list_t boollist;
}

struct sai_thrift_attribute_t {
    1: i32 id;
    2: sai_thrift_attribute_value_t value;
}

struct sai_thrift_route_entry_t {
    1: sai_thrift_object_id_t vr_id;
    2: sai_thrift_ip_prefix_t destination;
}

struct sai_thrift_neighbor_entry_t {
    1: sai_thrift_object_id_t rif_id;
    2: sai_thrift_ip_address_t ip_address;
}

struct sai_thrift_ipmc_entry_t {
    1: sai_thrift_object_id_t vr_id;
	2: sai_thrift_ipmc_entry_type_t type;
    3: sai_thrift_ip_address_t source;
	4: sai_thrift_ip_address_t destination;
}

struct sai_thrift_l2mc_entry_t {
    1: sai_thrift_object_id_t bv_id;
	2: sai_thrift_l2mc_entry_type_t type;
    3: sai_thrift_ip_address_t source;
	4: sai_thrift_ip_address_t destination;
}

struct sai_thrift_mcast_fdb_entry_t {
    1: sai_thrift_mac_t mac_address;
    2: sai_thrift_object_id_t bv_id;
}

/*##################################*/
struct sai_thrift_inseg_entry_t {
    1: i32 label;
}

struct sai_thrift_nat_entry_t {
    1: sai_thrift_object_id_t vr_id;
    2: sai_thrift_ip4_t source;
    3: sai_thrift_ip4_t destination;
    4: i16 proto;
    5: sai_thrift_l4port_t l4_src_port;
    6: sai_thrift_l4port_t l4_dst_port;
    7: sai_thrift_ip4_t source_mask;
    8: sai_thrift_ip4_t destination_mask;
    9: i16 proto_mask;
    10: sai_thrift_l4port_t l4_src_port_mask; 
    11: sai_thrift_l4port_t l4_dst_port_mask;
}

struct sai_thrift_attribute_list_t {
    1: list<sai_thrift_attribute_t> attr_list;
    2: i32 attr_count; // redundant
    3: sai_thrift_status_t status;
}

union sai_thrift_result_data_t {
    1: sai_thrift_object_list_t objlist;
    2: sai_thrift_object_id_t oid;
    3: i16 u16;
}

struct sai_thrift_result_t {
    1: sai_thrift_result_data_t data;
    2: sai_thrift_status_t status;
}

struct sai_thrift_results_t {
    1: sai_thrift_object_list_t objlist;
    2: sai_thrift_status_list_t statuslist;
}

struct sai_thrift_bulk_attributes_t {
    1: list<sai_thrift_attribute_t> attr_list;
}

service switch_sai_rpc {
    //port API
    sai_thrift_status_t sai_thrift_set_port_attribute(1: sai_thrift_object_id_t port_id, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_port_attribute(1: sai_thrift_object_id_t port_id);
    list<i64> sai_thrift_get_port_stats(
                             1: sai_thrift_object_id_t port_id,
                             2: list<sai_thrift_port_stat_counter_t> counter_ids,
                             3: i32 number_of_counters);
    list<i64> sai_thrift_get_port_stats_ext(
                             1: sai_thrift_object_id_t port_id,
                             2: list<sai_thrift_port_stat_counter_t> counter_ids,
                             3: i8 mode,
                             4: i32 number_of_counters);
    sai_thrift_status_t sai_thrift_clear_port_all_stats(1: sai_thrift_object_id_t port_id)
    sai_thrift_status_t sai_thrift_clear_port_stats(1: sai_thrift_object_id_t port_id, 2: i32 number_of_counters, 3: list<sai_thrift_port_stat_counter_t> counter_ids)
    
    //fdb API
    sai_thrift_status_t sai_thrift_create_fdb_entry(1: sai_thrift_fdb_entry_t thrift_fdb_entry, 2: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_delete_fdb_entry(1: sai_thrift_fdb_entry_t thrift_fdb_entry);
    sai_thrift_status_t sai_thrift_flush_fdb_entries(1: list <sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_set_fdb_entry_attribute(1: sai_thrift_fdb_entry_t thrift_fdb_entry, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_fdb_entry_attribute(1: sai_thrift_fdb_entry_t thrift_fdb_entry);

    //vlan API
    sai_thrift_object_id_t sai_thrift_create_vlan(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_vlan(1: sai_thrift_object_id_t vlan_oid);
    list<i64> sai_thrift_get_vlan_stats(
                             1: sai_thrift_object_id_t vlan_id,
                             2: list<sai_thrift_vlan_stat_counter_t> counter_ids,
                             3: i32 number_of_counters);
    list<i64> sai_thrift_get_vlan_stats_ext(1: sai_thrift_object_id_t vlan_id, 2: list<sai_thrift_vlan_stat_counter_t> thrift_counter_ids, 3: i8 mode, 4: i32 number_of_counters);
    sai_thrift_status_t sai_thrift_clear_vlan_stats(1: sai_thrift_object_id_t vlan_id, 2: list<sai_thrift_vlan_stat_counter_t> thrift_counter_ids, 3: i32 number_of_counters);
    sai_thrift_object_id_t sai_thrift_create_vlan_member(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_attribute_list_t sai_thrift_get_vlan_member_attribute(1: sai_thrift_object_id_t vlan_member_id);
    sai_thrift_status_t sai_thrift_remove_vlan_member(1: sai_thrift_object_id_t vlan_member_id);
    sai_thrift_status_t sai_thrift_set_vlan_attribute(1: sai_thrift_object_id_t vlan_id, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_status_t sai_thrift_set_vlan_member_attribute(1: sai_thrift_object_id_t vlan_member_id, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_vlan_attribute(1: sai_thrift_object_id_t vlan_id);
    sai_thrift_result_t sai_thrift_get_vlan_id(1: sai_thrift_object_id_t vlan_id);
    sai_thrift_results_t sai_thrift_create_vlan_members(1: list<sai_thrift_attribute_t> thrift_attr_lists, 2:list<i32> thrift_attr_count_lists, 3: i8 mode);
    sai_thrift_status_list_t sai_thrift_remove_vlan_members(1: list<sai_thrift_object_id_t> thrift_object_id_list, 2: i8 mode); 

    //virtual router API
    sai_thrift_object_id_t sai_thrift_create_virtual_router(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_virtual_router(1: sai_thrift_object_id_t vr_id);
    sai_thrift_status_t sai_thrift_set_virtual_router_attribute(1: sai_thrift_object_id_t vr_id, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_virtual_router_attribute(1: sai_thrift_object_id_t vr_id);

    //route API
    sai_thrift_status_t sai_thrift_create_route(1: sai_thrift_route_entry_t thrift_route_entry, 2: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_route(1: sai_thrift_route_entry_t thrift_route_entry);
    sai_thrift_status_t sai_thrift_set_route_attribute(1: sai_thrift_route_entry_t thrift_route_entry, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_route_attribute(1: sai_thrift_route_entry_t thrift_route_entry);
	sai_thrift_status_t sai_thrift_create_routes(1: list<sai_thrift_route_entry_t> thrift_route_entry_list, 2: list<sai_thrift_attribute_t> thrift_attr_list, 3:list<i32> thrift_attr_count_lists, 4: i8 mode );
	sai_thrift_status_t sai_thrift_remove_routes(1: list<sai_thrift_route_entry_t> thrift_route_entry_list, 2: i8 mode );
	sai_thrift_status_t sai_thrift_set_routes_attribute(1: list<sai_thrift_route_entry_t> thrift_route_entry_list, 2: list<sai_thrift_attribute_t> thrift_attr_list, 3: i8 mode );
	sai_thrift_attribute_list_t sai_thrift_get_routes_attribute(1: list<sai_thrift_route_entry_t> thrift_route_entry_list, 2: i8 mode );

    //router interface API
    sai_thrift_object_id_t sai_thrift_create_router_interface(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_router_interface(1: sai_thrift_object_id_t rif_id);
    sai_thrift_status_t sai_thrift_set_router_interface_attribute(1: sai_thrift_object_id_t rif_id, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_router_interface_attribute(1: sai_thrift_object_id_t rif_id);
    list<i64> sai_thrift_router_interface_get_stats(1: sai_thrift_object_id_t rif_id, 2: list<sai_thrift_router_interface_stat_counter_t> thrift_counter_ids, 3: i32 number_of_counters);
    list<i64> sai_thrift_router_interface_get_stats_ext(1: sai_thrift_object_id_t rif_id, 2: list<sai_thrift_router_interface_stat_counter_t> thrift_counter_ids, 3: i8 mode, 4: i32 number_of_counters);
    sai_thrift_status_t sai_thrift_router_interface_clear_stats(1: sai_thrift_object_id_t rif_id, 2: list<sai_thrift_router_interface_stat_counter_t> thrift_counter_ids, 3: i32 number_of_counters);

    //next hop API
    sai_thrift_object_id_t sai_thrift_create_next_hop(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_next_hop(1: sai_thrift_object_id_t next_hop_id);
	sai_thrift_status_t sai_thrift_set_next_hop_attribute(1: sai_thrift_object_id_t next_hop_id, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_next_hop_attribute(1: sai_thrift_object_id_t next_hop_id);

    // Next Hop Group API.
    sai_thrift_object_id_t sai_thrift_create_next_hop_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_next_hop_group(1: sai_thrift_object_id_t nhop_group_oid);
    sai_thrift_status_t sai_thrift_set_next_hop_group_attribute(1: sai_thrift_object_id_t nhop_group_oid, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_next_hop_group_attribute(1: sai_thrift_object_id_t nhop_group_oid);
    sai_thrift_object_id_t sai_thrift_create_next_hop_group_member(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_next_hop_group_member(1: sai_thrift_object_id_t nhop_group_member_oid);
    sai_thrift_attribute_list_t sai_thrift_get_next_hop_group_member_attribute(1: sai_thrift_object_id_t nhop_group_member_oid);
	sai_thrift_attribute_list_t sai_thrift_get_next_hop_group_member_attribute_ecmp(1: sai_thrift_object_id_t nhop_group_member_oid);
	sai_thrift_results_t sai_thrift_create_next_hop_group_members(1: list<sai_thrift_attribute_t> thrift_attr_lists, 2:list<i32> thrift_attr_count_lists, 3: i8 mode);
	sai_thrift_status_list_t sai_thrift_remove_next_hop_group_members(1: list<sai_thrift_object_id_t> thrift_object_id_list, 2: i8 mode);


    //lag API
    sai_thrift_object_id_t sai_thrift_create_lag(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_lag(1: sai_thrift_object_id_t lag_id);
    sai_thrift_status_t sai_thrift_set_lag_attribute(1: sai_thrift_object_id_t lag_id,
                                                     2: sai_thrift_attribute_t thrift_attr);
	sai_thrift_attribute_list_t sai_thrift_get_lag_attribute(1: sai_thrift_object_id_t lag_id);
    sai_thrift_object_id_t sai_thrift_create_lag_member(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_lag_member(1: sai_thrift_object_id_t lag_member_id);
	sai_thrift_status_t sai_thrift_set_lag_member_attribute(1: sai_thrift_object_id_t lag_member_id,
                                                     2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_lag_member_attribute(1: sai_thrift_object_id_t lag_member_id);

    //stp API
    sai_thrift_object_id_t sai_thrift_create_stp_entry(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_stp_entry(1: sai_thrift_object_id_t stp_id);

    sai_thrift_attribute_list_t sai_thrift_get_stp_attribute(1: sai_thrift_object_id_t stp_id);

    sai_thrift_object_id_t sai_thrift_create_stp_port(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_stp_port(1: sai_thrift_object_id_t stp_port_id);
    
    sai_thrift_attribute_list_t sai_thrift_get_stp_port_attribute(1: sai_thrift_object_id_t stp_port_id);
        
    sai_thrift_status_t sai_thrift_set_stp_port_state(1: sai_thrift_object_id_t stp_id, 2: sai_thrift_object_id_t port_id, 3: sai_thrift_port_stp_port_state_t stp_port_state);
    sai_thrift_port_stp_port_state_t sai_thrift_get_stp_port_state(1: sai_thrift_object_id_t stp_id, 2: sai_thrift_object_id_t port_id);

    sai_thrift_results_t sai_thrift_create_stp_ports(1: list<sai_thrift_attribute_t> thrift_attr_lists, 2:list<i32> thrift_attr_count_lists, 3: i8 mode);
    sai_thrift_status_list_t sai_thrift_remove_stp_ports(1: list<sai_thrift_object_id_t> thrift_object_id_list, 2: i8 mode); 
    
    //neighbor API
    sai_thrift_status_t sai_thrift_create_neighbor_entry(1: sai_thrift_neighbor_entry_t thrift_neighbor_entry, 2: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_neighbor_entry(1: sai_thrift_neighbor_entry_t thrift_neighbor_entry);
    sai_thrift_status_t sai_thrift_remove_all_neighbor_entry();
    sai_thrift_status_t sai_thrift_set_neighbor_entry_attribute(1: sai_thrift_neighbor_entry_t thrift_neighbor_entry, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_neighbor_entry_attribute(1: sai_thrift_neighbor_entry_t thrift_neighbor_entry);

    //switch API
    // sai_thrift_attribute_list_t sai_thrift_get_switch_attribute();
    sai_thrift_attribute_list_t sai_thrift_get_switch_attribute(1: list<i32> thrift_attr_ids);
    sai_thrift_attribute_t sai_thrift_get_port_list_by_front_port();
    sai_thrift_object_id_t sai_thrift_get_cpu_port_id();
    sai_thrift_object_id_t sai_thrift_get_default_trap_group();
    sai_thrift_object_id_t sai_thrift_get_default_router_id();
    sai_thrift_object_id_t sai_thrift_get_default_1q_bridge_id();
    sai_thrift_result_t sai_thrift_get_default_vlan_id();
    sai_thrift_object_id_t sai_thrift_get_port_id_by_front_port(1: string port_name);
    sai_thrift_status_t sai_thrift_set_switch_attribute(1: sai_thrift_attribute_t attribute);
    sai_thrift_object_id_t sai_thrift_create_switch();
    sai_thrift_status_t sai_thrift_remove_switch();
    list<i64> sai_thrift_get_switch_stats(
                             1: list<sai_thrift_port_stat_counter_t> counter_ids,
                             2: i32 number_of_counters);
    list<i64> sai_thrift_get_switch_stats_ext(
                             1: list<sai_thrift_port_stat_counter_t> counter_ids,
                             2: i8 mode,
                             3: i32 number_of_counters);
    sai_thrift_status_t sai_thrift_clear_switch_stats(
                             1: list<sai_thrift_port_stat_counter_t> counter_ids,
                             2: i32 number_of_counters);

    //bridge API
    sai_thrift_result_t sai_thrift_create_bridge_port(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_bridge_port(1: sai_thrift_object_id_t bridge_port_id);
    sai_thrift_result_t sai_thrift_get_bridge_port_list(1: sai_thrift_object_id_t bridge_id);
    sai_thrift_attribute_list_t sai_thrift_get_bridge_port_attribute(1: sai_thrift_object_id_t bridge_port_id);
    sai_thrift_status_t sai_thrift_set_bridge_port_attribute(1: sai_thrift_object_id_t bridge_port_id,
                                                             2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_result_t sai_thrift_create_bridge(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_bridge(1: sai_thrift_object_id_t bridge_id);
    sai_thrift_attribute_list_t sai_thrift_get_bridge_attribute(1: sai_thrift_object_id_t bridge_id);
    sai_thrift_status_t sai_thrift_set_bridge_attribute(1: sai_thrift_object_id_t bridge_id,
                                                             2: sai_thrift_attribute_t thrift_attr);
                                                             
    list<i64> sai_thrift_get_bridge_port_stats(
                             1: sai_thrift_object_id_t bridge_port_id,
                             2: list<sai_thrift_bridge_port_stat_counter_t> counter_ids,
                             3: i32 number_of_counters);
    list<i64> sai_thrift_get_bridge_port_stats_ext(1: sai_thrift_object_id_t bridge_port_id, 2: list<sai_thrift_bridge_port_stat_counter_t> thrift_counter_ids, 3: i8 mode, 4: i32 number_of_counters);
    sai_thrift_status_t sai_thrift_clear_bridge_port_stats(1: sai_thrift_object_id_t bridge_port_id, 2: list<sai_thrift_bridge_port_stat_counter_t> thrift_counter_ids, 3: i32 number_of_counters);                                                             

    //Trap API
    sai_thrift_object_id_t sai_thrift_create_hostif(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_hostif(1: sai_thrift_object_id_t thrift_hif_id);
    sai_thrift_attribute_list_t sai_thrift_get_hostif_attribute(1: sai_thrift_object_id_t thrift_hif_id);
    sai_thrift_status_t sai_thrift_set_hostif_attribute(1: sai_thrift_object_id_t thrift_hif_id,
                                                        2: sai_thrift_attribute_t thrift_attr);

    sai_thrift_object_id_t sai_thrift_create_hostif_table_entry(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_hostif_table_entry(1: sai_thrift_object_id_t thrift_hostif_table_entry_id);
    sai_thrift_attribute_list_t sai_thrift_get_hostif_table_entry_attribute(1: sai_thrift_object_id_t thrift_hostif_table_entry_id);
    sai_thrift_status_t sai_thrift_set_hostif_table_entry_attribute(1: sai_thrift_object_id_t thrift_hostif_table_entry_id,
                                                                    2: sai_thrift_attribute_t thrift_attr);

    sai_thrift_object_id_t sai_thrift_create_hostif_trap_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_hostif_trap_group(1: sai_thrift_object_id_t thrift_hostif_trap_group_id);
    sai_thrift_attribute_list_t sai_thrift_get_hostif_trap_group_attribute(1: sai_thrift_object_id_t thrift_hostif_trap_group_id);
    sai_thrift_status_t sai_thrift_set_hostif_trap_group_attribute(1: sai_thrift_object_id_t thrift_hostif_trap_group_id,
                                                                   2: sai_thrift_attribute_t thrift_attr);

    sai_thrift_object_id_t sai_thrift_create_hostif_trap(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_hostif_trap(1: sai_thrift_object_id_t thrift_hostif_trap_id);
    sai_thrift_attribute_list_t sai_thrift_get_hostif_trap_attribute(1: sai_thrift_object_id_t thrift_hostif_trap_id);
    sai_thrift_status_t sai_thrift_set_hostif_trap_attribute(1: sai_thrift_object_id_t thrift_hostif_trap_id,
                                                             2: sai_thrift_attribute_t thrift_attr);
                                                             
    // CPU Send packet 
    sai_thrift_status_t sai_thrift_send_hostif_packet(1: sai_thrift_object_id_t thrift_hif_id, 
                                                      2: string packet_data,
                                                      3: list<sai_thrift_attribute_t> thrift_attr_list);

    // ACL API
    # acl table
    sai_thrift_object_id_t sai_thrift_create_acl_table(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_acl_table(1: sai_thrift_object_id_t acl_table_id);
    sai_thrift_attribute_list_t sai_thrift_get_acl_table_attribute(1: sai_thrift_object_id_t acl_table_id, 2: list<i32> thrift_attr_ids);

    # acl entry
    sai_thrift_object_id_t sai_thrift_create_acl_entry(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_acl_entry(1: sai_thrift_object_id_t acl_entry);
    sai_thrift_status_t sai_thrift_set_acl_entry_attribute(1: sai_thrift_object_id_t acl_entry_id, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_acl_entry_attribute(1: sai_thrift_object_id_t acl_entry_id, 2: list<i32> thrift_attr_ids);

    # acl group
    sai_thrift_object_id_t sai_thrift_create_acl_table_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_acl_table_group(1: sai_thrift_object_id_t acl_table_group_id);
	sai_thrift_attribute_list_t sai_thrift_get_acl_table_group_attribute(1: sai_thrift_object_id_t acl_table_group_id);

    # acl group member
    sai_thrift_object_id_t sai_thrift_create_acl_table_group_member(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_acl_table_group_member(1: sai_thrift_object_id_t acl_table_group_member_id);
    sai_thrift_attribute_list_t sai_thrift_get_acl_table_group_member_attribute(1: sai_thrift_object_id_t acl_table_group_member_id);

    # acl counter
    sai_thrift_object_id_t sai_thrift_create_acl_counter(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_acl_counter(1: sai_thrift_object_id_t acl_counter_id);    
	sai_thrift_attribute_list_t sai_thrift_get_acl_counter_attribute(1: sai_thrift_object_id_t acl_counter_id);
    sai_thrift_status_t sai_thrift_set_acl_counter_attribute(1: sai_thrift_object_id_t acl_counter_id, 2: sai_thrift_attribute_t thrift_attr);    
    
    # acl range
    sai_thrift_object_id_t sai_thrift_create_acl_range(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_acl_range(1: sai_thrift_object_id_t acl_range_id);
	sai_thrift_attribute_list_t sai_thrift_get_acl_range_attribute(1: sai_thrift_object_id_t acl_range_id);
    
    // Hash API
    sai_thrift_object_id_t sai_thrift_create_hash(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_hash(1: sai_thrift_object_id_t hash_id);

	sai_thrift_status_t sai_thrift_set_hash_attribute(1: sai_thrift_object_id_t thrift_hash_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_hash_attribute(1: sai_thrift_object_id_t thrift_hash_id);

	// UDF API
    sai_thrift_object_id_t sai_thrift_create_udf_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_udf_group(1: sai_thrift_object_id_t udf_group_id);
    sai_thrift_attribute_list_t sai_thrift_get_udf_group_attribute(1: sai_thrift_object_id_t thrift_udf_group_id);

	sai_thrift_object_id_t sai_thrift_create_udf_match(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_udf_match(1: sai_thrift_object_id_t udf_match_id);
    sai_thrift_attribute_list_t sai_thrift_get_udf_match_attribute(1: sai_thrift_object_id_t thrift_udf_match_id);

	sai_thrift_object_id_t sai_thrift_create_udf(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_udf(1: sai_thrift_object_id_t udf_id);

	sai_thrift_status_t sai_thrift_set_udf_attribute(1: sai_thrift_object_id_t thrift_udf_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_udf_attribute(1: sai_thrift_object_id_t thrift_udf_id);

    // TWAMP API
    sai_thrift_object_id_t sai_thrift_create_twamp_session(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_twamp_session(1: sai_thrift_object_id_t session_id);

	sai_thrift_status_t sai_thrift_set_twamp_attribute(1: sai_thrift_object_id_t thrift_twamp_session_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_twamp_attribute(1: sai_thrift_object_id_t thrift_twamp_session_id);

    list<i64> sai_thrift_get_twamp_session_stats(
                             1: sai_thrift_object_id_t twamp_id,
                             2: list<sai_thrift_twamp_stat_counter_t> counter_ids,
                             3: i32 number_of_counters);

    sai_thrift_status_t sai_thrift_clear_twamp_session_stats(1: sai_thrift_object_id_t twamp_id, 2: list<sai_thrift_twamp_stat_counter_t> thrift_counter_ids, 3: i32 number_of_counters);  

    // NPM

    sai_thrift_object_id_t sai_thrift_create_npm_session(1: list<sai_thrift_attribute_t> thrift_attr_list);
    
    sai_thrift_status_t sai_thrift_remove_npm_session(1: sai_thrift_object_id_t session_id);

	sai_thrift_status_t sai_thrift_set_npm_attribute(1: sai_thrift_object_id_t thrift_npm_session_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
                                                         
    sai_thrift_attribute_list_t sai_thrift_get_npm_attribute(1: sai_thrift_object_id_t thrift_npm_session_id);

    list<i64> sai_thrift_get_npm_session_stats(
                             1: sai_thrift_object_id_t npm_id,
                             2: list<sai_thrift_npm_stat_counter_t> counter_ids,
                             3: i32 number_of_counters);

    sai_thrift_status_t sai_thrift_clear_npm_session_stats(1: sai_thrift_object_id_t npm_id, 2: list<sai_thrift_npm_stat_counter_t> thrift_counter_ids, 3: i32 number_of_counters); 
    
    
    // Mirror API
    sai_thrift_object_id_t sai_thrift_create_mirror_session(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_mirror_session(1: sai_thrift_object_id_t session_id);

	sai_thrift_status_t sai_thrift_set_mirror_attribute(1: sai_thrift_object_id_t thrift_mirror_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_mirror_attribute(1: sai_thrift_object_id_t thrift_mirror_id);

    // MPLS API
	sai_thrift_status_t sai_thrift_create_inseg_entry(1: sai_thrift_inseg_entry_t thrift_inseg_entry, 2: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_inseg_entry(1: sai_thrift_inseg_entry_t thrift_inseg_entry);
	sai_thrift_status_t sai_thrift_set_inseg_entry_attribute(1: sai_thrift_inseg_entry_t thrift_inseg_entry, 2: sai_thrift_attribute_t thrift_attr);
	sai_thrift_attribute_list_t sai_thrift_get_inseg_entry_attribute(1: sai_thrift_inseg_entry_t thrift_inseg_entry);

	// DUMP Log
	sai_thrift_status_t sai_thrift_dump_log(1: string dump_file_name);

    // Policer API
    sai_thrift_object_id_t sai_thrift_create_policer(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_policer(1: sai_thrift_object_id_t thrift_policer_id);
    sai_thrift_attribute_list_t sai_thrift_get_policer_attribute(1: sai_thrift_object_id_t thrift_policer_id);
    sai_thrift_status_t sai_thrift_set_policer_attribute(1: sai_thrift_object_id_t thrift_policer_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
    list<sai_thrift_uint64_t> sai_thrift_get_policer_stats(1: sai_thrift_object_id_t thrift_policer_id,
                                                           2: list<sai_thrift_policer_stat_t> thrift_counter_ids);
    
	list<sai_thrift_uint64_t> sai_thrift_get_policer_stats_ext(1: sai_thrift_object_id_t thrift_policer_id,
                                                           2: list<sai_thrift_policer_stat_t> thrift_counter_ids,
														   3: i8 mode);
														   
    sai_thrift_status_t sai_thrift_clear_policer_stats(1: sai_thrift_object_id_t thrift_policer_id,
                                                       2: list<sai_thrift_policer_stat_t> thrift_counter_ids);

    // Scheduler API
    sai_thrift_object_id_t sai_thrift_create_scheduler_profile(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_scheduler_profile(1: sai_thrift_object_id_t scheduler_id);
    sai_thrift_attribute_list_t sai_thrift_get_scheduler_attribute(1: sai_thrift_object_id_t thrift_scheduler_id);
    sai_thrift_status_t sai_thrift_set_scheduler_attribute(1: sai_thrift_object_id_t thrift_scheduler_id,
                                                           2: sai_thrift_attribute_t thrift_attr);

    // Scheduler Group API
    sai_thrift_object_id_t sai_thrift_create_scheduler_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_scheduler_group(1: sai_thrift_object_id_t scheduler_group_id);
    sai_thrift_attribute_list_t sai_thrift_get_scheduler_group_attribute(1: sai_thrift_object_id_t scheduler_group_id);
    sai_thrift_status_t sai_thrift_set_scheduler_group_attribute(1: sai_thrift_object_id_t scheduler_group_id,
                                                           2: sai_thrift_attribute_t thrift_attr);

    // Queue API
    list<i64> sai_thrift_get_queue_stats(
                             1: sai_thrift_object_id_t queue_id,
                             2: list<sai_thrift_queue_stat_counter_t> counter_ids,
                             3: i32 number_of_counters);
    sai_thrift_status_t sai_thrift_clear_queue_stats(
                             1: sai_thrift_object_id_t queue_id,
                             2: list<sai_thrift_queue_stat_counter_t> counter_ids,
                             3: i32 number_of_counters);
    sai_thrift_object_id_t sai_thrift_create_queue(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_queue(1: sai_thrift_object_id_t queue_id);
    sai_thrift_attribute_list_t sai_thrift_get_queue_attribute(1: sai_thrift_object_id_t queue_id);
    sai_thrift_status_t sai_thrift_set_queue_attribute(1: sai_thrift_object_id_t queue_id,
                                                       2: sai_thrift_attribute_t thrift_attr)

    // Buffer API
    sai_thrift_object_id_t sai_thrift_create_buffer_profile(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_buffer_profile(1: sai_thrift_object_id_t buffer_profile_id);
    sai_thrift_attribute_list_t sai_thrift_get_buffer_profile_attribute(1: sai_thrift_object_id_t buffer_profile_id);
    sai_thrift_status_t sai_thrift_set_buffer_profile_attribute(1: sai_thrift_object_id_t buffer_profile_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_object_id_t sai_thrift_create_pool_profile(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_object_id_t sai_thrift_create_priority_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_priority_group(1: sai_thrift_object_id_t priority_group_id);
    sai_thrift_attribute_list_t sai_thrift_get_priority_group_attribute(1: sai_thrift_object_id_t priority_group_id);
    sai_thrift_status_t sai_thrift_set_priority_group_attribute(1: sai_thrift_object_id_t pg_id,
                                                                2: sai_thrift_attribute_t thrift_attr)
    list<i64> sai_thrift_get_pg_stats(
                         1: sai_thrift_object_id_t pg_id,
                         2: list<sai_thrift_pg_stat_counter_t> counter_ids,
                         3: i32 number_of_counters);

    // WRED API
    sai_thrift_object_id_t sai_thrift_create_wred_profile(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_wred_profile(1: sai_thrift_object_id_t wred_id);
    sai_thrift_attribute_list_t sai_thrift_get_wred_attribute_profile(1: sai_thrift_object_id_t wred_id);
    sai_thrift_status_t sai_thrift_set_wred_attribute_profile(1: sai_thrift_object_id_t wred_id,
                                                         2: sai_thrift_attribute_t thrift_attr);

    // QoS Map API
    sai_thrift_object_id_t sai_thrift_create_qos_map(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_qos_map(1: sai_thrift_object_id_t qos_map_id);
    sai_thrift_attribute_list_t sai_thrift_get_qos_map_attribute(1: sai_thrift_object_id_t qos_map_id);
    sai_thrift_status_t sai_thrift_set_qos_map_attribute(1: sai_thrift_object_id_t qos_map_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
	// MCAST L2MC GROUP
	sai_thrift_object_id_t sai_thrift_create_l2mc_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_l2mc_group(1: sai_thrift_object_id_t grp_id);
	sai_thrift_attribute_list_t sai_thrift_get_l2mc_group_attribute(1: sai_thrift_object_id_t grp_id);

	sai_thrift_object_id_t sai_thrift_create_l2mc_group_member(1: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_l2mc_group_member(1: sai_thrift_object_id_t member_id);
	sai_thrift_status_t sai_thrift_set_l2mc_group_member_attribute(1: sai_thrift_object_id_t member_id, 2: sai_thrift_attribute_t thrift_attr);
	sai_thrift_attribute_list_t sai_thrift_get_l2mc_group_member_attribute(1: sai_thrift_object_id_t member_id);

	// L2MC ENTRY
	sai_thrift_status_t sai_thrift_create_l2mc_entry(1: sai_thrift_l2mc_entry_t thrift_l2mc_entry, 2: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_l2mc_entry(1: sai_thrift_l2mc_entry_t thrift_l2mc_entry);
	sai_thrift_status_t sai_thrift_set_l2mc_entry_attribute(1: sai_thrift_l2mc_entry_t thrift_l2mc_entry, 2: sai_thrift_attribute_t thrift_attr);
	sai_thrift_attribute_list_t sai_thrift_get_l2mc_entry_attribute(1: sai_thrift_l2mc_entry_t thrift_l2mc_entry);

	// MCAST FDB ENTRY
	sai_thrift_status_t sai_thrift_create_mcast_fdb_entry(1: sai_thrift_mcast_fdb_entry_t thrift_mcast_fdb_entry, 2: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_mcast_fdb_entry(1: sai_thrift_mcast_fdb_entry_t thrift_mcast_fdb_entry);
	sai_thrift_status_t sai_thrift_set_mcast_fdb_entry_attribute(1: sai_thrift_mcast_fdb_entry_t thrift_mcast_fdb_entry, 2: sai_thrift_attribute_t thrift_attr);
	sai_thrift_attribute_list_t sai_thrift_get_mcast_fdb_entry_attribute(1: sai_thrift_mcast_fdb_entry_t thrift_mcast_fdb_entry);

	// MCAST IPMC GROUP
	sai_thrift_object_id_t sai_thrift_create_ipmc_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_ipmc_group(1: sai_thrift_object_id_t grp_id);
	sai_thrift_attribute_list_t sai_thrift_get_ipmc_group_attribute(1: sai_thrift_object_id_t grp_id);

	sai_thrift_object_id_t sai_thrift_create_ipmc_group_member(1: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_ipmc_group_member(1: sai_thrift_object_id_t member_id);
	sai_thrift_status_t sai_thrift_set_ipmc_group_member_attribute(1: sai_thrift_object_id_t member_id, 2: sai_thrift_attribute_t thrift_attr);
	sai_thrift_attribute_list_t sai_thrift_get_ipmc_group_member_attribute(1: sai_thrift_object_id_t member_id);

	// RPF GROUP
	sai_thrift_object_id_t sai_thrift_create_rpf_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_rpf_group(1: sai_thrift_object_id_t grp_id);
	sai_thrift_attribute_list_t sai_thrift_get_rpf_group_attribute(1: sai_thrift_object_id_t grp_id);
	sai_thrift_object_id_t sai_thrift_create_rpf_group_member(1: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_rpf_group_member(1: sai_thrift_object_id_t member_id);
	sai_thrift_status_t sai_thrift_set_rpf_group_member_attribute(1: sai_thrift_object_id_t member_id, 2: sai_thrift_attribute_t thrift_attr);
	sai_thrift_attribute_list_t sai_thrift_get_rpf_group_member_attribute(1: sai_thrift_object_id_t member_id);

	// IPMC ENTRY
	sai_thrift_status_t sai_thrift_create_ipmc_entry(1: sai_thrift_ipmc_entry_t thrift_ipmc_entry, 2: list<sai_thrift_attribute_t> thrift_attr_list);
	sai_thrift_status_t sai_thrift_remove_ipmc_entry(1: sai_thrift_ipmc_entry_t thrift_ipmc_entry);
	sai_thrift_status_t sai_thrift_set_ipmc_entry_attribute(1: sai_thrift_ipmc_entry_t thrift_ipmc_entry, 2: sai_thrift_attribute_t thrift_attr);
	sai_thrift_attribute_list_t sai_thrift_get_ipmc_entry_attribute(1: sai_thrift_ipmc_entry_t thrift_ipmc_entry);

	// SAMPLE PACKET
    sai_thrift_object_id_t sai_thrift_create_samplepacket(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_samplepacket(1: sai_thrift_object_id_t samplepacket_id);
    sai_thrift_attribute_list_t sai_thrift_get_samplepacket_attribute(1: sai_thrift_object_id_t samplepacket_id);
    sai_thrift_status_t sai_thrift_set_samplepacket_attribute(1: sai_thrift_object_id_t samplepacket_id,
                                                             2: sai_thrift_attribute_t thrift_attr);

    // TUNNEL
    sai_thrift_object_id_t sai_thrift_create_tunnel_map_entry(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_tunnel_map_entry(1: sai_thrift_object_id_t tunnel_map_entry_id);
    sai_thrift_attribute_list_t sai_thrift_get_tunnel_map_entry_attribute(1: sai_thrift_object_id_t tunnel_map_entry_id);
    sai_thrift_status_t sai_thrift_set_tunnel_map_entry_attribute(1: sai_thrift_object_id_t tunnel_map_entry_id,
                                                             2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_object_id_t sai_thrift_create_tunnel_map(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_tunnel_map(1: sai_thrift_object_id_t tunnel_map_id);
    sai_thrift_attribute_list_t sai_thrift_get_tunnel_map_attribute(1: sai_thrift_object_id_t tunnel_map_id);
    sai_thrift_status_t sai_thrift_set_tunnel_map_attribute(1: sai_thrift_object_id_t tunnel_map_id,
                                                             2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_object_id_t sai_thrift_create_tunnel(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_tunnel(1: sai_thrift_object_id_t tunnel_id);
    sai_thrift_attribute_list_t sai_thrift_get_tunnel_attribute(1: sai_thrift_object_id_t tunnel_id,
                                                                2: list<i32> thrift_attr_ids);
    sai_thrift_status_t sai_thrift_set_tunnel_attribute(1: sai_thrift_object_id_t tunnel_id,
                                                             2: sai_thrift_attribute_t thrift_attr);
    list<i64> sai_thrift_get_tunnel_stats(
                             1: sai_thrift_object_id_t tunnel_id,
                             2: list<sai_thrift_queue_stat_counter_t> counter_ids,
                             3: i32 number_of_counters);
    sai_thrift_status_t sai_thrift_clear_tunnel_stats(
                             1: sai_thrift_object_id_t tunnel_id,
                             2: list<sai_thrift_queue_stat_counter_t> counter_ids,
                             3: i32 number_of_counters);
    sai_thrift_object_id_t sai_thrift_create_tunnel_term_table_entry(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_tunnel_term_table_entry(1: sai_thrift_object_id_t tunnel_term_table_entry_id);
    sai_thrift_attribute_list_t sai_thrift_get_tunnel_term_table_entry_attribute(1: sai_thrift_object_id_t tunnel_term_table_entry_id,
                                                                                 2: list<i32> thrift_attr_ids);
    sai_thrift_status_t sai_thrift_set_tunnel_term_table_entry_attribute(1: sai_thrift_object_id_t tunnel_term_table_entry_id,
                                                             2: sai_thrift_attribute_t thrift_attr);
    // Get Remote CPU receive packet info
    sai_thrift_attribute_list_t sai_thrift_get_cpu_packet_attribute();
    sai_thrift_result_t sai_thrift_get_cpu_packet_count();
    sai_thrift_result_t sai_thrift_clear_cpu_packet_info();
    
    //log set
    sai_thrift_status_t sai_thrift_log_set(1: i32 sai_api_id,  2: i32 log_level);

    sai_thrift_object_id_t sai_thrift_create_isolation_group(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_isolation_group(1: sai_thrift_object_id_t iso_group_oid);
    sai_thrift_object_id_t sai_thrift_create_isolation_group_member(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_isolation_group_member(1: sai_thrift_object_id_t member_oid);
    sai_thrift_attribute_list_t sai_thrift_get_isolation_group_attributes(1: sai_thrift_object_id_t iso_group_oid);
    sai_thrift_attribute_list_t sai_thrift_get_isolation_group_member_attributes(1: sai_thrift_object_id_t member_oid);
    
    //COUNTER
    sai_thrift_object_id_t sai_thrift_create_counter(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_counter(1: sai_thrift_object_id_t counter_oid);
    sai_thrift_status_t sai_thrift_set_counter_attribute(1: sai_thrift_object_id_t thrift_counter_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_counter_attribute(1: sai_thrift_object_id_t thrift_counter_id);
    list<i64> sai_thrift_get_counter_stats(
                             1: sai_thrift_object_id_t counter_id,
                             2: list<sai_thrift_stat_id_t> counter_ids,
                             3: i32 number_of_counters);
    list<i64> sai_thrift_get_counter_stats_ext(
                             1: sai_thrift_object_id_t counter_id,
                             2: list<sai_thrift_stat_id_t> counter_ids,
                             3: i8 mode,
                             4: i32 number_of_counters);
    sai_thrift_status_t sai_thrift_clear_counter_stats(
                             1: sai_thrift_object_id_t counter_id, 
                             2: list<sai_thrift_stat_id_t> thrift_counter_ids, 
                             3: i32 number_of_counters);
    
    //DEBUG COUNTER
    sai_thrift_object_id_t sai_thrift_create_debug_counter(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_debug_counter(1: sai_thrift_object_id_t debug_counter_oid);
    sai_thrift_status_t sai_thrift_set_debug_counter_attribute(1: sai_thrift_object_id_t thrift_debug_counter_id,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_debug_counter_attribute(1: sai_thrift_object_id_t thrift_debug_counter_id);
    
    //NAT API
    sai_thrift_status_t sai_thrift_create_nat(1: sai_thrift_nat_entry_t thrift_nat_entry, 2: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_nat(1: sai_thrift_nat_entry_t thrift_nat_entry);
    sai_thrift_status_t sai_thrift_set_nat_attribute(1: sai_thrift_nat_entry_t thrift_nat_entry, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_nat_attribute(1: sai_thrift_nat_entry_t thrift_nat_entry);
    
    //BFD API
    sai_thrift_object_id_t sai_thrift_create_bfd(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_bfd(1: sai_thrift_object_id_t bfd_oid);
    sai_thrift_status_t sai_thrift_set_bfd_attribute(1: sai_thrift_object_id_t bfd_oid,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_bfd_attribute(1: sai_thrift_object_id_t bfd_oid);
    
    //Y1731 API
    sai_thrift_object_id_t sai_thrift_create_y1731_meg(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_y1731_meg(1: sai_thrift_object_id_t y1731_meg_oid);
    sai_thrift_status_t sai_thrift_set_y1731_meg_attribute(1: sai_thrift_object_id_t y1731_meg_oid,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_y1731_meg_attribute(1: sai_thrift_object_id_t y1731_meg_oid);
    
    sai_thrift_object_id_t sai_thrift_create_y1731_session(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_y1731_session(1: sai_thrift_object_id_t y1731_session_oid);
    sai_thrift_status_t sai_thrift_set_y1731_session_attribute(1: sai_thrift_object_id_t y1731_session_oid,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_y1731_session_attribute(1: sai_thrift_object_id_t y1731_session_oid);
    
    sai_thrift_object_id_t sai_thrift_create_y1731_rmep(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_y1731_rmep(1: sai_thrift_object_id_t y1731_rmep_oid);
    sai_thrift_status_t sai_thrift_set_y1731_rmep_attribute(1: sai_thrift_object_id_t y1731_rmep_oid,
                                                         2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_y1731_rmep_attribute(1: sai_thrift_object_id_t y1731_rmep_oid);
    
    list<i64> sai_thrift_get_y1731_session_lm_stats(
                             1: sai_thrift_object_id_t y1731_session_oid,
                             2: list<sai_thrift_stat_id_t> lm_stats_ids,
                             3: i32 number_of_stats);

    //PORT API
    sai_thrift_object_id_t sai_thrift_create_port(1: string port_name, 2: list<sai_thrift_attribute_t> thrift_attr_list)    
    sai_thrift_status_t sai_thrift_remove_port(1: sai_thrift_object_id_t port_oid);    
	
	//PTP API
    sai_thrift_object_id_t sai_thrift_create_ptp_domain(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_ptp_domain(1: sai_thrift_object_id_t ptp_oid);
    sai_thrift_status_t sai_thrift_set_ptp_domain_attribute(1: sai_thrift_object_id_t ptp_oid, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_ptp_domain_attribute(1: sai_thrift_object_id_t ptp_oid);	

	//syncE API
    sai_thrift_object_id_t sai_thrift_create_synce(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_synce(1: sai_thrift_object_id_t synce_oid);
    sai_thrift_status_t sai_thrift_set_synce_attribute(1: sai_thrift_object_id_t synce_oid, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_synce_attribute(1: sai_thrift_object_id_t synce_oid);	
    
    //ES API
    sai_thrift_object_id_t sai_thrift_create_es(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_es(1: sai_thrift_object_id_t es_oid);
    sai_thrift_status_t sai_thrift_set_es_attribute(1: sai_thrift_object_id_t es_oid, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_es_attribute(1: sai_thrift_object_id_t es_oid);

	//Monitor API
    sai_thrift_object_id_t sai_thrift_create_monitor_buffer(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_monitor_buffer(1: sai_thrift_object_id_t monitor_buffer_oid);
    sai_thrift_status_t sai_thrift_set_monitor_buffer_attribute(1: sai_thrift_object_id_t monitor_buffer_oid, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_monitor_buffer_attribute(1: sai_thrift_object_id_t monitor_buffer_oid);	

    sai_thrift_object_id_t sai_thrift_create_monitor_latency(1: list<sai_thrift_attribute_t> thrift_attr_list);
    sai_thrift_status_t sai_thrift_remove_monitor_latency(1: sai_thrift_object_id_t monitor_latency_oid);
    sai_thrift_status_t sai_thrift_set_monitor_latency_attribute(1: sai_thrift_object_id_t monitor_latency_oid, 2: sai_thrift_attribute_t thrift_attr);
    sai_thrift_attribute_list_t sai_thrift_get_monitor_latency_attribute(1: sai_thrift_object_id_t monitor_latency_oid);	

}
