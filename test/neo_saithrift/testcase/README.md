#Test Script Report

##Common Script

| Module | Number | Module | Number | Module | Number | Module | Number | Module | Number |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| acl | 6 | hostif | 12 | l2 | 12 | l3 | 20 | mirror | 8 |

##Centec Script

| Module | Number | Module | Number | Module | Number | Module | Number |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| acl | 134 | aps | 29 | bfd | 36 | bridge | 62 |
| buffer | 18 | counter | 25 | debug_counter | 7 | fdb | 35 |
| hash | 115 | hostif | 12 | h-qos | 4 | ipmc | 55 |
| l2mc | 66 | lag | 34 | mirror | 19 | monitor | 61 |
| mpls | 87 | mplsvpn | 15 | nat | 6 | neighbor | 26 |
| nexthop | 12 | nexthop_group | 19 | npm | 35 | oam_aps | 29 |
| policer | 43 | port | 69 | ptp | 35 | qosmap | 56 |
| queue | 18 | route | 71 | router_interface | 22 | scheduler | 13 |
| scheduler_group | 19 | samplepacket | 8 | stp | 23 | switch | 75 |
| tunnel | 15 | twamp | 20 | udf | 16 | virtual_router | 7 |
| vlan | 50 | wred | 19 | y1731 | 58 | Total | 1578 |

#Basic Module Test Script

##Switch

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_switch_fn | switch能够在uml环境当中正常启动 | 无 |
| sai_remove_switch_fn | switch能够在uml环境当中正常冷热重启 | 无 |
| sai_set_switch_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功set，不支持的需要返回错误 | func_03_set_and_get_switch_attribute_xx |
| sai_get_switch_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回错误 | func_03_set_and_get_switch_attribute_xx |
| sai_get_switch_stats_fn | 发一定数量的报文之后，验证stats是否准确；停流情况下验证多次get stats数据是否一致&nbsp; | func_04_get_switch_stats_and_clear_switch_stats |
| sai_get_switch_stats_ext_fn | 发一定数量的报文之后，不同mode下验证stats是否准确；再次get stats数据时验证所有stats数据是否清零（对应读清mode）&nbsp;&nbsp; | func_05_get_switch_stats_ext |
| sai_clear_switch_stats_fn | 发包验证stats数据准确之后，clear stats，再次get stats验证所有数据全部清零 | func_04_get_switch_stats_and_clear_switch_stats |

###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| 基于switch ingress/egress bind acl | scenario_01_switch_ingress_and_egrees_acl |
| 获取当前ipv4/v6 route entry count | scenario_02_get_available_ip_route_entry |
| 获取当前ipv4/v6 nexthop count | scenario_03_get_available_nexthop |
| 获取当前ipv4/v6 neighbor count | scenario_04_get_available_neighbor |
| 获取当前nexthop group以及group member count | scenario_05_get_available_nexthop_group |
| 获取当前fdb entry count | scenario_06_get_available_fdb |
| 获取当前l2mc entry count | scenario_07_get_available_l2mc |
| 获取当前ipmc entry count | scenario_08_get_available_ipmc |
| 获取当前snat entry count | scenario_09_get_available_snat |
| 获取当前dnat entry count | scenario_10_get_available_dnat |
| 全局设置system route-mac | scenario_11_set_route_mac |
| 全局控制learning-address-number | scenario_12_set_max_learning_address |
| 全局控制fdb-unicast-miss-packet-action | scenario_13_fdb_unicast_miss_packet_action |
| 全局控制fdb-multicast-miss-packet-action | scenario_14_fdb_multicast_miss_packet_action |
| 全局控制fdb-broadcast-miss-packet-action | scenario_15_fdb_broadcast_miss_packet_action |

##Port

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_port_fn | 指定speed和lane_list，创建port，执行成功后返回相应的port-oid | func_01_create_port_fn |
| 　 | 创建相同的port，返回相同的port-oid | func_02_create_same_port_fn |
| 　 | 创建max个不同的port，成功执行，再创建port时，执行失败 | func_03_create_max_port_fn |
| sai_remove_port_fn | 删除已经创建的port，执行成功 | func_04_remove_port_fn |
| 　 | 删除未创建的port，返回异常 | func_05_remove_not_exist_port_fn |
| sai_set_port_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功set，不支持的需要返回unsupport | func_06_set_and_get_port_attribute_fn_XX |
| sai_get_port_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回unsupport | func_06_set_and_get_port_attribute_fn_XX |
| sai_get_port_stats_fn | 发固定数量的报文转发之后，验证stats是否准确；停流情况下验证多次get stats数据是否一致 | func_07_get_port_stats |
| sai_get_port_stats_ext_fn | 发固定数量的报文转发之后，不同mode下验证stats是否准确；再次get stats数据时验证所有stats数据是否清零（对应读清mode） | func_08_get_port_stats_ext |
| sai_clear_port_stats_fn | 发包验证stats数据准确之后，clear 指定stats，验证只有指定的stats数据被清零 | func_09_clear_port_stats |
| sai_clear_port_all_stats_fn | 发包验证stats数据准确之后，clear stats，验证所有数据全部清零 | func_10_debug_counter_get_port_stats |
| sai_create_port_pool_fn | 　 | 不支持 |
| sai_remove_port_pool_fn | 　 | 不支持 |
| sai_set_port_pool_attribute_fn | 　 | 不支持 |
| sai_get_port_pool_attribute_fn | 　 | 不支持 |
| sai_get_port_pool_stats_fn | 　 | 不支持 |
| sai_get_port_pool_stats_ext_fn | 　 | 不支持 |
| sai_clear_port_pool_stats_fn | 　 | 不支持 |
| sai_create_port_serdes_fn | 　 | 不支持 |
| sai_remove_port_serdes_fn | 　 | 不支持 |
| sai_set_port_serdes_attribute_fn | 　 | 不支持 |
| sai_get_port_serdes_attribute_fn | 　 | 不支持 |

##Vlan

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_vlan_fn | 首次创建vlan，成功返回vlan-oid | func_01_create_vlan_fn&nbsp; |
| 　 | 重复创建相同的vlan，返回异常 | func_02_create_same_vlan_fn |
| 　 | 创建数量超过max时，返回异常 | func_03_create_max_vlan_fn |
| sai_remove_vlan_fn | 删除已经创建了的vlan，返回执行成功 | func_04_remove_vlan_fn&nbsp; |
| 　 | 删除未创建的vlan，返回异常 | func_05_remove_not_exist_vlan_fn&nbsp; |
| sai_set_vlan_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功set，不支持的需要返回unsupport | func_06_set_and_get_vlan_attribute_fn_x |
| sai_get_vlan_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回unsupport | func_06_set_and_get_vlan_attribute_fn_x |
| sai_create_vlan_member_fn | 创建vlan member，成功返回vlan-member-oid | func_07_create_vlan_member_fn |
| 　 | 重复创建相同的vlan member，返回相同的vlan-member-oid | func_08_create_same_vlan_member_fn |
| sai_remove_vlan_member_fn | 删除已经创建了的vlan-member，返回执行成功 | func_09_remove_vlan_member_fn |
| 　 | 删除未创建的vlan-member，返回异常 | func_10_remove_not_exist_vlan_member_fn |
| sai_set_vlan_member_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功set，不支持的需要返回unsupport | func_11_set_and_get_vlan_member_attribute_fn_x |
| sai_get_vlan_member_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回unsupport | func_11_set_and_get_vlan_member_attribute_fn_x |
| sai_get_vlan_stats_fn | 发固定数量的报文转发之后，验证stats是否准确；停流情况下验证多次get stats数据是否一致 | func_12_get_vlan_stats_fn |
| sai_get_vlan_stats_ext_fn | 发固定数量的报文转发之后，验证stats是否准确；再次get stats数据时验证所有stats数据均已清零 | func_13_get_vlan_stats_ext_fn_x |
| sai_clear_vlan_stats_fn | 发包验证stats数据准确之后，clear stats，验证所有数据全部清零 | func_14_clear_vlan_stats_fn |
| sai_bulk_object_create_fn | 1.批量创建多个vlan member，返回多个oid和status<BR>2.mode为0时，如果创建过程当中出现failer情况，则立即停止创建，后续未创建的vlan member也不再创建<BR>3.mode为1时，如果创建过程当中出现failer情况，直接忽略跳过，继续创建后续的vlan member成员 | func_15_create_and_remove_vlan_members_fn_mode |
| sai_bulk_object_remove_fn | 1.批量删除多个vlan member，返回多个status<BR>2.mode为0时，如果删除过程当中出现failer情况，则立即停止删除，后续未删除的vlan member也不再删除<BR>3.mode为1时，如果删除过程当中出现failer情况，直接忽略跳过，继续删除后续的vlan member成员 | func_15_create_and_remove_vlan_members_fn_mode |

###Scenario Test

| Scenario | Test Point | Test Script |
| :---- | :---- | :---- |
| access/trunk/hybrid port | access接口出去的vlan都不带vlan tag | scenario_01_access_port |
| 　 | trunk接口出去的报文除了pvid，都带vlan tag | scenario_02_trunk_port |
| 　 | hybrid接口出去的报文可以指定哪些vlan tag携带，哪些vlan tag不携带 | scenario_03_hybrid_port |
| stp instance | stp、rstp所有vlan关联到一个stp instance下，同一个port下针对所有vlan的转发行为均一致 | scenario_04_stp_rstp |
| 　 | mstp通过将不同的vlan关联到多个stp instance上，实现同一个port下针对不同vlan不同转发行为的效果 | scenario_05_mstp |
| flood_control | per vlan 控制BUM报文的转发情况 | scenario_06_unknown_ucast |
| 　 | 　 | scenario_07_unknown_mcast |
| 　 | 　 | scenario_08_broadcast |
| max learning address | mac learn-limit per vlan 控制 | scenario_09_max_learning_address |
| learning enable/disable | per vlan 控制mac learning enable/disable | scenario_10_mac_learning_enable |
| igmp snooping | per vlan 控制igmp snooping enable/disable | scenario_11_igmp_snooping_enable |
| vlan stats | 当前sai vlan属性不支持设置statsid ，需要创建vlan时sdk自动加入statsid对vlan做统计；增加SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE属性，用于控制vlan是否支持stats；将原有sai_thrift_create_vlan接口添加一个默认参数stats_enable，且缺省值为1 | scenario_12_vlan_stats_enable |
| acl/metadata | per vlan配置ingress/egress acl实现报文匹配 | scenario_13_vlan_ingress_acl |
| 　 | 　 | scenario_14_vlan_egress_acl |
| 　 | 匹配到的报文执行相应的action操作 | scenario_15_vlan_acl_metadata |
| l2 mcast lookup key | per vlan控制l2mc是基于macda还是基于ip | scenario_16_l2_mcast_macda |
|    | 基于ip存在XG、SG、XG and SG 三种行为 | scenario_17_ipv4_l2mc |
|    |    | scenario_18_ipv6_l2mc |

