#Test Script Report

##SAI Common Scripts

| Module | Number | Module | Number | Module | Number | Module | Number | Module | Number |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| acl | 6 | hostif | 12 | L2 | 12 | L3 | 20 | mirror | 8 |


##Centec Scripts

| Module | Number | Module | Number | Module | Number | Module | Number | Module | Number |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| acl | 28 | bfd | 10 | bridge | 62 | counter | 8 | debug_counter | 7 |
| fdb | 35 | hash | 8 | hostif | 12 | ipmc | 55 | l2mc | 64 |
| mirror | 19 | mpls | 8 | mplsvpn | 8 | nat | 6 | neighbor | 26 |
| nexthop | 12 | nexthop_group | 18 | port | 69 | ptp | 5 | qos | 48 |
| route | 71 | router_interface | 21 | samplepacket | 8 | stp | 23 | switch | 75 |
| tunnel | 15 | twamp | 8 | udf | 11 | virtual_router | 7 | vlan | 50 |
| y1731 | 14 |  |  |  |  |  |  |  |  |

#Centec Test Scripts Detail

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