##Bridge

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| SAI API | Test Point | Test Script |
| sai_create_bridge_fn | 首次创建bridge，成功返回bridge-oid | func_01_create_bridge_fn&nbsp; |
| 　 | 多次创建，返回不同的bridge-oid | func_02_create_multi_bridge_fn |
| 　 | 创建数量超过max时，返回异常 | func_03_create_max_bridge_fn |
| sai_remove_bridge_fn | 删除已经创建了的bridge，返回执行成功 | func_04_remove_bridge_fn&nbsp; |
| 　 | 删除未创建的bridge，返回异常 | func_05_remove_not_exist_bridge_fn&nbsp; |
| sai_set_bridge_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功set，不支持的需要返回unsupport | func_06_set_and_get_bridge_attribute_fn_x |
| sai_get_bridge_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回unsupport | func_06_set_and_get_bridge_attribute_fn_x |
| sai_get_bridge_stats_fn | 　 | 不支持 |
| sai_get_bridge_stats_ext_fn | 　 | 不支持 |
| sai_clear_bridge_stats_fn | 　 | 不支持 |
| sai_create_bridge_port_fn | 默认db-init的时候，会将所有物理port创建为port bridge-port，且关联到default_bridge上；创建sub bridge-port时，会先删除之前创建的port bridge-port，然后再添加sub bridge-port | func_07_create_bridge_port_fn_x |
| 　 | 重复创建sub bridge-port时，会返回相同的oid | func_08_create_same_bridge_port_fn_x |
| sai_remove_bridge_port_fn | 删除一个已经创建的sub port，会先将这个sub port删除之后，再基于这个port创建port bridge-port | func_09_remove_bridge_port_fn |
| 　 | 删除一个未创建的sub port，会返回异常 | func_10_remove_not_exist_bridge_port_fn&nbsp; |
| sai_set_bridge_port_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功set，不支持的需要返回unsupport | func_11_set_and_get_bridge_port_attribute_fn_x |
| &nbsp;&nbsp;&nbsp; sai_get_bridge_port_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回unsupport | func_11_set_and_get_bridge_port_attribute_fn_x |
| sai_get_bridge_port_stats_fn | 发固定数量的报文转发之后，验证stats是否准确，停流情况下验证多次get stats数据是否一致&nbsp; | func_12_get_bridge_port_stats_fn&nbsp; |
| &nbsp;&nbsp;&nbsp; sai_get_bridge_port_stats_ext_fn | 发固定数量的报文转发之后，验证stats是否准确，再次get stats数据时验证所有stats数据均已清零&nbsp; | func_13_get_bridge_port_stats_ext_fn&nbsp; |
| sai_clear_bridge_port_stats_fn | 发包验证stats数据准确之后，clear stats，验证所有数据全部清零&nbsp; | func_14_clear_bridge_port_stats_fn&nbsp; |


###Scenario Test

| Scenario | Test Point | Test Script |
| :---- | :---- | :---- |
| per 1d bridge 设置max learning limit | 学习到的fdb数目超过limit之后，不再学习，但报文还会继续转发 | scenario_01_bridge_max_learning_limit |
| per 1d bridge 设置mac learning disable | 使能/去使能mac learning 功能 | scenario_02_bridge_mac_learning_disable |
| per 1d bridge 控制unknown unicast flood control | 使能/去使能 unknown unicast flood功能 | scenario_03_unknown_unicast_flood_control |
| per 1d bridge 控制unknown multicast flood control | 使能/去使能 unknown multicast flood功能 | scenario_04_unknown_multicast_flood_control |
| per 1d bridge 控制broadcast flood control | 使能/去使能broadcast flood功能 | scenario_05_broadcast_flood_control |
| sub-port之间二层流量互转 | 1.同一个物理port上出多个sub-port<BR>2.多个物理port上的多个sub-port流量互转 | scenario_06_sub_port_forward |
| sub-port之间二层流量互转的同时，per sub-port控制egress方向tag-mode | 1.默认从sub-port egress方向转发出来的报文，携带svlan tag<BR>2.通过per sub-port控制egress方向转发出来的报文，是tag的还是untag的 | scenario_07_sub_port_forward_tag_mode |
| 1d-router之间三层流量互访 | 多个1d-router之间三层互访 | scenario_08_1d_router_forward |
| tunnel bridge port与tunnel nexthop绑定之后，双向流量加解封装 | 1.tunnel bridge-port egress方向加封装<BR>2.tunnel bridge-port ingress方向解封装 | scenario_09_tunnel_port_forward |
| 网络规划导致需要更新bridge-port所绑定的bridge-id | 1.切换bridge-port的bridge-id时，需要先将接口admin-state置为false<BR>2.然后flush掉相关的fdb转发表项<BR>3.再切换bridge-id<BR>4.最后再将bridge-port的admin-state置为true<BR>5.1d-router和tunnel port步骤和上面一致 | scenario_10_update_bridge_port_bridge_id |
| per bridge-port控制 max learning address and learning limit violation action | per bridge-port上控制mac学习的最大数目已经超过最大数目之后的惩罚措施 | scenario_11_bridge_port_mac_learn_num_and_violation |
| per bridge-port控制 ingress and egress 方向vlan filter | per bridge-port上控制vlan的filter，可以基于ingress方向和egress方向 | scenario_12_bridge_port_ingress_vlan_filter<BR>scenario_13_bridge_port_egress_vlan_filter |
| per bridge-port控制 isolation group | 1.per bridge-port上控制隔离组<BR>2.同一个隔离组内的bridge-port无法互访 | scenario_14_bridge_port_isolation_group |

##FDB

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_fdb_entry_fn | 添加一条fdb，可以成功执行并返回success | func_01_create_fdb_entry_fn_1q |
| 　 | 　 | func_02_create_fdb_entry_fn_1d_subport |
| 　 | 　 | func_03_create_fdb_entry_fn_tunnel_port |
| 　 | 重复添加相同的fdb，返回success | func_04_create_same_fdb_entry_fn_1q |
| 　 | 添加一条vlan-id/bridge-id/birdge-port不存在的fdb，返回异常 | func_05_create_error_fdb_entry_fn |
| sai_remove_fdb_entry_fn | 删除一条已创建的fdb，可以成功执行并返回success | func_06_remove_fdb_entry_fn |
| 　 | 删除一条未创建的fdb，返回异常 | func_07_remove_not_exist_fdb_entry_fn |
| sai_set_fdb_entry_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功set，不支持的需要返回unsupport&nbsp; | func_08_set_and_get_fdb_entry_attribute_fn |
| sai_get_fdb_entry_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回unsupport | func_08_set_and_get_fdb_entry_attribute_fn |
| sai_flush_fdb_entries_fn | 基于bridge-portid、bv-id、entry-type单个或者组合flush相应的fdb entry | func_09_flush_fdb_entry_fn |

###Scenario Test

| Scenario | Test Point | Test Script |
| :---- | :---- | :---- |
| 动态fdb learning报中断add | 芯片接收到报文之后，会触发fdb learning中断，由中断函数进行fdb的add操作 | scenario_01_fdb_learning_and_aging_port |
| 　 | 　 | scenario_02_fdb_learning_and_aging_sub_port |
| 　 | 　 | scenario_03_fdb_learning_and_aging_tunnel_port |
| 动态fdb aging报中断remove | 学习到fdb之后，芯片会不停的scan，当到达老化时间之后，触发中断函数进行fdb的remove操作 | scenario_01_fdb_learning_and_aging_port |
| 　 | 　 | scenario_02_fdb_learning_and_aging_sub_port |
| 　 | 　 | scenario_03_fdb_learning_and_aging_tunnel_port |
| fdb update时，neighbor信息需要同步更新 | fdb做station move时，neighbor信息需要同步更新 | scenario_04_fdb_fdb_station_move |
| 静态fdb可以覆盖动态fdb，但动态fdb无法无法静态fdb | 1.芯片收到源mac未知的报文会进行fdb的learning操作<BR>2.添加静态fdb表项会覆盖刚才学习的动态fdb表项 | scenario_05_fdb_fdb_entry_cover |

##STP

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_stp_fn | 首次创建stp，成功返回stp oid | func_01_create_stp_fn |
| 　 | 重复创建相同stp，返回异常 | func_02_create_same_stp_fn |
| 　 | 创建stp超过max之后，返回异常 | func_03_create_max_stp_fn |
| sai_remove_stp_fn | 删除已创建的stp，返回执行成功 | func_04_remove_stp_fn |
| 　 | 删除未创建的stp，返回异常 | func_05_remove_none_exist_stp_fn |
| sai_set_stp_attribute_fn | 按照头文件当中定义的属性id和value，set support属性正确的value，返回执行成；set unsupport属性或者value，返回异常 | func_06_set_and_get_stp_attribute_fn |
| sai_get_stp_attribute_fn | 按照头文件当中定义的属性id和value，get所有support属性，返回执行成；get所有unsupport属性或者value，返回异常 | func_06_set_and_get_stp_attribute_fn |
| sai_create_stp_port_fn | 基于port上绑定stp并设置state，成功返回stp-port oid；发包验证port state行为是否与设置一致 | func_07_create_stp_port_fn |
| sai_remove_stp_port_fn | 删除stp port，发包验证port state处于forward状态 | func_08_remove_stp_port_fn |
| sai_set_stp_port_attribute_fn | 创建完stp port之后，修改stp port state，发包验证port state行为是否与设置一致 | func_09_set_stp_port_attribute_fn |
| sai_get_stp_port_attribute_fn | 创建完stp port之后，修改stp port state，get 所有stp port属性，验证是否与设置一致 | func_09_set_stp_port_attribute_fn |
| sai_bulk_object_create_fn | 1.批量创建多个stp port，返回多个oid和status<BR>2.mode为0时，如果创建过程当中出现fail的情况，则立即停止创建，后续未创建的stp port也不再创建<BR>3.mode为1时，如果创建过程当中出现fail的情况，会忽略这个fail情况，继续创建后续的stp port | func_10_create_and_remove_stp_ports_fn_mode |
| sai_bulk_object_remove_fn | 1.批量删除多个stp port，返回多个status<BR>2.mode为0时，如果删除过程当中出现fail的情况，则立即停止删除，后续未删除的stp port也不再删除<BR>3.mode为1时，如果删除过程当中出现fail的情况，会忽略这个fail情况，继续删除后续的stp port | func_10_create_and_remove_stp_ports_fn_mode |

###Scenario Test

| Scenario | Test Point | Test Script |
| :---- | :---- | :---- |
| STP/RSTP | 所有VLAN共享一棵生成树，所有vlan均绑定到default stp oid上 | scenario_01_stp_rstp_forward |
| 　 | 所有stp port的state可以任意切换 | scenario_02_stp_rstp_learning |
| 　 | stp port state状态对ingress和egree方向的流量均生效 | scenario_03_stp_rstp_discard |
| MSTP | 通过instance使得不同的VLAN通过不同的生成树转发流量 | scenario_04_mstp_instance_ingress |
|    | 区分用户或业务流量，并实现负载分担 | scenario_05_mstp_instance_egress |

## Virtual Router

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_virtual_router_fn | 首次创建virtual router，返回正确的oid，创建时传入的attribute都正确 | func_01_create_virtual_router_fn |
| 　 | 创建到max之后，再次创建返回异常的oid | func_02_create_max_virtual_router_fn |
| sai_remove_virtual_router_fn | 删除已创建的virtual router，返回执行成功 | func_03_remove_virtual_router_fn |
| 　 | 删除未创建的virtual router，返回异常 | func_04_remove_no_exist_virtual_router_fn |
| sai_set_virtual_router_attribute_fn | set正确的attribute，返回执行成功 | func_05_virtual_router_set_and_get_attr_fn |
| sai_get_virtual_router_attribute_fn | get attribute，返回所有attribute，且都正确 | func_05_virtual_router_set_and_get_attr_fn |

###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| 改变virtual router的attr的同时改变对应的router interface的attr | scenario_01_vr_change_rif_attr |
| 压力测试 | senario_02_stress |

##Router Interface

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_router_interface | 创建port、vlan、sub和bridge等7种类型的rif，返回执行成功 | fun_01_create_rif_fn |
| 　 | 再次创建相同attribute的port、vlan和sub类型的rif，返回异常 | fun_02_create_exist_rif_fn |
| 　 | 再次创建相同attribute的bridge、loopback、mpls_router和qinq_port类型的rif，返回执行成功 | fun_03_create_same_attr_rif_fn |
| 　 | 创建到max之后，再次创建rif，返回异常 | fun_04_max_rif_fn |
| 　 | 创建支持stats的rif，最多rif和vlan的数目总和为2046，再创建时返回异常 | fun_05_create_stats_enable_rif_fn |
| remove_router_interface | remove创建的6种类型的rif，返回执行成功，get该rif，返回异常 | fun_06_remove_rif_fn |
| 　 | remove不存在的rif，返回异常，已存在的rif不受影响 | fun_07_remove_no_exist_rif_fn |
| set_router_interface_attribute | set所有支持的attribute，返回执行成功 | fun_08_set_and_get_attribute_fn |
| 　 | set新增的stats_state attribute，返回执行成功 | fun_09_rif_set_stats_state_attribute_fn |
| get_router_interface_attribute | 创建rif，get default attribute，结果与预期符合 | fun_10_rif_default_attribute_fn |
| 　 | get attribute，返回执行成功，所有结果符合预期 | fun_08_set_and_get_attribute_fn |
| get_router_interface_stats | 收发包前后get stats，统计结果正确 | fun_11_rif_get_stats_fn |
| clear_router_interface_stats | 执行clear之后再次get stats，统计结果已清0 | fun_12_rif_clear_stats_fn |
| get_router_interface_stats_ext | 做读清类型的get stats操作，统计结果正确 | fun_13_rif_get_and_clear_stats_fn |

###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| set routermac，发包测试，macda为routermac的包通过interface转发，否则不能通过该interface转发 | scenario_01_rif_routermac_test |
| set MTU，packet length大于MTU的包不能转发 | scenario_02_rif_MTU_test |
| brideg类型rif发包测试 | scenario_03_bridge_rif_test |
| set v4_state的booldata，为1时可以转发，为0是无法转发 | scenario_04_rif_v4_enabled_test |
| set v6_state的booldata，为1时可以转发，为0是无法转发 | scenario_05_rif_v6_enabled_test |
| virtual router interface发包测试 | scenario_06_virtual_rif_test |
| set stats_state测试，设置为1之后，才开始进行收发包的统计 | scenario_07_stats_state_test |
| router interface增删压力测试 | scenario_08_stress_test |

##Neighbor

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_neighbor_entry_fn | 创建一个v4 neighbor，返回执行成功 | fun_01_neighbor_v4_create_fn |
| 　 | 创建一个v6 neighbor，返回执行成功 | fun_02_neighbor_v6_create_fn |
| 　 | 再次创建已存在的v4 neighbor，返回已存在 | fun_03_neighbor_v4_create_exist_fn |
| 　 | 再次创建已存在的v4 neighbor，返回已存在 | fun_04_neighbor_v6_create_exist_fn |
| 　 | 创建到max之后，再次创建v4 neighbor，返回异常 | fun_05_neighbor_v4_max_fn |
| 　 | 创建到max之后，再次创建v6 neighbor，返回异常 | fun_06_neighbor_v6_max_fn |
| sai_remove_neighbor_entry_fn | 删除创建的v4 neighbor，返回执行成功 | fun_07_neighbor_v4_remove_fn |
| 　 | 删除创建的v6 neighbor，返回执行成功 | fun_08_neighbor_v6_remove_fn |
| 　 | 删除不存在的v4 neighbor，返回not found | fun_09_neighbor_v4_remove_no_exist_fn |
| 　 | 删除不存在的v6 neighbor，返回not found | fun_10_neighbor_v6_remove_no_exist_fn |
| sai_set_neighbor_entry_attribute_fn | set支持的属性，返回执行成功 | fun_11_neighbor_set_attribute_fn |
| 　 | set不支持的属性，返回invalid | fun_12_neighbor_set_unsupported_attribute_fn |
| sai_get_neighbor_entry_attribute_fn | get attribute，返回执行成功，且所有attribute符合预期 | fun_11_neighbor_set_attribute_fn |
| 　 | 创建neighbor，get default entry，结果符合预期 | fun_13_neighbor_get_default_attribute |
| sai_remove_all_neighbor_entries_fn | 调用接口删除所有neighbor，返回执行成功，且所有neighbor被删除 | fun_14_neighbor_remove_all_fn |

###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| v4 neighbor收包测试，能收到dst ip hit的报文 | scenario_01_neighbor_v4_receive_packet_test |
| v6 neighbor收包测试，能收到dst ip hit的报文 | scenario_02_neighbor_v6_receive_packet_test |
| dst mac收包测试，收到的报文dst mac为neighbor配置的dst mac | scenario_03_neighbor_macda_test |
| no host route收包测试，enable时收包失败，disable时收包成功 | scenario_04_neighbor_no_host_test |
| packet action收包测试，不同的action，报文对应会被转发或者丢弃 | scenario_05_neighbor_packet_action_test |
| neighbor update by fdb收包测试，vlan interface时，配置对应vlan和dst mac的interface时，能收到包，否则不能 | scenario_06_neighbor_update_by_FDB_Test |
| 先创建nexthop再创建neighbor收包测试，收包功能正常 | scenario_07_neighbor_add_by_nexthop_test |
| 创建nexthop之后，再创建删除创建neighbor，能正常创建 | scenario_08_neighbor_create_nexthop_first |
| v4 neighbor压力测试 | scenario_09_neighbor_v4_stress_test |
| v6 neighbor压力测试 | scenario_10_neighbor_v6_stress_test |

##Nexthop(ipuc)

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_next_hop | 创建一个v4 nexthop，返回执行成功 | fun_01_create_v4_nexthop_fn |
| 　 | 创建一个v6 nexthop，返回执行成功 | fun_02_create_v6_nexthop_fn |
| 　 | 再次创建已存在的v4 nexthop，返回已存在 | fun_03_create_exist_v4_nexthop_fn |
| 　 | 再次创建已存在的v4 nexthop，返回已存在 | fun_04_create_exist_v6_nexthop_fn |
| 　 | 创建多条nexthop，返回成功 | fun_05_create_nexthop_multi_fn |
| remove_next_hop | 删除创建的v4 nexthop，返回执行成功 | fun_06_remove_v4_nexthop_fn |
| 　 | 删除创建的v6 nexthop，返回执行成功 | fun_07_remove_v6_nexthop_fn |
| 　 | 删除不存在的v4 nexthop，返回not found | fun_08_remove_no_exist_v4_nexthop_fn |
| 　 | 删除不存在的v6 nexthop，返回not found | fun_09_remove_no_exist_v6_nexthop_fn |
| set_next_hop_attribute | 没有支持set的attribute | 　 |
| get_next_hop_attribute | get attribute，返回执行成功，且所有attribute符合预期 | fun_10_get_nexthop_attribute_fn |


###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| 先创建nexthop再创建neighbor，收发包测试 | scenario_01_nhop_neighbor_share_test |
| 多条路由绑定同一个nexthop，收发包测试 | scenario_02_nhop_bind_multi_route_test |

##Nexthop Group(ecmp)

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_next_hop_group | 创建一个nexthop group，返回执行成功 | fun_01_create_nexthop_group_fn |
| 　 | 创建到max之后，再创建ipmc group，返回异常 | fun_02_create_max_nexthop_group_fn |
| remove_next_hop_group | 删除创建的ipmc group，返回执行成功 | fun_03_remove_nexthop_group_fn |
| 　 | 删除不存在的ipmc group，返回异常 | fun_04_remove_no_exist_nexthop_group_fn |
| set_next_hop_group_attribute | 没有支持set的attribute | 　 |
| get_next_hop_group_attribute | get attribute，返回执行成功，且所有attribute符合预期 | fun_05_get_nexthop_group_attribute_type_fn |
| 　 | 　 | fun_06_get_nexthop_group_attribute_counterid_fn |
| 　 | 创建若干group member后，再次get attribute，返回执行成功，且结果符合预期 | fun_07_get_nexthop_group_attribute_count_fn |
| create_next_hop_group_member | 创建1个nexthop group member，返回执行成功 | fun_08_create_nexthop_group_member_fn |
| 　 | 创建属于同一个group的member到最大，再创建返回异常 | fun_09_create_max_nexthop_group_member_fn |
| remove_next_hop_group_member | 删除创建的nexthop group member，返回执行成功 | fun_10_remove_nexthop_group_member_fn |
| 　 | 删除不存在的nexthop group member，返回异常 | fun_11_remove_no_exist_nexthop_group_member_fn |
| set_next_hop_group_member_attribute | 没有支持set的attribute | 　 |
| get_next_hop_group_member_attribute | get nexthop group member attribute，返回成功，且结果符合预期 | fun_12_get_nexthop_group_member_attribute_fn |
| create_next_hop_group_members | 一次创建16个nexthop group member，返回执行成功 | fun_13_bulk_create_nexthop_group_member_fn |
| 　 | STOP_ON_ERROR模式，某一条创建失败之后，返回失败，后面的member不会再创建 | fun_14_bulk_create_stop_on_error_fn |
| 　 | IGNORE_ERROR模式，某一条创建失败之后，后面member继续创建，并返回成功 | fun_15_bulk_create_ignore_error_fn |
| remove_next_hop_group_members | 一次删除16个nexthop group member，返回执行成功 | fun_16_bulk_remove_nexthop_group_member_fn |
| 　 | STOP_ON_ERROR模式，某一条删除失败之后，返回失败，后面的member不会再删除 | fun_17_bulk_remove_stop_on_error_fn |
| 　 | IGNORE_ERROR模式，某一条删除失败之后，后面member继续删除，并返回成功 | fun_18_bulk_remove_ignore_error_fn |

###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| 创建nexthop group，统计发往这个group的20个包最终从每个member出去的个数，结果符合负载均衡的预期 | scenario_01_ecmp_test |

## Route

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_route_entry | 创建一个v4 route，返回执行成功 | fun_01_create_v4_route_fn |
| 　 | 创建一个v6 route，返回执行成功 | fun_02_create_v6_route_fn |
| 　 | 再次创建已存在的v4 route，返回已存在 | fun_03_create_exist_v4_route_fn |
| 　 | 再次创建已存在的v4 route，返回已存在 | fun_04_create_exist_v6_route_fn |
| 　 | 创建到max之后，再次创建v4 route，返回异常 | fun_05_max_v4_route_fn |
| 　 | 创建到max之后，再次创建v6 route，返回异常 | fun_06_max_v6_route_fn |
| remove_route_entry | 删除创建的v4 route，返回执行成功 | fun_07_remove_v4_route_fn |
| 　 | 删除创建的v6 route，返回执行成功 | fun_08_remove_v6_route_fn |
| 　 | 删除不存在的v4 route，返回not found | fun_09_remove_no_exist_v4_route_fn |
| 　 | 删除不存在的v6 route，返回not found | fun_10_remove_no_exist_v6_route_fn |
| set_route_entry_attribute | set支持的属性，返回执行成功 | fun_11_set_and_get_attribute_fn |
| 　 | set不支持的属性，返回not support | fun_12_set_unsupported_attribute_fn |
| get_route_entry_attribute | get attribute，返回执行成功，且所有attribute符合预期 | fun_11_set_and_get_attribute_fn |
| 　 | 创建route，get default attribute，结果符合预期 | fun_13_get_default_attribute_fn |
| create_route_entries | 一次创建100条v4 route entry，返回执行成功 | fun_14_bulk_create_v4_route_fn |
| 　 | 一次创建100条v6 route entry，返回执行成功 | fun_15_bulk_create_v6_route_fn |
| 　 | STOP_ON_ERROR模式，某一条创建失败之后，返回失败，后面的路由不会再创建 | fun_16_bulk_create_route_stop_on_error_fn |
| 　 | IGNORE_ERROR模式，某一条路由创建失败之后，后面路由继续创建，并返回成功 | fun_17_bulk_create_route_ignore_error_fn |
| remove_route_entries | 一次删除100条v4 route entry，返回执行成功 | fun_18_bulk_remove_v4_route_fn |
| 　 | 一次删除100条v6 route entry，返回执行成功 | fun_19_bulk_remove_v6_route_fn |
| 　 | STOP_ON_ERROR模式，某一条删除失败之后，返回失败，后面的路由不会再删除 | fun_20_bulk_remove_route_stop_on_error_fn |
| 　 | IGNORE_ERROR模式，某一条路由删除失败之后，后面路由继续删除，并返回成功 | fun_21_bulk_remove_route_ignore_error_fn |
| set_route_entries_attribute | 批量set route entry的attribute，每次set一种attribute，返回执行成功 | fun_22_bulk_set_route_attr_fn_1 |
| 　 | 　 | fun_22_bulk_set_route_attr_fn_2 |
| 　 | 　 | fun_22_bulk_set_route_attr_fn_3 |
| 　 | 　 | fun_22_bulk_set_route_attr_fn_4 |
| 　 | STOP_ON_ERROR模式，某一条set失败之后，返回失败，后面的路由不会继续set | fun_23_bulk_set_route_attr_stp_on_error_fn |
| 　 | IGNORE_ERROR模式，某一条路由set失败之后，后面路由继续set，并返回成功 | fun_24_bulk_set_route_attr_ignore_error_fn |
| get_route_entries_attribute | 批量get route entry的attribute，返回执行成功 | fun_22_bulk_set_route_attr_fn_1 |
| 　 | 　 | fun_22_bulk_set_route_attr_fn_2 |
| 　 | 　 | fun_22_bulk_set_route_attr_fn_3 |
| 　 | 　 | fun_22_bulk_set_route_attr_fn_4 |
| 　 | STOP_ON_ERROR模式，某一条get失败之后，返回失败，后面的路由不会继续get | fun_25_bulk_get_route_attr_stp_on_error_fn |
| 　 | IGNORE_ERROR模式，某一条路由get失败之后，后面路由继续get，并返回成功 | fun_26_bulk_get_route_attr_ignore_error_fn |

###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| v4 route entry收包测试，能收到dst ip 匹配的报文 | scenario_01_v4_route_dest_ip_match_test |
| v6 route entry收包测试，能收到dst ip 匹配的报文 | scenario_02_v6_route_dest_ip_match_test |
| v4 packet action收包测试，给v4 route entry配置不同的action，为转发时能收到包，为丢弃或者上cpu时不能收到包 | scenario_03_v4_route_action_test |
| v6 packet action收包测试，给v6 route entry配置不同的action，为转发时能收到包，为丢弃或者上cpu时不能收到包 | scenario_04_v6_route_action_test |
| v4 set nexthop测试，修改nexthop前后，出口发生变化，报文均能正常转发 | scenario_05_v4_route_nexthop_test |
| v6 set nexthop测试，修改nexthop前后，出口发生变化，报文均能正常转发 | scenario_06_v6_route_nexthop_test |
| port-rif to port-rif收发包测试(v4) | scenario_07_v4_route_phy_to_phy_test |
| port-rif to vlan-rif收发包测试(v4) | scenario_09_v4_route_phy_to_vlan_test |
| port-rif to sub-rif收发包测试(v4) | scenario_11_v4_route_phy_to_sub_test |
| port-rif to bridge-rif收发包测试(v4) | scenario_13_v4_route_phy_to_bridge_test |
| vlan-rif to port-rif收发包测试(v4) | scenario_15_v4_route_vlan_to_phy_test |
| vlan-rif to vlan-rif收发包测试(v4) | scenario_17_v4_route_vlan_to_vlan_test |
| vlan-rif to sub-rif收发包测试(v4) | scenario_19_v4_route_vlan_to_sub_test |
| vlan-rif to bridge-rif收发包测试(v4) | scenario_21_v4_route_vlan_to_bridge_test |
| sub-rif to port-rif收发包测试(v4) | scenario_23_v4_route_sub_to_phy_test |
| sub-rif to vlan-rif收发包测试(v4) | scenario_25_v4_route_sub_to_vlan_test |
| sub-rif to sub-rif收发包测试(v4) | scenario_27_v4_route_sub_to_sub_test |
| sub-rif to bridge-rif收发包测试(v4) | scenario_29_v4_route_sub_to_bridge_test |
| bridge-rif to port-rif收发包测试(v4) | scenario_31_v4_route_bridge_to_phy_test |
| bridge-rif to vlan-rif收发包测试(v4) | scenario_33_v4_route_bridge_to_vlan_test |
| bridge-rif to sub-rif收发包测试(v4) | scenario_35_v4_route_bridge_to_sub_test |
| bridge-rif to bridge-rif收发包测试(v4) | scenario_37_v4_route_bridge_to_bridge_test |
| port-rif to port-rif收发包测试(v6) | scenario_08_v6_route_phy_to_phy_test |
| port-rif to vlan-rif收发包测试(v6) | scenario_10_v6_route_phy_to_vlan_test |
| port-rif to sub-rif收发包测试(v6) | scenario_12_v6_route_phy_to_sub_test |
| port-rif to bridge-rif收发包测试(v6) | scenario_14_v4_route_phy_to_bridge_test |
| vlan-rif to port-rif收发包测试(v6) | scenario_16_v4_route_vlan_to_phy_test |
| vlan-rif to vlan-rif收发包测试(v6) | scenario_18_v4_route_vlan_to_vlan_test |
| vlan-rif to sub-rif收发包测试(v6) | scenario_20_v4_route_vlan_to_sub_test |
| vlan-rif to bridge-rif收发包测试(v6) | scenario_22_v4_route_vlan_to_bridge_test |
| sub-rif to port-rif收发包测试(v6) | scenario_24_v4_route_sub_to_phy_test |
| sub-rif to vlan-rif收发包测试(v6) | scenario_26_v4_route_sub_to_vlan_test |
| sub-rif to sub-rif收发包测试(v6) | scenario_28_v4_route_sub_to_sub_test |
| sub-rif to bridge-rif收发包测试(v6) | scenario_30_v4_route_sub_to_bridge_test |
| bridge-rif to port-rif收发包测试(v6) | scenario_32_v4_route_bridge_to_phy_test |
| bridge-rif to vlan-rif收发包测试(v6) | scenario_34_v4_route_bridge_to_vlan_test |
| bridge-rif to sub-rif收发包测试(v6) | scenario_36_v4_route_bridge_to_sub_test |
| bridge-rif to bridge-rif收发包测试(v6) | scenario_38_v4_route_bridge_to_bridge_test |
| v4 route entry收发包压力测试 | scenario_39_v4_stress_test |
| v6 route entry收发包压力测试 | scenario_40_v6_stress_test |

##L2mc

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_l2mc_group_fn | 创建l2mc group，成功执行，返回oid | func_01_create_l2mc_group_fn |
| 　 | 创建多个l2mc group，返回多个不同的oid | func_02_create_multi_l2mc_group_fn |
| 　 | 创建最大规格l2mc group之后，无法再创建新的l2mc group了，返回空oid | func_03_create_max_l2mc_group_fn |
| sai_remove_l2mc_group_fn | 删除已创建的l2mc group，成功执行，返回success | func_04_remove_l2mc_group_fn |
| 　 | 删除不存在的l2mc group，返回not found | func_05_remove_not_exist_l2mc_group_fn |
| sai_set_l2mc_group_attribute_fn | 　 | 不支持set |
| sai_get_l2mc_group_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回出错&nbsp; | func_06_get_l2mc_group_attribute_fn |
| sai_create_l2mc_group_member_fn | 创建一个l2mc group member，将bridge port和l2mc group进行绑定，返回member-oid；相同group，相同port，会提示已经存在无法create | func_07_create_l2mc_group_member_fn |
| sai_remove_l2mc_group_member_fn | 删除已创建的l2mc group member，返回success；删除不存在的l2mc group member，返回not found | func_08_remove_l2mc_group_member_fn |
| sai_set_l2mc_group_member_attribute_fn | 　 | 不支持set |
| sai_get_l2mc_group_member_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回出错&nbsp; | func_09_get_l2mc_group_member_attribute_fn |
| sai_create_mcast_fdb_entry_fn | 1.未创建mcast_fdb_entry时，收到组播报文，当作未知组播处理，flood转发<BR>2.创建了mcast_fdb_entry之后，再次收到组播报文，当作已知组播处理，在组播组当中转发 | func_10_create_mcast_fdb_entry_fn |
| sai_remove_mcast_fdb_entry_fn | 1.创建了mcast_fdb_entry之后，收到组播报文，当作已知组播处理，在组播组当中转发<BR>2.删除mcast_fdb_entry之后，再次收到组播报文，当作未知组播处理，flood转发 | func_11_remove_mcast_fdb_entry_fn |
| sai_set_mcast_fdb_entry_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功set，不支持的需要返回unsupport&nbsp; | func_12_set_and_get_mcast_fdb_entry_attribute_fn |
| sai_get_mcast_fdb_entry_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回出错 | func_12_set_and_get_mcast_fdb_entry_attribute_fn |
| sai_create_l2mc_entry_fn | 1.未创建l2_mc_entry时，收到组播报文，当作未知组播处理，flood转发<BR>2.创建了l2_mc_entry之后，再次收到组播报文，当作已知组播处理，在组播组当中转发 | func_13_create_l2mc_entry_fn |
| sai_remove_l2mc_entry_fn | 1.创建了l2_mc_entry之后，收到组播报文，当作已知组播处理，在组播组当中转发<BR>2.删除l2_mc_entry之后，再次收到组播报文，当作未知组播处理，flood转发 | func_14_remove_l2mc_entry_fn |
| sai_set_l2mc_entry_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功set，不支持的需要返回unsupport&nbsp; | func_15_set_and_get_l2mc_entry_attribute_fn |
| sai_get_l2mc_entry_attribute_fn | 按照头文件当中定义的属性列表，支持的属性可以成功get，不支持的需要返回出错 | func_15_set_and_get_l2mc_entry_attribute_fn |

###Scenario Test

| Scenario | Test Point | Test Script |
| :---- | :---- | :---- |
| mcast fdb 一条entry对应一个group | group对应的member发生改变时，entry的转发行为要同步改变 | scenario_01_update_group_member_for_one_entry |
| mcast fdb 多条entry对应一个group | group对应的member发生改变时，所有对应该group的entry转发行为都要改变 | scenario_02_update_group_member_for_multi_entry |
| l2mc 一条entry对应一个group | group对应的member发生改变时，entry的转发行为要同步改变 | scenario_03_l2mc_update_group_member_for_one_entry |
| l2mc 多条entry对应一个group | group对应的member发生改变时，所有对应该group的entry转发行为都要改变 | scenario_04_l2mc_update_group_member_for_multi_entry |
| mcast fdb entry直接更新group | entry对应的group更新之后，entry对应的转发出接口需要同步为更新之后的group所对应的member | scenario_05_update_group_id_for_multi_entry |
| l2mc entry 直接更新group | entry对应的group更新之后，entry对应的转发出接口需要同步为更新之后的group所对应的member | scenario_06_l2mc_update_group_id_for_multi_entry |
| per mcast fdb entry 出 packet action | 基于mcast fdb entry配置相应的packet action | scenario_07_set_packet_action_per_mcast_fdb_entry |
| per l2mc entry 出 packet action | 基于l2mc entry配置相应的packet action | scenario_08_set_packet_action_per_l2mc_entry |
| l2mc lookup_key_type | per vlan控制mcast lookup key type是XG还是SG | scenario_09_l2mc_lookup_key_type |
| ipmc entry bind l2mc entry | 1.创建ipmc entry时，group member当中包含vlanif，SAI内部会自动bind到相关的l2mc entry上<BR>2.l2mc entry update时，相应的ipmc entry也会自动更新<BR>3.更新的操作包含：create/remove group member，create/remove entry，set entry group-id | scenario_10_ipmc_entry_bind_l2mc_entry |
| ipmc entry bind mcast fdb entry | 1.创建ipmc entry时，group member当中包含vlanif，SAI内部会自动bind到相关的mcast fdb entry上<BR>2.mcast fdb entry update时，相应的ipmc entry也会自动更新<BR>3.更新的操作包含：create/remove group member，create/remove entry，set entry group-id | scenario_11_ipmc_entry_bind_mcast_fdb_entry |
| ipmc entry选择性绑定l2mc entry和mcast fdb entry | 1.创建ipmc entry时，group member当中包含vlanif<BR>2.创建相应的l2mc entry和mcast fdb entry，让ipmc entry自动去bind<BR>3.删除被bind的entry，验证ipmc entry会自动更新重新bind | scenario_12_ipmc_entry_auto_bind |
| ipmc sg entry 自动bind到l2mc entry的 sg、xg以及mcast fdb entry&nbsp; | 1.创建sg的ipmc entry<BR>2.创建对应的l2mc sg、xg以及mcast fdb entry<BR>3.发包验证bind的优先关系 | scenario_13_ipmc_entry_bind_order |

##Ipmc

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| SAI API | Test Point | Test Script |
| create_ipmc_group | 创建一个ipmc group，返回执行成功 | fun_01_create_ipmc_group_fn |
| 　 | 创建到max之后，再创建ipmc group，返回异常 | fun_02_create_max_ipmc_group_fn |
| remove_ipmc_group | 删除创建的ipmc group，返回执行成功 | fun_03_remove_ipmc_group_fn |
| 　 | 删除不存在的ipmc group，返回异常 | fun_04_remove_no_exist_ipmc_group_fn |
| set_ipmc_group_attribute | 没有支持set的attribute | 　 |
| get_ipmc_group_attribute | get attribute，返回执行成功，且所有attribute符合预期 | fun_05_get_ipmc_group_attribute_fn_1 |
| 　 | 创建若干group member后，再次get attribute，返回执行成功，且结果符合预期 | fun_06_get_ipmc_group_attribute_fn_2 |
| create_ipmc_group_member | 创建1个ipmc group member，返回执行成功 | fun_07_create_ipmc_group_member_fn |
| 　 | 再次创建已存在的ipmc group member，返回已存在 | fun_08_create_exist_ipmc_group_member_fn |
| remove_ipmc_group_member | 删除创建的ipmc group member，返回执行成功 | fun_09_remove_ipmc_group_member_fn |
| 　 | 删除不存在的ipmc group member，返回异常 | fun_10_remove_no_exist_ipmc_group_member_fn |
| set_ipmc_group_member_attribute | 没有支持set的attribute | 　 |
| get_ipmc_group_member_attribute | get ipmc group member attribute，返回成功，且结果符合预期 | fun_11_get_ipmc_group_member_attribute_fn |
| create_rpf_group | 创建一个rpf group，返回执行成功 | fun_12_create_rpf_group_fn |
| 　 | 创建到max之后，再创建rpf group，返回异常 | fun_13_create_max_rpf_group_fn |
| remove_rpf_group | 删除创建的rpf group，返回执行成功 | fun_14_remove_rpf_group_fn |
| 　 | 删除不存在的rpf group，返回异常 | fun_15_remove_no_exist_rpf_group_fn |
| set_rpf_group_attribute | 没有支持set的attribute | 　 |
| get_rpf_group_attribute | get attribute，返回执行成功，且所有attribute符合预期 | fun_16_get_rpf_group_attribute_fn_1 |
| 　 | 创建若干rpf group member后，再次get attribute，返回执行成功，且结果符合预期 | fun_17_get_rpf_group_attribute_fn_2 |
| create_rpf_group_member | 创建1个rpf group member，返回执行成功 | fun_18_create_rpf_group_member_fn |
| 　 | 再次创建已存在的rpf group member，返回已存在 | fun_19_create_exist_rpf_group_member_fn |
| remove_rpf_group_member | 删除创建的rpf group member，返回执行成功 | fun_20_remove_rpf_group_member_fn |
| 　 | 删除不存在的rpf group member，返回异常 | fun_21_remove_no_exist_rpf_group_member_fn |
| set_rpf_group_member_attribute | 没有支持set的attribute | 　 |
| get_rpf_group_member_attribute | get ipmc group member attribute，返回成功，且结果符合预期 | fun_22_get_rpf_group_member_attribute_fn |
| create_ipmc_entry | 创建1个ipmc entry，返回执行成功 | fun_23_create_v4_ipmc_entry_fn |
| 　 | 　 | fun_24_create_v6_ipmc_entry_fn |
| 　 | 再次创建已存在的ipmc entry，返回异常 | fun_25_create_exist_v4_ipmc_entry_fn |
| 　 | 　 | fun_26_create_exist_v6_ipmc_entry_fn |
| 　 | 创建到max之后，再次创建ipmc entry，返回异常 | fun_27_create_max_v4_ipmc_entry_fn |
| 　 | 　 | fun_28_create_max_v6_ipmc_entry_fn |
| remove_ipmc_entry | 删除创建的ipmc entry，返回执行成功 | fun_29_remove_v4_ipmc_entry_fn |
| 　 | 　 | fun_30_remove_v6_ipmc_entry_fn |
| 　 | 删除不存在的ipmc entry，返回异常 | fun_31_remove_no_exist_v4_ipmc_entry_fn |
| 　 | 　 | fun_32_remove_no_exist_v6_ipmc_entry_fn |
| set_ipmc_entry_attribute | set所有支持的attribute，返回执行成功 | fun_33_set_ipmc_entry_attribute_action_fn |
| 　 | 　 | fun_34_set_ipmc_entry_attribute_group_fn |
| 　 | 　 | fun_35_set_ipmc_entry_attribute_rpf_fn |
| get_ipmc_entry_attribute | set attribute之后再get，返回执行成功，且结果符合预期 | fun_33_set_ipmc_entry_attribute_action_fn |
| 　 | 　 | fun_34_set_ipmc_entry_attribute_group_fn |
| 　 | 　 | fun_35_set_ipmc_entry_attribute_rpf_fn |
| 　 | get default attribute，结果符合预期 | fun_36_get_ipmc_entry_default_attribute_fn |

###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| XG收发包测试(v4) | scenario_01_v4_XG_test |
| SG收发包测试(v4) | scenario_02_v4_SG_test |
| SG update RPF收发包测试(v4) | scenario_03_v4_SG_update_rpf_test |
| XG update action收发包测试(v4) | scenario_04_v4_XG_update_action_test |
| SG update action收发包测试(v4) | scenario_05_v4_SG_update_action_test |
| XG update group收发包测试(v4) | scenario_06_v4_XG_update_group_test |
| SG update group收发包测试(v4) | scenario_07_v4_SG_update_group_test |
| XG收发包测试(v6) | scenario_08_v6_XG_test |
| SG收发包测试(v6) | scenario_09_v6_SG_test |
| SG update RPF收发包测试(v6) | scenario_10_v6_SG_update_rpf_test |
| XG update action收发包测试(v6) | scenario_11_v6_XG_update_action_test |
| SG update action收发包测试(v6) | scenario_12_v6_SG_update_action_test |
| XG update group收发包测试(v6) | scenario_13_v6_XG_update_group_test |
| SG update group收发包测试(v6) | scenario_14_v6_SG_update_group_test |
| l2mc由fdb entry更新为l2mc entry，相关的ipmc表项做相应更新 | scenario_15_fdb_to_l2mc_update_ipmc_test |
| 多个ipmc entry对应同一个group，group member增删，对应出口增加或者减少 | scenario_16_v4_SG_test_multi |

## Mirror

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_mirror_session | 创建local mirror session，返回执行成功 | fun_01_create_local_mirror_session |
| 　 | 创建port_list enable的local mirror session，返回执行成功 | fun_01_create_local_mirror_session |
| 　 | 创建rspan mirror session，返回执行成功 | fun_02_create_rspan_mirror_session |
| 　 | 创建erspan mirror session，返回执行成功 | fun_03_create_erspan_mirror_session |
| remove_mirror_session | 删除以上4种mirror session，都返回执行成功 | fun_04_remove_mirror_session |
| 　 | 删除不存在的mirror session，返回异常 | fun_05_remove_no_exist_mirror_session |
| set_mirror_session_attribute | set local mirror session支持的所有attribute，返回执行成功 | fun_06_set_local_mirror_session_attribute |
| 　 | set port_list enable的local mirror session支持的所有attribute，返回执行成功 | fun_07_set_portlist_mirror_session_attribute |
| 　 | set rspan mirror session支持的所有attribute，返回执行成功 | fun_08_set_rspan_mirror_session_attribute |
| 　 | set erspan mirror session支持的所有attribute，返回执行成功 | fun_09_set_erspan_mirror_session_attribute |
| get_mirror_session_attribute | get attribute，返回执行成功，且所有attribute符合预期 | fun_06_set_local_mirror_session_attribute |
| 　 | 　 | fun_07_set_portlist_mirror_session_attribute |
| 　 | 　 | fun_08_set_rspan_mirror_session_attribute |
| 　 | 　 | fun_09_set_erspan_mirror_session_attribute |

###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| port配置ingress local mirror session收包测试 | scenario_01_ingress_local_mirror_test |
| port配置egress local mirror session收包测试 | scenario_02_egress_local_mirror_test |
| flow配置local mirror session收包测试 | scenario_03_flow_mirror_test |
| portlist enable的local mirror session收包测试 | scenario_04_portlist_local_mirror_test |
| rspan mirror session收包测试 | scenario_05_rspan_mirror_test |
| erspan mirror session收包测试 | scenario_06_erspan_mirror_test |
| local mirror session set attribute收包测试 | scenario_07_local_mirror_set_attribute_test |
| portlist enable的local mirror session set attribute收包测试 | scenario_08_portlist_local_mirror_set_attribute_test |
| rspan mirror session set attribute收包测试 | rspan不支持绑定之后update |
| erspan mirror session set attribute收包测试 | scenario_09_erspan_mirror_set_attribute_test |
| 1 port to 4 type mirror session收包测试 | scenario_10_one_port_to_multi_mirror_set_attribute_test |

## Mpls

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_inseg_entry | 分别创建三种普通mpls inseg entry，返回执行成功 | fun_01_create_mpls_inseg_entry_fn | PASS |
| 　 | 创建l3vpn inseg entry，返回执行成功 | fun_02_create_l3vpn_inseg_entry_fn | PASS |
| 　 | 创建vpls inseg entry，返回执行成功 | fun_03_create_vpls_inseg_entry_fn | PASS |
| 　 | 创建vpws inseg entry，返回执行成功 | fun_04_create_vpws_inseg_entry_fn | PASS |
| 　 | 创建vpws inseg entry，并绑定到实际的nexthop，返回执行成功 | fun_05_create_vpws_inseg_entry_binding_nexthop_fn | PASS |
| 　 | 创建已存在的inseg entry，返回异常 | fun_06_create_exist_inseg_entry_fn | PASS |
| 　 | 创建inseg entry到max，再创建返回异常 | fun_07_create_max_inseg_entry_fn | PASS |
| remove_inseg_entry | 正常删除3种类型的普通mpls inseg entry，返回执行成功 | fun_08_remove_mpls_inseg_entry_fn | PASS |
| 　 | 删除l3vpn inseg entry，返回执行成功 | fun_09_remove_l3vpn_inseg_entry_fn | PASS |
| 　 | 删除vpls inseg entry，返回执行成功 | fun_10_remove_vpls_inseg_entry_fn | PASS |
| 　 | 删除vpws inseg entry，返回执行成功 | fun_11_remove_vpws_inseg_entry_fn | PASS |
| 　 | 删除不存在的inseg entry，返回not found | fun_12_remove_no_exist_inseg_entry_fn | PASS |
| set_inseg_entry_attribute | 多次set和get action，返回执行成功，结果符合预期 | fun_14_set_inseg_entry_attr_action_fn | PASS |
| 　 | 多次set和get普通nexthop，返回执行成功，结果符合预期 | fun_15_set_inseg_entry_attr_nhop_fn | PASS |
| 　 | 多次set和get interface类型nexthop，返回执行成功，结果符合预期 | fun_16_set_inseg_entry_attr_rifnhop_fn | PASS |
| get_inseg_entry_attribute | get attribute，返回执行成功，且所有attribute符合预期 | fun_13_get_inseg_entry_attr_fn | PASS |
| create_next_hop | 创建一个mpls nexthop，返回执行成功 | fun_17_create_mpls_nexthop_fn | PASS |
| 　 | 创建一个l3vpn nexthop，返回执行成功 | fun_18_create_l3vpn_nexthop_fn | PASS |
| 　 | 创建一个l2vpn nexthop，返回执行成功 | fun_19_create_l2vpn_nexthop_fn | PASS |
| 　 | 创建mpls nexthop到max，再创建返回异常 | fun_20_create_max_mpls_nexthop_fn | PASS |
| remove_next_hop | 删除创建的mpls nexthop，返回执行成功 | fun_21_remove_mpls_nexthop_fn | PASS |
| 　 | 删除创建的l3vpn nexthop，返回执行成功 | fun_22_remove_l3vpn_nexthop_fn | PASS |
| 　 | 删除创建的l2vpn nexthop，返回执行成功 | fun_23_remove_l2vpn_nexthop_fn | PASS |
| 　 | 删除不存在的nexthop，返回异常 | fun_24_remove_no_exist_mpls_nexthop_fn | PASS |
| get_next_hop_attribute | get所有mpls nexthop的所有attribute，结果符合预期 | fun_25_get_mpls_nexthop_attr_fn | PASS |
| 　 | get所有tunnel_encap nexthop（l2vpn）的所有attribute，结果符合预期 | fun_26_get_tunnel_encap_nexthop_attr_fn | PASS |
| set_next_hop_attribute | set counter id之后get，结果符合预期 | fun_27_set_and_get_mpls_nexthop_attr_fn | PASS |
| create_es | 创建两个es，返回执行成功，oid type正确 | fun_28_create_es_fn | PASS |
| 　 | 创建已存在的es，返回exist | fun_29_create_exist_es_fn | PASS |
| 　 | 创建label相同的es和inseg entry，返回已存在 | fun_30_create_same_label_es_and_inseg_entry_fn | PASS |
| remove_es | 删除创建的es，返回执行成功 | fun_31_remove_es_fn | PASS |
| 　 | 删除不存在的es，返回not found | fun_32_remove_no_exist_es_fn | PASS |
| 　 | 删除和es label相同的inseg entry，返回失败 | fun_33_remove_same_label_es_and_inseg_entry_fn | PASS |
| set_es_attribute | 没有支持set的attribute | 　 | 　 |
| get_es_attribute | get esi label，返回成功，结果正确 | fun_34_get_es_attribute_fn | PASS |
| create_tunnel | 创建一个mpls type的tunnel，返回执行成功 | fun_35_create_mpls_tunnel_fn | PASS |
| 　 | 创建一个mpls_l2 type的tunnel，返回执行成功 | fun_36_create_mpls_l2_tunnel_fn | PASS |
| 　 | 创建两个attribute完全相同的mpls tunnel，返回执行成功 | fun_37_create_same_mpls_tunnel_fn | PASS |
| remove_tunnel | remove创建的mpls type的tunnel，返回执行成功 | fun_38_remove_mpls_tunnel_fn | PASS |
| 　 | remove创建的mpls_l2 type的tunnel，返回执行成功 | fun_39_remove_mpls_l2_tunnel_fn | PASS |
| 　 | 删除不存在的mpls tunnel，返回异常 | fun_40_remove_no_exist_mpls_tunnel_fn | PASS |
| set_tunnel_attribute | set tunnel支持set的每个attribute，返回执行成功，结果符合预期 | fun_44_set_mpls_l2_tunnel_attribute_decap_with_cw_fn | PASS |
| 　 | 　 | fun_45_set_mpls_l2_tunnel_attribute_encap_with_cw_fn | PASS |
| 　 | 　 | fun_46_set_mpls_l2_tunnel_attribute_tagged_vlan_fn | PASS |
| 　 | 　 | fun_47_set_mpls_l2_tunnel_attribute_decap_esi_valid_fn | PASS |
| 　 | 　 | fun_48_set_mpls_l2_tunnel_attribute_encap_esi_valid_fn | PASS |
| get_tunnel_attribute | get mpls type的tunnel的所有attribute，返回执行成功，结果符合预期 | fun_41_get_mpls_tunnel_attribute_fn | PASS |
| 　 | get mpls_l2 type的tunnel的所有attribute，返回执行成功，结果符合预期 | fun_42_get_mpls_l2_tunnel_attribute_fn | PASS |
| 　 | tunnel bind l3vpn之后，get tunnel的attribute nexthop，结果符合预期 | fun_43_get_mpls_tunnel_attr_nexthop_fn | PASS |

###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| basic mpls AC to PW发包测试 | scenario_01_basic_mpls_ac_to_pw_test |
| basic mpls PW to AC发包测试 | scenario_02_basic_mpls_pw_to_ac_test |
| basic mpls swap label发包测试 | scenario_03_basic_mpls_swap_test |
| basic mpls php 发包测试 | scenario_04_basic_mpls_php_test |
| l3vpn uniform模式ac to pw发包测试(exp相关问题需要后续再测一下) | scenario_05_mpls_l3vpn_ac_to_pw_test |
| l3vpn pipe模式ac to pw发包测试 | scenario_06_l3vpn_ac_to_pw_pipe_mode_test |
| l3vpn ac to pw per vrf发包测试，不同vrf的interface进来的报文，出口相同，加封装的pw label不同 | scenario_07_mpls_l3vpn_ac_to_pw_per_vrf_test |
| l3vpn uniform模式pw to ac发包测试 | scenario_08_mpls_l3vpn_pw_to_ac_test |
| l3vpn pipe模式pw to ac发包测试 | scenario_09_l3vpn_pw_to_ac_pipe_mode_test |
| l3vpn pw to ac per vrf发包测试，从同一个口进来的不同pw label的报文，出口不同，编辑行为也不同 | scenario_10_mpls_l3vpn_pw_to_ac_per_vrf_test |
| l3vpn swap label发包测试，只有lsp label发生改变，pw label和ip报文保持不变&nbsp; | scenario_11_mpls_l3vpn_swap_test |
| vpls tagged mode发包测试，ac to pw或者pw to ac，旧vlan被替换为新vlan | scenario_12_vpls_tagged_test |
| vpls raw mode发包测试，ac to pw，p-vlan被剥去，pw to ac，p-vlan被加上 | scenario_13_vpls_raw_test |
| vpws tagged mode发包测试，ac to pw或者pw to ac，旧vlan被替换为新vlan | scenario_14_vpws_tagged_test |
| vpws raw mode发包测试，ac to pw，p-vlan被剥去，pw to ac，p-vlan被加上 | scenario_15_vpws_raw_test |
| mpls sr ac to pw发包测试，一共加11个label（10个sr+1个l3vpn）（当前测试结果中ttl有些问题，后续等nexthop模块代码固定下来，需要再回头测一下） | scenario_16_mpls_sr_ac_to_pw_test |
| mpls sr lsp transmit发包测试，pop掉最外层lable，将最外层label的ttl减一，赋给下一层label | scenario_17_mpls_sr_transmit_test |
| evpn ac to pw发包测试，从同一个port发送的对应到不同bridge的报文，出去时带不同的pw label | scenario_18_evpn_ac_to_pw_test |
| evpn pw to ac发包测试，从同一port发送的带不同pw label的报文，出口和编辑行为不同 | scenario_19_evpn_pw_to_ac_test |
| evpn pw方向fdb learning disable测试 | scenario_20_evpn_learning_fdb_test |
| 使能es label相关功能，发送已知单播报文，收到的包不带es label | scenario_21_evpn_unicast_add_es_label_test |
| 使能es label相关功能，发送bum报文，收到的包带es label | scenario_22_evpn_bum_add_es_label_test |
| pw to ac时，带es label的报文不会配了同样es的port出去 | scenario_23_evpn_pw_to_ac_bum_with_es_label_test |
| 同一个port出两个对应不同bridge的ac口，删掉其中一个，对另一个的转发报文行为没有影响 | scenario_24_one_port_two_ac_and_delete_one_ac_to_pw_test |
| 同一个port出两个对应不同bridge的ac口，删掉其中一个，对另一个的接收报文行为没有影响 | scenario_25_one_port_two_ac_and_delete_one_pw_to_ac_test |
| vpls tagged mode set p-vlan测试，set之后报文打上新的vlan tag；从pw来的带新vlan tag的报文能在ac端收到 | scenario_26_vpls_set_tunnel_tagged_vlan_test |
| evpn set encap cw enable测试，set为False和True时，ac to pw的报文，分别不带和带control word | scenario_27_evpn_set_tunnel_encap_with_cw_test |
| evpn set decap cw enable测试，set为False和True时，pw to ac的不带和带control word的报文分别被正确转发 | scenario_28_evpn_set_tunnel_decap_with_cw_test |
| evpn set encap es valid测试，set为False和True时，ac to pw的报文，分别不带和带es label | scenario_29_evpn_bum_set_tunnel_encap_es_label_valid_test |
| evpn set decap es valid测试，set为False和True时，pw to ac的不带和带es label的报文分别被正确转发 | scenario_30_evpn_bum_set_tunnel_decap_es_label_valid_test |

## Ptp

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_ptp_domain | 创建一个ptp domain，返回执行成功，返回的oid正确 | func_01_create_one_ptp_domain_fn |
| 　 | 再次创建一个ptp domain，返回失败 | func_02_create_two_ptp_domain_fn |
| 　 | 先后4种device type的ptp domain，返回执行成功 | func_03_create_4_device_type_ptp_domain_fn |
| 　 | 创建包含input type tod interface的ptp domain，返回执行成功 | func_04_create_ptp_domain_fn_with_input_tod_interface |
| 　 | 创建包含output type tod interface的ptp domain，返回执行成功 | func_05_create_ptp_domain_fn_with_output_tod_interface |
| remove_ptp_domain | 删除创建的ptp domain，返回执行成功 | func_06_remove_ptp_domain_fn |
| 　 | 删除不存在的ptp domain，返回异常 | func_07_remove_no_exist_ptp_domain_fn |
| set_ptp_domain_attribute | 分别set所有支持set的attribute，返回执行成功，get到的结果符合预期 | func_12_set_ptp_domain_attr_time_offset_fn |
| 　 | 　 | func_13_set_ptp_domain_attr_drift_offset_fn |
| 　 | 　 | func_14_set_ptp_domain_attr_tod_intf_enable_and_mode_fn |
| 　 | 　 | func_15_set_ptp_domain_attr_tod_intf_leap_second_fn |
| 　 | 　 | func_16_set_ptp_domain_attr_tod_intf_pps_status_fn |
| 　 | 　 | func_17_set_ptp_domain_attr_tod_intf_pps_accuracy_fn |
| get_ptp_domain_attribute | get attribute，返回所有attribute，且都符合预期 | func_08_get_basic_ptp_domain_attr_fn |
| 　 | 　 | func_09_get_basic_ptp_domain_attr_fn_2 |
| 　 | 　 | func_10_get_output_tod_interface_ptp_domain_attr_fn |
| 　 | 　 | func_11_get_input_tod_interface_ptp_domain_attr_fn |


###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| oc device收到ptp协议报文上送cpu | scenario_01_oc_device_rx_pkt_to_cpu_test |
| bc device收到ptp协议报文上送cpu | scenario_02_bc_device_rx_pkt_to_cpu_test |
| oc device给从cpu发送的sync报文打上时间戳（直接从硬表get，测试时为0），并修改correctionfield | scenario_03_oc_device_sync_pkt_cpu_to_tx_test |
| oc device给从cpu发送的delay_req报文打上时间戳（直接从硬表get，测试时为0），并修改correctionfield（sdk bug，egress delay没有加上） | scenario_04_oc_device_delay_req_pkt_cpu_to_tx_test |
| bc device给从cpu发送的sync报文打上时间戳（直接从硬表get，测试时为0），并修改correctionfield | scenario_05_bc_device_sync_pkt_cpu_to_tx_test |
| bc device给从cpu发送的delay_req报文打上时间戳（直接从硬表get，测试时为0），并修改correctionfield（sdk bug，egress delay没有加上） | scenario_06_bc_device_delay_req_pkt_cpu_to_tx_test |
| e2etc device收到delay_resp报文，不做编辑，转发出去 | scenario_07_e2e_tc_device_delay_resp_pkt_test |
| e2etc device收到sync报文，修改correctionfield（ingress delay） | scenario_08_e2e_tc_device_sync_pkt_test |
| p2ptc device收到follow_up报文，不做编辑，转发出去 | scenario_09_p2p_tc_device_follow_up_pkt_test |
| p2ptc device收到delay_req报文，修改correctionfield（ingress delay+path delay） | scenario_10_p2p_tc_device_sync_pkt_test |

## Synce

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_synce | 创建一个synce，返回执行成功 | func_01_create_synce_fn |
| 　 | 创建一个synce之后，再次创建，返回异常 | func_02_create_another_synce_fn |
| remove_synce | remove创建的synce，返回执行成功 | func_03_remove_synce_fn |
| 　 | remove不存在的synce，返回异常 | func_04_remove_no_exist_synce_fn |
| set_synce_attribute | set和get synce的attribute CLOCK_DIVIDER，结果符合预期 | func_05_set_synce_attr_clock_divider_fn |
| 　 | set和get synce的attribute RECOVERED_PORT，结果符合预期 | func_06_set_synce_attr_recovered_port_fn |
| get_synce_attribute | get所有attribute，返回执行成功，结果符合预期 | func_07_get_synce_attr_fn |

## Lag

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_lag | 创建5种mode的lag，返回执行成功 | fun_01_create_5_mode_lag_fn |
| 　 | 创建lag到最大个数（256），再创建时返回异常 | fun_02_create_max_lag_fn |
| 　 | 创建lag到lag member的最大个数（2k），再创建时返回异常 | fun_03_create_max_lag_member_fn |
| 　 | 创建lag member invalid的5种lag，返回异常 | fun_04_create_5_mode_invalid_param_lag_fn |
| remove_lag | remove创建的lag，返回执行成功 | fun_05_remove_5_mode_lag_fn |
| 　 | remove不存在的lag，返回异常 | fun_06_remove_no_exist_lag_fn |
| set_lag_attribute | set和get SAI_LAG_ATTR_INGRESS_ACL，结果符合预期 | fun_07_set_lag_attr_igs_acl_fn |
| 　 | set和get SAI_LAG_ATTR_PORT_VLAN_ID，结果符合预期 | fun_08_set_lag_attr_pvid_fn |
| 　 | set和get SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY，结果符合预期 | fun_09_set_lag_attr_default_cos_fn |
| 　 | set和get SAI_LAG_ATTR_DROP_UNTAGGED，结果符合预期 | fun_10_set_lag_attr_drop_untagged_fn |
| 　 | set和get SAI_LAG_ATTR_DROP_TAGGED，结果符合预期 | fun_11_set_lag_attr_drop_tagged_fn |
| get_lag_attribute | 创建一个lag，get所有attribute，结果符合预期 | fun_12_get_lag_all_default_attr_fn |
| 　 | 　 | fun_13_get_lag_all_attr_fn |
| 　 | 给lag添加member，再get SAI_LAG_ATTR_PORT_LIST，结果符合预期 | fun_14_add_member_get_lag_attr_port_list_fn |
| create_lag_member | 创建一个lag member，返回执行成功 | fun_15_create_lag_member_fn |
| 　 | 创建一个已经存在于这个lag group的lag member，返回已存在 | fun_16_create_exist_lag_member_fn |
| remove_lag_member | remove创建的lag member，返回执行成功 | fun_17_remove_lag_member_fn |
| 　 | remove不存在的lag member，返回异常 | fun_18_remove_no_exist_lag_member_fn |
| set_lag_member_attribute | set和get SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE，结果符合预期 | fun_19_set_lag_member_attribute_igs_disable_fn |
| 　 | set和get SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE，结果符合预期 | fun_20_set_lag_member_attribute_egs_disable_fn |
| get_lag_member_attribute | 创建一个lag member，get所有attribute，结果符合预期 | fun_21_get_lag_member_all_attribute_fn |


###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| 用lag创建普通的属于同一vlan的bridge port，发送未知单播报文，在同一vlan内泛洪 | scenario_01_lag_bind_bridge_port_vlan_test |
| 用lag创建普通的属于同一vlan的bridge port，并创建对应的fdb，报文查fdb进行正确转发 | scenario_02_lag_bind_bridge_port_fdb_test |
| 用lag创建普通的bridge port，做增删member的操作，测试相应转发行为正确 | scenario_03_lag_bind_bridge_port_add_and_remove_member_test |
| 用同一lag创建多个bridge sub port，做相应的收发包测试 | scenario_04_lag_bind_sub_port_test |
| 用lag创建bridge sub port,并进行增删member的操作，测试相应转发行为正确 | scenario_05_lag_bind_sub_port_add_and_remove_test |
| set lag attribute drop untagged，并进行set前后的收发包对比测试 | scenario_06_lag_set_drop_untagged_test |
| set lag attribute drop tagged，并进行set前后的收发包对比测试 | scenario_07_lag_set_drop_tagged_test |
| set lag attribute port vlan id，并进行set前后的收发包对比测试 | scenario_08_lag_set_pvid_test |
| set lag attribute default vlan property，并进行set前后的收发包对比 | scenario_09_lag_set_default_vlan_cos_test |
| 用lag创建phy interface，并进行对应的收发包测试 | scenario_10_lag_bind_phyif_test |
| 用lag创建phy interface，做增删member的操作，并进行相应的收发包测试 | scenario_11_lag_bind_phyif_add_and_remove_member_test |
| 用一个lag创建多个sub interface，并进行相应的收发包测试 | scenario_12_lag_bind_subif_test |
| 用一个lag创建多个sub interface，做增删member的操作，并进行相应的收发包测试 | scenario_13_lag_bind_subif_add_and_remove_member_test |

## Policer

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| create_policer | 创建一个type为SAI_METER_TYPE_BYTES，mode为RFC2697，色盲模式的policer，bind port，返回执行成功，get所有attribute，结果符合预期 | PortRFC2697SrTCMBPSPoicer |
| 　 | 创建一个type为SAI_METER_TYPE_PACKETS，mode为RFC2697，色盲模式的policer，bind port，返回执行成功，get所有attribute，结果符合预期 | PortRFC2697SrTCMPPSPoicer |
| 　 | 创建一个type为SAI_METER_TYPE_BYTES，mode为RFC2697，色明模式的policer，bind port，返回执行成功，get所有attribute，结果符合预期 | PortRFC2697SrTCMColorAwarePoicer |
| 　 | 创建一个type为SAI_METER_TYPE_BYTES，mode为RFC2697，色盲模式，三种color报文action均为drop的policer，bind port，返回执行成功，get所有attribute，结果符合预期 | PortRFC2697SrTCMColorDropPoicer |
| 　 | 创建一个type为SAI_METER_TYPE_PACKETS，mode为RFC2698，色盲模式的policer，bind port，返回执行成功，get所有attribute，结果符合预期 | PortRFC4115TrTCMColorBlindPoicer |
| 　 | 创建一个type为SAI_METER_TYPE_PACKETS，mode为RFC2698，色明模式的policer，bind port，返回执行成功，get所有attribute，结果符合预期 | PortRFC4115TrTCMColorAwarePoicer |
| 　 | 创建一个type为SAI_METER_TYPE_BYTES，mode为RFC2698，色盲模式，三种color报文action均为drop的policer，bind port，返回执行成功，get所有attribute，结果符合预期 | PortRFC4115TrTCMColorDropPoicer |
| 　 | 创建一个type为SAI_METER_TYPE_BYTES，mode为storm control的policer，作为flood storm control attribute，bind port，返回执行成功，get相关attribute，结果符合预期 | PortStormCtlFlood |
| 　 | 创建一个type为SAI_METER_TYPE_PACKETS，mode为storm control的policer，作为multicast storm control attribute，bind port，返回执行成功，get相关attribute，结果符合预期 | PortStormCtlMcast |
| 　 | 创建一个type为SAI_METER_TYPE_PACKETS，mode为storm control的policer，作为broadcast storm control attribute，bind port，返回执行成功，get相关attribute，结果符合预期 | PortStormCtlBcast |
| 　 | port bind一个policer id之后，再bind 新的policer，get port相关attribute，执行成功，结果符合预期 | PortRFC2697SrTCMPPSPoicerResetId |
| 　 | 使能policer的stats功能，发一个包之后get policer stats，结果符合预期 | PortRFC2697SrTCMColorAwarePoicerStatsEn |
| 　 | policer bind port压力测试，共创建1600个policer，轮流bind 32个port，结果正常无误 | PolicerStressTest |
| 　 | sub-port和tunnel分别bind一个policer，set并get policer attribute，结果符合预期 | SubPortPoicer |
| 　 | sub-port bind一个policer id之后，再bind 新的policer，get port相关attribute，执行成功，结果符合预期 | SubportAndTunnelportRFC2697SrTCMPPSPoicerResetId |
| 　 | 创建两个policer，做mode不匹配的bind，返回异常 | PortBindModeNotMatchPolicer |
| 　 | 一个policer给一个port的三个stormctl attribute用，做update和remove操作，返回执行成功，结果符合预期 | PortBindThreeTypeStormctlPolicer |
| 　 | 创建两个典型的policer，对oid做check，结果符合预期 | fun_01_create_policer_fn |
| remove_policer | 删除创建的policer，返回执行成功 | fun_02_remove_policer_fn |
| 　 | 删除不存在的policer，返回异常 | fun_03_remove_no_exist_policer_fn |
| 　 | 删除bind port的policer，返回异常 | fun_04_remove_bind_port_policer_fn |
| 　 | 删除bind sub-port的policer，返回异常 | fun_05_remove_bind_bridge_port_policer_fn |
| set_policer_attribute | set和get attribute SAI_POLICER_ATTR_CBS，返回执行成功，结果符合预期，查看硬表，下的硬表同样正确 | fun_06_set_policer_attribute_cir_fn |
| 　 | set和get attribute SAI_POLICER_ATTR_CIR，返回执行成功，结果符合预期，查看硬表，下的硬表同样正确 | fun_07_set_policer_attribute_cbs_fn |
| 　 | set和get attribute SAI_POLICER_ATTR_PBS，返回执行成功，结果符合预期，查看硬表，下的硬表同样正确 | fun_08_set_policer_attribute_pir_fn |
| 　 | set和get attribute SAI_POLICER_ATTR_PIR，返回执行成功，结果符合预期，查看硬表，下的硬表同样正确 | fun_09_set_policer_attribute_pbs_fn |
| 　 | set和get attribute SAI_POLICER_ATTR_GREEN_PACKET_ACTION，返回执行成功，结果符合预期，查看硬表，下的硬表同样正确 | fun_10_set_policer_attribute_green_pkt_action_fn |
| 　 | set和get attribute SAI_POLICER_ATTR_YELLOW_PACKET_ACTION，返回执行成功，结果符合预期，查看硬表，下的硬表同样正确 | fun_11_set_policer_attribute_yellow_pkt_action_fn |
| 　 | set和get attribute SAI_POLICER_ATTR_RED_PACKET_ACTION，返回执行成功，结果符合预期，查看硬表，下的硬表同样正确 | fun_12_set_policer_attribute_red_pkt_action_fn |
| 　 | set和get attribute SAI_POLICER_ATTR_ENABLE_COUNTER_LIST，返回执行成功，结果符合预期 | fun_13_set_policer_attribute_enable_counter_list_fn |
| get_policer_attribute | 创建一个使用attribute默认值的policer，get所有支持的attribute，返回执行成功，结果符合预期 | fun_14_get_policer_default_attribute_fn |
| get_policer_stats | 先后发送两个报文，读取green packet的stats，返回执行成功，结果符合预期 | fun_15_get_policer_green_pkt_stats_fn |
| get_policer_stats_ext | 先后发送三个报文，调用读清接口，不同mode分别读取green packet的stats，返回执行成功，结果符合预期 | fun_16_get_policer_green_pkt_stats_ext_fn |
| clear_policer_stats | 发送两个报文，读取green packet的stats，再调用clear stats接口之后，再次读取green packet的stats，结果符合预期 | fun_17_clear_policer_green_pkt_stats_fn |


## Bfd

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_bfd_session_fn | 创建一个bfd session，返回success | func_01_create_bfd_session_fn |
| &nbsp; | 创建两个相同的bfd session，返回failure | func_02_create_same_bfd_session_fn |
| &nbsp; | 创建多个不同的bfd session，返回success | func_03_create_multi_bfd_session_fn |
| &nbsp; | 创建max bfd session之后，无法继续创建bfd session，返回failure | func_04_create_max_bfd_session_fn |
| sai_remove_bfd_session_fn | 删除一个已创建的bfd session，返回success | func_05_remove_bfd_session_fn |
| &nbsp; | 删除一个未创建的bfd session，返回failure | func_06_remove_not_exist_bfd_session_fn |
| sai_set_bfd_session_attribute_fn | 按照头文件当中定义的属性id和value，set所有支持的attribute，返回执行成功 | func_07_set_and_get_bfd_session_attr |
| sai_get_bfd_session_attribute_fn | 按照头文件当中定义的属性id和value，get所有支持的attribute，返回执行成功 | func_07_set_and_get_bfd_session_attr |


###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| micro bfd session tx方向发送ipv4 bfd报文出去 | scenario_01_micro_ipv4_bfd_tx_test |
| micro bfd session rx方向收到ipv4 bfd报文之后，session state修改为up | scenario_02_micro_ipv4_bfd_rx_test |
| micro bfd session tx方向发送ipv6 bfd报文出去 | scenario_03_micro_ipv6_bfd_tx_test |
| micro bfd session rx方向收到ipv6 bfd报文之后，session state修改为up | scenario_04_micro_ipv6_bfd_rx_test |
| ip bfd 采用loop方式，loop完根据ipda加vrf查表之后，将ipv4 bfd报文发送出去 | scenario_05_ipv4_bfd_tx_test |
| ip bfd 采用loop方式，收到ipv4 bfd报文之后，session state修改为up | scenario_06_ipv4_bfd_rx_test |
| ip bfd 采用指定nexthop的方式，将ipv4 报文往指定的nexthop上发送出去 | scenario_07_ipv4_bfd_tx_test_with_nh |
| ip bfd 采用loop方式，loop完根据ipda加vrf查表之后，将ipv6 bfd报文发送出去 | scenario_08_ipv6_bfd_tx_test |
| ip bfd 采用loop方式，收到ipv6 bfd报文之后，session state修改为up | scenario_09_ipv6_bfd_rx_test |
| mpls bfd session，tx方向发送携带lsp label的bfd报文 | scenario_11_mpls_ipv4_lsp_bfd_tx_and_rx_test |
| mpls bfd session，tx方向发送携带pw label的bfd报文，且bfd报文之前无ip和udp header | scenario_12_mpls_pw_vccv_raw_bfd_tx_and_rx_test |
| mpls bfd session，tx方向发送携带pw label的bfd报文，且bfd报文当中携带ipv4和udp header | scenario_13_mpls_pw_vccv_ipv4_bfd_tx_and_rx_test |
| mpls bfd session，tx方向发送携带pw label的bfd报文，且bfd报文当中携带ipv6和udp header | scenario_14_mpls_pw_vccv_ipv6_bfd_tx_and_rx_test |
| mpls tp bfd session，tx方向发送携带pw labell的bfd报文，且携带了gal header | scenario_15_mpls_tp_pw_tx_and_rx_test |
| mpls tp bfd session，tx方向发送携带pw labell的bfd报文，没有携带gal header | scenario_16_mpls_tp_pw_tx_and_rx_test_without_gal |
| mpls tp bfd session，tx方向发送携带lsp labell的bfd报文 | scenario_17_mpls_tp_lsp_tx_and_rx_test |
| mpls tp bfd session，rx方向检查BFD Tx 报文携带source mep-id tlv字段，且ach channel type为0x0023（cv报文）&nbsp; | scenario_18_mpls_tp_lsp_bfd_cv_test |
| mpls tp section bfd，tx方向不携带任何mpls label | scenario_19_mpls_tp_section_tx_and_rx_test |


## Y1731

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_y1731_meg_fn | 创建一个y1731 meg，返回success | func_01_create_y1731_meg_fn |
| &nbsp; | 创建两个相同的y1731 meg，返回failure | func_02_create_same_y1731_meg_fn |
| &nbsp; | 创建多个不同的y1731 meg，返回success | func_03_create_multi_y1731_meg_fn |
| &nbsp; | 创建max y1731 meg之后，无法继续创建y1731 meg，返回failure | func_04_create_max_y1731_meg_fn |
| sai_remove_y1731_meg_fn | 删除一个已创建的y1731 meg，返回success | func_05_remove_y1731_meg_fn |
| &nbsp; | 删除一个未创建的y1731 meg，返回failure | func_06_remove_not_exist_y1731_meg_fn |
| sai_set_y1731_meg_attribute_fn | 没有支持set的attribute | &nbsp; |
| sai_get_y1731_meg_attribute_fn | 没有支持get的attribute | &nbsp; |
| sai_create_y1731_session_fn | 创建一个y1731 session，返回success | func_07_create_y1731_session_fn |
| &nbsp; | 创建两个相同的y1731 session，返回failure | func_08_create_same_y1731_session_fn |
| &nbsp; | 创建多个不同的y1731 session，返回success | func_09_create_multi_y1731_session_fn |
| &nbsp; | 创建max y1731 session之后，无法继续创建y1731 session，返回failure | func_10_create_max_y1731_session_fn |
| sai_remove_y1731_session_fn | 删除一个已创建的y1731 session，返回success | func_11_remove_y1731_session_fn |
| &nbsp; | 删除一个未创建的y1731 session，返回failure | func_12_remove_not_exist_y1731_session_fn |
| sai_set_y1731_session_attribute_fn | 在scenario脚本中覆盖 | &nbsp; |
| sai_get_y1731_session_attribute_fn | 在scenario脚本中覆盖 | &nbsp; |
| sai_create_y1731_remote_mep_fn | 创建一个y1731 rmep，返回success | func_13_create_y1731_rmep_fn |
| &nbsp; | 创建两个相同的y1731 rmep，返回failure | func_14_create_same_y1731_rmep_fn |
| &nbsp; | 创建多个不同的y1731 rmep，返回success | func_15_create_multi_y1731_rmep_fn |
| &nbsp; | 创建max y1731 rmep之后，无法继续创建y1731 rmep，返回failure | func_16_create_max_y1731_rmep_fn |
| sai_remove_y1731_remote_mep_fn | 删除一个已创建的y1731 rmep，返回success | func_17_remove_y1731_rmep_fn |
| &nbsp; | 删除一个未创建的y1731 rmep，返回failure | func_18_remove_not_exist_y1731_rmep_fn |
| sai_set_y1731_remote_mep_attribute_fn | 在上面脚本中已覆盖 | &nbsp; |
| sai_get_y1731_remote_mep_attribute_fn | 在上面脚本中已覆盖 | &nbsp; |
| sai_get_y1731_session_lm_stats_fn | 验证网络中端到端双向丢包性能 | func_19_EthOam_DownMep_Dual_LMStats_test |



###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| 也称之为outward类型，mep向它所在的端口发送报文，即常规理解的接口向外发送报文 | scenario_01_eth_down_mep_ccm_test |
| 也称之为inward类型，mep不向它所在的端口发送报文，而是向设备的其他端口发送报文，理解上就是想广播域内的其他端口发送报文 | scenario_02_eth_up_mep_ccm_test |
| 与ping类似，指定节点收到LBM报文之后，将向源端点回应LBR报文，故障位置之前的MEP端点可以回应，故障位置之后的MEP端点无法回应，从而实现故障的定位 | scenario_03_eth_down_mep_lb_test |
| 与traceroute类似，由源端构造LTM报文，在转发到目的MEP的路径当中，MIP会回复LTR并转发LTM报文，到达目的MEP节点之后，终止LTM报文；经过上诉过程，源端点可以知晓去往远端端点的整个路径信息 | scenario_04_eth_down_mep_lt_test |
| 用于在发生错误时，通知对端MEP，在CCM当中携带；可以在CCM的RDI field当中，进行set和clear | scenario_05_eth_rdi_test |
| 基于链路级别的检测 | scenario_06_eth_link_oam_test |
| 用于统计网络中端到端的链路丢包性能；分为单向Single和双向Dual | scenario_07_eth_down_mep_lm_test |
| 用于统计网络中端到端的时延性能；分为单向1DM和双向2DM | scenario_08_eth_down_mep_dm_test |
| L2VPN场景下，per ac port+ vlan 进行oam的检测 | scenario_09_vpls_vlan_test |
| L2VPN场景下，per evc 进行oam的检测 | scenario_10_vpls_vsi_test |
| 与上诉同理 | scenario_11_vpws_vlan_test |
| 与上诉同理 | scenario_12_vpws_vsi_test |
| 基于l3if的oam检测 | scenario_13_tp_section_test |
| 基于lsp的oam检测 | scenario_14_tp_lsp_ccm_test |
| 基于pw的oam检测 | scenario_15_tp_pw_ccm_test |
| 构造相应的ccm报文，触发相应的defect中断；验证cb函数打印信息 | scenario_16_defect_test |
| 当MIP收到不等于自己级别的报文时不会进行处理，而是将其按原有路径转发；当MIP收到等于自己级别的报文时才会进行处理 | scenario_17_mip_test |

## Twamp

###API Test

| SAI API | Test Point | Test Script |
| :---- | :---- | :---- |
| sai_create_twamp_session_fn | 创建一个twamp session，返回success | func_01_create_twamp_session_fn |
| &nbsp; | 创建两个相同的twamp session，返回failure | func_02_create_same_twamp_session_fn |
| &nbsp; | 创建多个不同的twamp session，返回success | func_03_create_multi_twamp_session_fn |
| &nbsp; | 创建max twamp session之后，无法继续创建twamp session，返回failure | func_04_create_max_twamp_session_fn |
| sai_remove_twamp_session_fn | 删除一个已创建的twamp session，返回success | func_05_remove_twamp_session_fn |
| &nbsp; | 删除一个未创建的twamp session，返回failure | func_06_remove_not_exist_twamp_session_fn&nbsp; |
| sai_set_twamp_session_attribute_fn | 按照头文件当中定义的属性id和value，set support和unsupport属性的value，返回执行成功 | func_07_set_and_get_twamp_session_attr_fn&nbsp; |
| sai_get_twamp_session_attribute_fn | 按照头文件当中定义的属性id和value，get support和unsupport属性的value，返回执行成功 | func_07_set_and_get_twamp_session_attr_fn&nbsp; |
| sai_get_twamp_session_stats_fn | 创建一个twamp session之后测试正常收发包，get上诉session的stats数据，验证数据是否准确 | func_08_get_and_clear_twamp_session_stats_fn |
| sai_clear_twamp_session_stats_fn | 创建一个twamp session之后测试正常收发包；get上诉session的stats数据，验证数据是否准确；clear上诉session的stats数据之后，再次get，验证stats数据被清空 | func_08_get_and_clear_twamp_session_stats_fn |




###Scenario Test

| Scenario | Test Script |
| :---- | :---- |
| sender端能够正确组建twamp test报文，并且查找路由表之后发送出去；验证发送出去的报文的长度、tos、ttl、源目ip，源目udp port、head当中的length、checksum、时间戳等信息是否正确；sender端收到reflector端swap之后的test报文，端口上的acl能够正确匹配并上送oam engine，最终生成出相应的测试数据stats | scenario_01_sender_tx_and_rx_test |
| reflector端收到sender发送的twamp test报文之后，能够被ACL正确匹配到继而上送oam engine，并且对测试报文进行ip地址和udp port的swap编辑操作；上送oam engine之后的twamp test报文，会更新相应的seq num和timestamp等字段，并且查找路由表之后再发送出去；由于进行了swap的处理以及ts的更新，所以转发回去的test报文，udp的checksum需要更新，需要验证是否更新正确 | scenario_02_reflector_rx_and_tx_test |
| 两台设备之间，构造MPLS L3VPN环境，测试用户侧端口与用户侧端口之间的网络性能；验证最终的twamp测试stats是否正确 | scenario_03_UNI_sender_tx_and_rx_test |
| 两台设备之间，构造MPLS L3VPN环境，测试用户侧端口与用户侧端口之间的网络性能；验证最终的twamp测试stats是否正确 | scenario_04_UNI_reflector_rx_and_tx_test |
| 两台设备之间，构造MPLS L3VPN环境，测试网络侧端口与网络侧端口之间的网络性能；验证sender端报文的封装格式是否正确 | scenario_05_NNI_sender_tx_and_rx_test |
| 两台设备之间，构造MPLS L3VPN环境，测试网络侧端口与网络侧端口之间的网络性能；验证reflector端报文的封装格式是否正确 | scenario_06_NNI_reflector_rx_and_tx_test |
| 同一台设备上，同时创建上诉三种场景的twamp session，验证同时工作是否正常；同一台设备上，既是某个session的sender端，也是另一个session的reflector端，验证是否可以正常工作 | scenario_07_mix_test |
| 两台设备之间，纯ip网络，测试用户侧端口与用户侧端口之间sender端网络性能 | scenario_08_ipv6_sender_tx_and_rx_test |
| 两台设备之间，纯ip网络，测试用户侧端口与用户侧端口之间reflector端网络性能 | scenario_09_ipv6_reflector_rx_and_tx_test |
| 两台设备之间，构造MPLS L3VPN环境，测试用户侧端口与用户侧端口之间的网络性能；验证sender端报文的封装格式是否正确 | scenario_10_ipv6_UNI_sender_tx_and_rx_test |
| 两台设备之间，构造MPLS L3VPN环境，测试用户侧端口与用户侧端口之间的网络性能；验证reflector端报文的封装格式是否正确 | scenario_11_ipv6_UNI_reflector_rx_and_tx_test |
| 两台设备之间，构造MPLS L3VPN环境，测试网络侧端口与网络侧端口之间的网络性能，验证sender端报文的封装格式是否正确 | scenario_12_ipv6_NNI_sender_tx_and_rx_test |
| 两台设备之间，构造MPLS L3VPN环境，测试网络侧端口与网络侧端口之间的网络性能，验证reflector端报文的封装格式是否正确 | scenario_13_ipv6_NNI_reflector_rx_and_tx_test |
| reflector端只将报文swap回去，不对报文信息进行统计；报文的发送不再通过autogen进行 | scenario_14_reflector_light_mode_test |
