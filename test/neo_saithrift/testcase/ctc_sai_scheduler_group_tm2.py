import socket
from switch import *
import sai_base_test
import pdb

class fun_01_create_level0_scheduler_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)


        port = port_list[1]
        level = [0, 5]
        max_childs = [12, 8]
        parent_id = port

        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
        sys_logging("sched_group_id_root=0x%x"%sched_group_id_root)

        warmboot(self.client)
        try:
            assert(SAI_NULL_OBJECT_ID != sched_group_id_root)
            sched_group_id_root1 = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
            sys_logging("sched_group_id_root1=0x%x"%sched_group_id_root1)
            assert(SAI_NULL_OBJECT_ID == sched_group_id_root1)
        finally:
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
        
class fun_02_create_level5_scheduler_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        #create scheduler group and queue
        port = port_list[1]
        level = [0, 5]
        max_childs = [12, 8]
        root_sched_group = [None]*1
        node_sched_group = [None]*8


        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        
        node_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])      
        node_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])      
        node_sched_group[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])

        sys_logging("node_sched_group[0]=0x%x" %node_sched_group[0])
        sys_logging("node_sched_group[1]=0x%x" %node_sched_group[1])
        sys_logging("node_sched_group[2]=0x%x" %node_sched_group[2])
        sys_logging("node_sched_group[3]=0x%x" %node_sched_group[3])
        sys_logging("node_sched_group[4]=0x%x" %node_sched_group[4])
        sys_logging("node_sched_group[5]=0x%x" %node_sched_group[5])
        sys_logging("node_sched_group[6]=0x%x" %node_sched_group[6])
        sys_logging("node_sched_group[7]=0x%x" %node_sched_group[7])

        warmboot(self.client)
        try:
            assert(SAI_NULL_OBJECT_ID != node_sched_group[0])
            assert(SAI_NULL_OBJECT_ID != node_sched_group[1])
            assert(SAI_NULL_OBJECT_ID != node_sched_group[2])
            assert(SAI_NULL_OBJECT_ID != node_sched_group[3])
            assert(SAI_NULL_OBJECT_ID != node_sched_group[4])
            assert(SAI_NULL_OBJECT_ID != node_sched_group[5])
            assert(SAI_NULL_OBJECT_ID != node_sched_group[6])
            assert(SAI_NULL_OBJECT_ID != node_sched_group[7])

            node_sched_group_8 = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0]) 
            sys_logging("node_sched_group_8=0x%x"%node_sched_group_8)
            assert(SAI_NULL_OBJECT_ID == node_sched_group_8)

        finally:
            for i in node_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)


class fun_03_remove_level5_scheduler_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        #create scheduler group and queue
        port = port_list[1]
        level = [0, 5]
        max_childs = [12, 8]
        root_sched_group = [None]*1
        node_sched_group = [None]*8

        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        
        node_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])      
        node_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])      
        node_sched_group[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        node_sched_group[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])

        sys_logging("node_sched_group[0]=0x%x" %node_sched_group[0])
        sys_logging("node_sched_group[1]=0x%x" %node_sched_group[1])
        sys_logging("node_sched_group[2]=0x%x" %node_sched_group[2])
        sys_logging("node_sched_group[3]=0x%x" %node_sched_group[3])
        sys_logging("node_sched_group[4]=0x%x" %node_sched_group[4])
        sys_logging("node_sched_group[5]=0x%x" %node_sched_group[5])
        sys_logging("node_sched_group[6]=0x%x" %node_sched_group[6])
        sys_logging("node_sched_group[7]=0x%x" %node_sched_group[7])

        warmboot(self.client)
        try:
        
            for i in node_sched_group:
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_SUCCESS == attrs.status)
                status = self.client.sai_thrift_remove_scheduler_group(i)
                sys_logging("remove sched_group status=%d"%status)
                assert(SAI_STATUS_SUCCESS == status)
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get removed sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_ITEM_NOT_FOUND == attrs.status)
            for i in root_sched_group:
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_SUCCESS == attrs.status)
                status = self.client.sai_thrift_remove_scheduler_group(i)
                sys_logging("remove sched_group status=%d"%status)
                assert(SAI_STATUS_SUCCESS == status)
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get removed sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_ITEM_NOT_FOUND == attrs.status)
        finally:
            pass


            
class fun_04_basic_queue_schedule_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)


        #create scheduler profile
        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight1 = 10
        sched_weight2 = 15
        sched_weight3 = 20
        cir = 2000000
        cir2 = 2500000
        cbs = 256000
        cbs2 = 356000
        pir = 1000000
        pir2 = 1500000
        pbs = 64000
        pbs2 = 74000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir2, cbs2, pir2, pbs2)
        sched_oid5 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir2, cbs2, pir2, pbs2)
        sched_oid6 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight3, cir2, cbs2, pir2, pbs2)



        #create scheduler group and queue
        port = port_list[1]
        level = [0,5]
        max_childs = [12, 8]
        root_sched_group = [None]*1
        channel_sched_group = [None]*4
        node_sched_group = [None]*8
        basic_queueId = [None]*8


        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        
        node_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0], sched_oid4)      
        node_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0], sched_oid4)
        node_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0], sched_oid4)
        node_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0], sched_oid4)
        node_sched_group[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0], sched_oid4)      
        node_sched_group[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0], sched_oid4)
        node_sched_group[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0], sched_oid4)
        node_sched_group[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0], sched_oid4)

        queue_type = SAI_QUEUE_TYPE_ALL
        queue_index = [0,1,2,3,4,5,6,7]
        #pdb.set_trace()
        basic_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group[0], sche_id=sched_oid1)        
        basic_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group[1], sche_id=sched_oid5)
        basic_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group[1], sche_id=sched_oid6)
        basic_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group[3], sche_id=sched_oid2)
        basic_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group[4], sche_id=sched_oid6)
        basic_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group[4], sche_id=sched_oid5)
        basic_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group[4], sche_id=sched_oid6)
        basic_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group[7], sche_id=sched_oid3)
        #pdb.set_trace()




        #update scheduler group attribure parent scheduler group and scheduler profile
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid5)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[3], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[4], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[5], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[6], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[7], attr)

        attr_value = sai_thrift_attribute_value_t(oid=root_sched_group[0])
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[3], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[4], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[5], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[6], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[7], attr)
        #pdb.set_trace()

        try:
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[3])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid4:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    sys_logging("#Get Levle:", a.value.u8)
                    if a.value.u8 != level[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    sys_logging("#Get Max Childs:", a.value.u8)
                    if a.value.u8 != max_childs[1]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    #sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))

            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[4])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid4:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    sys_logging("#Get Levle:", a.value.u8)
                    if a.value.u8 != level[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    sys_logging("#Get Max Childs:", a.value.u8)
                    if a.value.u8 != max_childs[1]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 3:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    #sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))

            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[6])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    #sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))

            #update queue attribure parent scheduler group and scheduler profile
            attr_value = sai_thrift_attribute_value_t(oid=node_sched_group[3])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[5], attr)
            attr_value = sai_thrift_attribute_value_t(oid=node_sched_group[6])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_oid4)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[3], attr)
            attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[6], attr)
            #pdb.set_trace()

            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[3])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 3:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    #sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))

            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[4])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    #sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[6])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    #sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        
        finally:

            
            
            #remove all
            for i in basic_queueId:
                self.client.sai_thrift_remove_queue(i)
            for i in node_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid6)


#service_queue+sp/dwrr
class fun_05_service_queue_schedule_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)


        #create scheduler profile
        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight1 = 10
        sched_weight2 = 15
        sched_weight3 = 20
        cir = 2000000
        cir2 = 2500000
        cbs = 256000
        cbs2 = 356000
        pir = 1000000
        pir2 = 1500000
        pbs = 64000
        pbs2 = 74000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir2, cbs2, pir2, pbs2)
        sched_oid5 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir2, cbs2, pir2, pbs2)
        sched_oid6 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight3, cir2, cbs2, pir2, pbs2)

        sched_oid7 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, 30, 1000000, cbs2, pir2, pbs2)
        sched_oid8 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, 50, 500000, cbs2, pir2, pbs2)
        print sched_oid1,sched_oid2,sched_oid7



        #create scheduler group and queue
        port = port_list[1]
        level = [0,1,2,3,4,5]
        max_childs = [12, 100, 100, 100, 100, 8]
        root_sched_group = [None]*1
        level1_sched_group = [None]*4
        level2_sched_group1 = [None]*4
        level2_sched_group2 = [None]*4
        level3_sched_group1 = [None]*4
        level3_sched_group2 = [None]*4
        level3_sched_group3 = [None]*4
        level3_sched_group4 = [None]*4
        level4_sched_group1 = [None]*4
        level4_sched_group2 = [None]*4
        level4_sched_group3 = [None]*4
        level4_sched_group4 = [None]*4
        level4_sched_group5 = [None]*4
        level4_sched_group6 = [None]*4
        level4_sched_group7 = [None]*4
        level4_sched_group8 = [None]*4
        level4_sched_group9 = [None]*4
        level5_sched_group1 = [None]*8
        level5_sched_group2 = [None]*8
        level5_sched_group3 = [None]*8
        level5_sched_group4 = [None]*8
        level5_sched_group5 = [None]*8
        level5_sched_group6 = [None]*8
        level5_sched_group7 = [None]*8
        level5_sched_group8 = [None]*8
        level5_sched_group9 = [None]*8
        level5_sched_group10 = [None]*8
        level5_sched_group11 = [None]*8
        service1_queueId = [None]*8
        service2_queueId = [None]*8
        service3_queueId = [None]*8
        service4_queueId = [None]*8
        service5_queueId = [None]*8
        service6_queueId = [None]*8
        service7_queueId = [None]*8
        service8_queueId = [None]*8
        service9_queueId = [None]*8
        service10_queueId = [None]*8
        service11_queueId = [None]*8

        sched_group_service_id = [1,2,3,4,5,6,7,8,9,10,11]

        all_leve2_group = []
        all_leve3_group = []
        all_leve4_group = []
        all_leve5_group = []
        all_queue = []

        print 'create root group'
        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        print 'create level1 group'
        level1_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        
        #pdb.set_trace()
        print 'create level2 group'
        level2_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        all_leve2_group.append(level2_sched_group1)
        
        level2_sched_group2[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[3], sched_oid4)
        level2_sched_group2[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[3], sched_oid4)
        level2_sched_group2[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[3], sched_oid4)
        level2_sched_group2[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[3], sched_oid4)
        all_leve2_group.append(level2_sched_group2)

        print 'create level3 group'
        level3_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        all_leve3_group.append(level3_sched_group1)

        level3_sched_group2[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid5)
        level3_sched_group2[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid5)
        level3_sched_group2[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid5)
        level3_sched_group2[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid5)
        all_leve3_group.append(level3_sched_group2)

        level3_sched_group3[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[1], sched_oid4)
        level3_sched_group3[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[1], sched_oid4)
        level3_sched_group3[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[1], sched_oid4)
        level3_sched_group3[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[1], sched_oid4)
        all_leve3_group.append(level3_sched_group3)

        level3_sched_group4[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group2[2], sched_oid4)
        level3_sched_group4[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group2[2], sched_oid4)
        level3_sched_group4[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group2[2], sched_oid4)
        level3_sched_group4[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group2[2], sched_oid4)
        all_leve3_group.append(level3_sched_group4)
        
        print 'create level4 group'
        level4_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        all_leve4_group.append(level4_sched_group1)

        level4_sched_group2[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid6)
        level4_sched_group2[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid6)
        level4_sched_group2[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid6)
        level4_sched_group2[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid6)
        all_leve4_group.append(level4_sched_group2)

        level4_sched_group3[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[1], sched_oid5)
        level4_sched_group3[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[1], sched_oid5)
        level4_sched_group3[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[1], sched_oid5)
        level4_sched_group3[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[1], sched_oid5)
        all_leve4_group.append(level4_sched_group3)

        level4_sched_group4[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[2], sched_oid5)
        level4_sched_group4[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[2], sched_oid5)
        level4_sched_group4[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[2], sched_oid5)
        level4_sched_group4[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[2], sched_oid5)
        all_leve4_group.append(level4_sched_group4)

        level4_sched_group5[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[3], sched_oid4)
        level4_sched_group5[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[3], sched_oid4)
        level4_sched_group5[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[3], sched_oid4)
        level4_sched_group5[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[3], sched_oid4)
        all_leve4_group.append(level4_sched_group5)

        level4_sched_group6[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[3], sched_oid6)
        level4_sched_group6[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[3], sched_oid6)
        level4_sched_group6[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[3], sched_oid6)
        level4_sched_group6[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[3], sched_oid6)
        all_leve4_group.append(level4_sched_group6)

        level4_sched_group7[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group2[0], sched_oid4)
        level4_sched_group7[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group2[0], sched_oid4)
        level4_sched_group7[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group2[0], sched_oid4)
        level4_sched_group7[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group2[0], sched_oid4)
        all_leve4_group.append(level4_sched_group7)

        level4_sched_group8[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group3[3], sched_oid6)
        level4_sched_group8[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group3[3], sched_oid6)
        level4_sched_group8[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group3[3], sched_oid6)
        level4_sched_group8[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group3[3], sched_oid6)
        all_leve4_group.append(level4_sched_group8)
        
        level4_sched_group9[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group4[1], sched_oid6)
        level4_sched_group9[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group4[1], sched_oid6)
        level4_sched_group9[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group4[1], sched_oid6)
        level4_sched_group9[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group4[1], sched_oid6)
        all_leve4_group.append(level4_sched_group9)

        #pdb.set_trace()
        print 'create level5 group'
        level5_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        all_leve5_group.append(level5_sched_group1)

        level5_sched_group2[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[1])
        level5_sched_group2[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[1])
        level5_sched_group2[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[1])
        level5_sched_group2[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[1])
        level5_sched_group2[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[1])
        level5_sched_group2[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[1])
        level5_sched_group2[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[1])
        level5_sched_group2[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[1])
        all_leve5_group.append(level5_sched_group2)

        level5_sched_group3[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group2[2], sched_oid4, service_id=sched_group_service_id[2])
        level5_sched_group3[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group2[2], sched_oid4, service_id=sched_group_service_id[2])
        level5_sched_group3[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group2[2], sched_oid4, service_id=sched_group_service_id[2])
        level5_sched_group3[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group2[2], sched_oid4, service_id=sched_group_service_id[2])
        level5_sched_group3[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group2[2], sched_oid4, service_id=sched_group_service_id[2])
        level5_sched_group3[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group2[2], sched_oid4, service_id=sched_group_service_id[2])
        level5_sched_group3[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group2[2], sched_oid4, service_id=sched_group_service_id[2])
        level5_sched_group3[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group2[2], sched_oid4, service_id=sched_group_service_id[2])
        all_leve5_group.append(level5_sched_group3)

        level5_sched_group4[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[1], sched_oid4, service_id=sched_group_service_id[3])
        level5_sched_group4[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[1], sched_oid4, service_id=sched_group_service_id[3])
        level5_sched_group4[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[1], sched_oid4, service_id=sched_group_service_id[3])
        level5_sched_group4[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[1], sched_oid4, service_id=sched_group_service_id[3])
        level5_sched_group4[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[1], sched_oid4, service_id=sched_group_service_id[3])
        level5_sched_group4[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[1], sched_oid4, service_id=sched_group_service_id[3])
        level5_sched_group4[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[1], sched_oid4, service_id=sched_group_service_id[3])
        level5_sched_group4[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[1], sched_oid4, service_id=sched_group_service_id[3])
        all_leve5_group.append(level5_sched_group4)

        level5_sched_group5[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[2], sched_oid4, service_id=sched_group_service_id[4])
        level5_sched_group5[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[2], sched_oid4, service_id=sched_group_service_id[4])
        level5_sched_group5[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[2], sched_oid4, service_id=sched_group_service_id[4])
        level5_sched_group5[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[2], sched_oid4, service_id=sched_group_service_id[4])
        level5_sched_group5[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[2], sched_oid4, service_id=sched_group_service_id[4])
        level5_sched_group5[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[2], sched_oid4, service_id=sched_group_service_id[4])
        level5_sched_group5[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[2], sched_oid4, service_id=sched_group_service_id[4])
        level5_sched_group5[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group3[2], sched_oid4, service_id=sched_group_service_id[4])
        all_leve5_group.append(level5_sched_group5)

        level5_sched_group6[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group4[2], sched_oid4, service_id=sched_group_service_id[5])
        level5_sched_group6[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group4[2], sched_oid4, service_id=sched_group_service_id[5])
        level5_sched_group6[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group4[2], sched_oid4, service_id=sched_group_service_id[5])
        level5_sched_group6[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group4[2], sched_oid4, service_id=sched_group_service_id[5])
        level5_sched_group6[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group4[2], sched_oid4, service_id=sched_group_service_id[5])
        level5_sched_group6[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group4[2], sched_oid4, service_id=sched_group_service_id[5])
        level5_sched_group6[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group4[2], sched_oid4, service_id=sched_group_service_id[5])
        level5_sched_group6[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group4[2], sched_oid4, service_id=sched_group_service_id[5])
        all_leve5_group.append(level5_sched_group6)

        level5_sched_group7[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group5[2], sched_oid4, service_id=sched_group_service_id[6])
        level5_sched_group7[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group5[2], sched_oid4, service_id=sched_group_service_id[6])
        level5_sched_group7[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group5[2], sched_oid4, service_id=sched_group_service_id[6])
        level5_sched_group7[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group5[2], sched_oid4, service_id=sched_group_service_id[6])
        level5_sched_group7[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group5[2], sched_oid4, service_id=sched_group_service_id[6])
        level5_sched_group7[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group5[2], sched_oid4, service_id=sched_group_service_id[6])
        level5_sched_group7[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group5[2], sched_oid4, service_id=sched_group_service_id[6])
        level5_sched_group7[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group5[2], sched_oid4, service_id=sched_group_service_id[6])
        all_leve5_group.append(level5_sched_group7)

        level5_sched_group8[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group6[2], sched_oid4, service_id=sched_group_service_id[7])
        level5_sched_group8[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group6[2], sched_oid4, service_id=sched_group_service_id[7])
        level5_sched_group8[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group6[2], sched_oid4, service_id=sched_group_service_id[7])
        level5_sched_group8[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group6[2], sched_oid4, service_id=sched_group_service_id[7])
        level5_sched_group8[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group6[2], sched_oid4, service_id=sched_group_service_id[7])
        level5_sched_group8[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group6[2], sched_oid4, service_id=sched_group_service_id[7])
        level5_sched_group8[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group6[2], sched_oid4, service_id=sched_group_service_id[7])
        level5_sched_group8[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group6[2], sched_oid4, service_id=sched_group_service_id[7])
        all_leve5_group.append(level5_sched_group8)

        level5_sched_group9[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group7[0], sched_oid4, service_id=sched_group_service_id[8])
        level5_sched_group9[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group7[0], sched_oid4, service_id=sched_group_service_id[8])
        level5_sched_group9[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group7[0], sched_oid4, service_id=sched_group_service_id[8])
        level5_sched_group9[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group7[0], sched_oid4, service_id=sched_group_service_id[8])
        level5_sched_group9[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group7[0], sched_oid4, service_id=sched_group_service_id[8])
        level5_sched_group9[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group7[0], sched_oid4, service_id=sched_group_service_id[8])
        level5_sched_group9[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group7[0], sched_oid4, service_id=sched_group_service_id[8])
        level5_sched_group9[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group7[0], sched_oid4, service_id=sched_group_service_id[8])
        all_leve5_group.append(level5_sched_group9)

        level5_sched_group10[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        #all_leve5_group.append(level5_sched_group10)
        sys_logging("level5_sched_group10[0]=0x%x"%level5_sched_group10[0])
        sys_logging("level5_sched_group10[1]=0x%x"%level5_sched_group10[1])
        sys_logging("level5_sched_group10[2]=0x%x"%level5_sched_group10[2])
        sys_logging("level5_sched_group10[3]=0x%x"%level5_sched_group10[3])
        sys_logging("level5_sched_group10[4]=0x%x"%level5_sched_group10[4])
        sys_logging("level5_sched_group10[5]=0x%x"%level5_sched_group10[5])
        sys_logging("level5_sched_group10[6]=0x%x"%level5_sched_group10[6])
        sys_logging("level5_sched_group10[7]=0x%x"%level5_sched_group10[7])

        level5_sched_group11[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        #all_leve5_group.append(level5_sched_group11)
        sys_logging("level5_sched_group11[0]=0x%x"%level5_sched_group11[0])
        sys_logging("level5_sched_group11[1]=0x%x"%level5_sched_group11[1])
        sys_logging("level5_sched_group11[2]=0x%x"%level5_sched_group11[2])
        sys_logging("level5_sched_group11[3]=0x%x"%level5_sched_group11[3])
        sys_logging("level5_sched_group11[4]=0x%x"%level5_sched_group11[4])
        sys_logging("level5_sched_group11[5]=0x%x"%level5_sched_group11[5])
        sys_logging("level5_sched_group11[6]=0x%x"%level5_sched_group11[6])
        sys_logging("level5_sched_group11[7]=0x%x"%level5_sched_group11[7])

        for i in level5_sched_group10:
            self.client.sai_thrift_remove_scheduler_group(i)
        for i in level5_sched_group11:
            self.client.sai_thrift_remove_scheduler_group(i)

        level5_sched_group10[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        level5_sched_group10[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group8[3], sched_oid4, service_id=sched_group_service_id[9])
        all_leve5_group.append(level5_sched_group10)
        sys_logging("level5_sched_group10[0]=0x%x"%level5_sched_group10[0])
        sys_logging("level5_sched_group10[1]=0x%x"%level5_sched_group10[1])
        sys_logging("level5_sched_group10[2]=0x%x"%level5_sched_group10[2])
        sys_logging("level5_sched_group10[3]=0x%x"%level5_sched_group10[3])
        sys_logging("level5_sched_group10[4]=0x%x"%level5_sched_group10[4])
        sys_logging("level5_sched_group10[5]=0x%x"%level5_sched_group10[5])
        sys_logging("level5_sched_group10[6]=0x%x"%level5_sched_group10[6])
        sys_logging("level5_sched_group10[7]=0x%x"%level5_sched_group10[7])

        level5_sched_group11[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        level5_sched_group11[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group9[2], sched_oid4, service_id=sched_group_service_id[10])
        all_leve5_group.append(level5_sched_group11)
        sys_logging("level5_sched_group11[0]=0x%x"%level5_sched_group11[0])
        sys_logging("level5_sched_group11[1]=0x%x"%level5_sched_group11[1])
        sys_logging("level5_sched_group11[2]=0x%x"%level5_sched_group11[2])
        sys_logging("level5_sched_group11[3]=0x%x"%level5_sched_group11[3])
        sys_logging("level5_sched_group11[4]=0x%x"%level5_sched_group11[4])
        sys_logging("level5_sched_group11[5]=0x%x"%level5_sched_group11[5])
        sys_logging("level5_sched_group11[6]=0x%x"%level5_sched_group11[6])
        sys_logging("level5_sched_group11[7]=0x%x"%level5_sched_group11[7])
    
        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service1_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group1[0], sche_id=sched_oid1, service_id=sched_group_service_id[0])        
        service1_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group1[1], sche_id=sched_oid5, service_id=sched_group_service_id[0])
        service1_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group1[1], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service1_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group1[3], sche_id=sched_oid2, service_id=sched_group_service_id[0])
        service1_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group1[4], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service1_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group1[4], sche_id=sched_oid5, service_id=sched_group_service_id[0])
        service1_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group1[4], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service1_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group1[7], sche_id=sched_oid3, service_id=sched_group_service_id[0])
        all_queue.append(service1_queueId)
        
        service2_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group2[0], sche_id=sched_oid1, service_id=sched_group_service_id[1])        
        service2_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group2[1], sche_id=sched_oid5, service_id=sched_group_service_id[1])
        service2_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group2[1], sche_id=sched_oid6, service_id=sched_group_service_id[1])
        service2_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group2[3], sche_id=sched_oid2, service_id=sched_group_service_id[1])
        service2_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group2[4], sche_id=sched_oid6, service_id=sched_group_service_id[1])
        service2_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group2[4], sche_id=sched_oid5, service_id=sched_group_service_id[1])
        service2_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group2[4], sche_id=sched_oid6, service_id=sched_group_service_id[1])
        service2_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group2[7], sche_id=sched_oid3, service_id=sched_group_service_id[1])
        all_queue.append(service2_queueId)

        service3_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group3[0], sche_id=sched_oid1, service_id=sched_group_service_id[2])        
        service3_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group3[1], sche_id=sched_oid5, service_id=sched_group_service_id[2])
        service3_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group3[1], sche_id=sched_oid6, service_id=sched_group_service_id[2])
        service3_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group3[3], sche_id=sched_oid2, service_id=sched_group_service_id[2])
        service3_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group3[4], sche_id=sched_oid6, service_id=sched_group_service_id[2])
        service3_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group3[4], sche_id=sched_oid5, service_id=sched_group_service_id[2])
        service3_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group3[4], sche_id=sched_oid6, service_id=sched_group_service_id[2])
        service3_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group3[7], sche_id=sched_oid3, service_id=sched_group_service_id[2])
        all_queue.append(service3_queueId)

        service4_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group4[0], sche_id=sched_oid1, service_id=sched_group_service_id[3])        
        service4_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group4[1], sche_id=sched_oid5, service_id=sched_group_service_id[3])
        service4_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group4[1], sche_id=sched_oid6, service_id=sched_group_service_id[3])
        service4_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group4[3], sche_id=sched_oid2, service_id=sched_group_service_id[3])
        service4_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group4[4], sche_id=sched_oid6, service_id=sched_group_service_id[3])
        service4_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group4[4], sche_id=sched_oid5, service_id=sched_group_service_id[3])
        service4_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group4[4], sche_id=sched_oid6, service_id=sched_group_service_id[3])
        service4_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group4[7], sche_id=sched_oid3, service_id=sched_group_service_id[3])
        all_queue.append(service4_queueId)

        service5_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group5[0], sche_id=sched_oid1, service_id=sched_group_service_id[4])        
        service5_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group5[1], sche_id=sched_oid5, service_id=sched_group_service_id[4])
        service5_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group5[1], sche_id=sched_oid6, service_id=sched_group_service_id[4])
        service5_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group5[3], sche_id=sched_oid2, service_id=sched_group_service_id[4])
        service5_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group5[4], sche_id=sched_oid6, service_id=sched_group_service_id[4])
        service5_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group5[4], sche_id=sched_oid5, service_id=sched_group_service_id[4])
        service5_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group5[4], sche_id=sched_oid6, service_id=sched_group_service_id[4])
        service5_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group5[7], sche_id=sched_oid3, service_id=sched_group_service_id[4])
        all_queue.append(service5_queueId)

        service6_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group6[0], sche_id=sched_oid1, service_id=sched_group_service_id[5])        
        service6_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group6[1], sche_id=sched_oid5, service_id=sched_group_service_id[5])
        service6_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group6[1], sche_id=sched_oid6, service_id=sched_group_service_id[5])
        service6_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group6[3], sche_id=sched_oid2, service_id=sched_group_service_id[5])
        service6_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group6[4], sche_id=sched_oid6, service_id=sched_group_service_id[5])
        service6_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group6[4], sche_id=sched_oid5, service_id=sched_group_service_id[5])
        service6_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group6[4], sche_id=sched_oid6, service_id=sched_group_service_id[5])
        service6_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group6[7], sche_id=sched_oid3, service_id=sched_group_service_id[5])
        all_queue.append(service6_queueId)

        service7_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group7[0], sche_id=sched_oid1, service_id=sched_group_service_id[6])        
        service7_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group7[1], sche_id=sched_oid5, service_id=sched_group_service_id[6])
        service7_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group7[1], sche_id=sched_oid6, service_id=sched_group_service_id[6])
        service7_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group7[3], sche_id=sched_oid2, service_id=sched_group_service_id[6])
        service7_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group7[4], sche_id=sched_oid6, service_id=sched_group_service_id[6])
        service7_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group7[4], sche_id=sched_oid5, service_id=sched_group_service_id[6])
        service7_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group7[4], sche_id=sched_oid6, service_id=sched_group_service_id[6])
        service7_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group7[7], sche_id=sched_oid3, service_id=sched_group_service_id[6])
        all_queue.append(service7_queueId)

        service8_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group8[0], sche_id=sched_oid1, service_id=sched_group_service_id[7])        
        service8_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group8[1], sche_id=sched_oid5, service_id=sched_group_service_id[7])
        service8_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group8[1], sche_id=sched_oid6, service_id=sched_group_service_id[7])
        service8_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group8[3], sche_id=sched_oid2, service_id=sched_group_service_id[7])
        service8_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group8[4], sche_id=sched_oid6, service_id=sched_group_service_id[7])
        service8_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group8[4], sche_id=sched_oid5, service_id=sched_group_service_id[7])
        service8_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group8[4], sche_id=sched_oid6, service_id=sched_group_service_id[7])
        service8_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group8[7], sche_id=sched_oid3, service_id=sched_group_service_id[7])
        all_queue.append(service8_queueId)

        service9_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group9[0], sche_id=sched_oid1, service_id=sched_group_service_id[8])        
        service9_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group9[1], sche_id=sched_oid5, service_id=sched_group_service_id[8])
        service9_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group9[1], sche_id=sched_oid6, service_id=sched_group_service_id[8])
        service9_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group9[3], sche_id=sched_oid2, service_id=sched_group_service_id[8])
        service9_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group9[4], sche_id=sched_oid6, service_id=sched_group_service_id[8])
        service9_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group9[4], sche_id=sched_oid5, service_id=sched_group_service_id[8])
        service9_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group9[4], sche_id=sched_oid6, service_id=sched_group_service_id[8])
        service9_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group9[7], sche_id=sched_oid3, service_id=sched_group_service_id[8])
        all_queue.append(service9_queueId)

        service10_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group10[0], sche_id=sched_oid1, service_id=sched_group_service_id[9])        
        service10_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group10[1], sche_id=sched_oid5, service_id=sched_group_service_id[9])
        service10_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group10[1], sche_id=sched_oid6, service_id=sched_group_service_id[9])
        service10_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group10[3], sche_id=sched_oid2, service_id=sched_group_service_id[9])
        service10_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group10[4], sche_id=sched_oid6, service_id=sched_group_service_id[9])
        service10_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group10[4], sche_id=sched_oid5, service_id=sched_group_service_id[9])
        service10_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group10[4], sche_id=sched_oid6, service_id=sched_group_service_id[9])
        service10_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group10[7], sche_id=sched_oid3, service_id=sched_group_service_id[9])
        all_queue.append(service10_queueId)

        service11_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group11[0], sche_id=sched_oid1, service_id=sched_group_service_id[10])        
        service11_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group11[1], sche_id=sched_oid5, service_id=sched_group_service_id[10])
        service11_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group11[1], sche_id=sched_oid6, service_id=sched_group_service_id[10])
        service11_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group11[3], sche_id=sched_oid2, service_id=sched_group_service_id[10])
        service11_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group11[4], sche_id=sched_oid6, service_id=sched_group_service_id[10])
        service11_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group11[4], sche_id=sched_oid5, service_id=sched_group_service_id[10])
        service11_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group11[4], sche_id=sched_oid6, service_id=sched_group_service_id[10])
        service11_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group11[7], sche_id=sched_oid3, service_id=sched_group_service_id[10])
        all_queue.append(service11_queueId)


        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                #assert(32 == a.value.u32)
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS:
                sys_logging("get port attribute scheduler group num = %d"%a.value.u32)
                #assert (37 == a.value.u32)  
            if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST:
                sys_logging("get port attribute scheduler group list count = " ,a.value.objlist.count)
                for o_i in range(a.value.objlist.count):
                    sys_logging("the %dth scheduler group member = 0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
        
        #pdb.set_trace()
        #update queue attribure parent scheduler group and scheduler profile
        #service1_queueId
        attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group1[3])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service1_queueId[4], attr)
        self.client.sai_thrift_set_queue_attribute(service1_queueId[5], attr)
        attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group1[6])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service1_queueId[6], attr)
        
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid4)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service1_queueId[3], attr)
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service1_queueId[6], attr)

        #service2_queueId
        attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group2[0])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service2_queueId[1], attr)
        self.client.sai_thrift_set_queue_attribute(service2_queueId[2], attr)
        self.client.sai_thrift_set_queue_attribute(service2_queueId[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid4)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service2_queueId[0], attr)
        self.client.sai_thrift_set_queue_attribute(service2_queueId[3], attr)
        #pdb.set_trace()


        #update level 5 scheduler group attribure parent scheduler group and scheduler profile
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid7)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group1[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group1[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group1[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group1[3], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group1[4], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group1[5], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group1[6], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group1[7], attr)

        

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid8)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group2[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group2[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group2[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group2[3], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group2[4], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group2[5], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group2[6], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group2[7], attr)

        attr_value = sai_thrift_attribute_value_t(oid=level4_sched_group2[1])
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group4[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group4[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group4[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group4[3], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group4[4], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group4[5], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group4[6], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level5_sched_group4[7], attr)
        #pdb.set_trace()


        #update level 4 scheduler group attribure parent scheduler group and scheduler profile
        attrs = self.client.sai_thrift_get_scheduler_group_attribute(level4_sched_group2[1])
        sys_logging("get attribute status=%d"%attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                if a.value.oid != sched_oid6:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                sys_logging("#Get Levle:", a.value.u8)
                if a.value.u8 != level[4]:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                sys_logging("#Get Max Childs:", a.value.u8)
                if a.value.u8 != max_childs[4]:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                if a.value.oid != level3_sched_group1[0]:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                sys_logging("#Get Port Id:0x%x"%a.value.oid)
                if a.value.oid != port:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                sys_logging("#Get Child Count:",a.value.u32)
                if a.value.u32 != 8:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                #sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                for o_i in range(a.value.objlist.count):
                    sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid7)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group1[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group1[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group1[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group1[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid8)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group2[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group2[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group2[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group2[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=level3_sched_group1[0])
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group3[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group3[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group3[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level4_sched_group3[3], attr)

        attrs = self.client.sai_thrift_get_scheduler_group_attribute(level4_sched_group2[1])
        sys_logging("get attribute status=%d"%attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                if a.value.oid != sched_oid8:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                sys_logging("#Get Levle:", a.value.u8)
                if a.value.u8 != level[4]:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                sys_logging("#Get Max Childs:", a.value.u8)
                if a.value.u8 != max_childs[4]:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                if a.value.oid != level3_sched_group1[0]:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                sys_logging("#Get Port Id:0x%x"%a.value.oid)
                if a.value.oid != port:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                sys_logging("#Get Child Count:",a.value.u32)
                if a.value.u32 != 8:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                #sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                for o_i in range(a.value.objlist.count):
                    sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
        #pdb.set_trace()



        #update level 3 scheduler group attribure parent scheduler group and scheduler profile
        attrs = self.client.sai_thrift_get_scheduler_group_attribute(level2_sched_group2[0])
        sys_logging("get attribute status=%d"%attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                sys_logging("#Get Child Count:",a.value.u32)
                if a.value.u32 != 0:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                for o_i in range(a.value.objlist.count):
                    sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                    
        attrs = self.client.sai_thrift_get_scheduler_group_attribute(level3_sched_group1[0])
        sys_logging("get attribute status=%d"%attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                if a.value.oid != sched_oid4:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                sys_logging("#Get Levle:", a.value.u8)
                if a.value.u8 != level[3]:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                sys_logging("#Get Max Childs:", a.value.u8)
                if a.value.u8 != max_childs[3]:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                if a.value.oid != level2_sched_group1[0]:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                sys_logging("#Get Port Id:0x%x"%a.value.oid)
                if a.value.oid != port:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                sys_logging("#Get Child Count:",a.value.u32)
                if a.value.u32 != 12:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                for o_i in range(a.value.objlist.count):
                    sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                    
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid7)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group1[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group1[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group1[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group1[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid8)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group2[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group2[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group2[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group2[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=level2_sched_group2[0])
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group1[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group1[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group1[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group1[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=level2_sched_group2[2])
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group3[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group3[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group3[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level3_sched_group3[3], attr)

        attrs = self.client.sai_thrift_get_scheduler_group_attribute(level2_sched_group2[0])
        sys_logging("get attribute status=%d"%attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                sys_logging("#Get Child Count:",a.value.u32)
                if a.value.u32 != 4:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                for o_i in range(a.value.objlist.count):
                    sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                    
        attrs = self.client.sai_thrift_get_scheduler_group_attribute(level3_sched_group1[0])
        sys_logging("get attribute status=%d"%attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                if a.value.oid != sched_oid7:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                sys_logging("#Get Levle:", a.value.u8)
                if a.value.u8 != level[3]:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                sys_logging("#Get Max Childs:", a.value.u8)
                if a.value.u8 != max_childs[3]:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                if a.value.oid != level2_sched_group2[0]:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                sys_logging("#Get Port Id:0x%x"%a.value.oid)
                if a.value.oid != port:
                    raise NotImplementedError() 
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                sys_logging("#Get Child Count:",a.value.u32)
                if a.value.u32 != 12:
                    raise NotImplementedError()
            if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                for o_i in range(a.value.objlist.count):
                    sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
        #pdb.set_trace()


        #update level 2 scheduler group attribure parent scheduler group and scheduler profile
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid8)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level2_sched_group1[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level2_sched_group1[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level2_sched_group1[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level2_sched_group1[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=level1_sched_group[3])
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level2_sched_group1[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level2_sched_group1[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level2_sched_group1[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level2_sched_group1[3], attr)
        #pdb.set_trace()


        #update level 1 scheduler group attribure parent scheduler group and scheduler profile,do nothing
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid8)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(level1_sched_group[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level1_sched_group[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level1_sched_group[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(level1_sched_group[3], attr)
        #pdb.set_trace()



        #remove all
        for j in all_queue:
            for i in j:
                self.client.sai_thrift_remove_queue(i)
        #pdb.set_trace()
        for j in all_leve5_group:
            for i in j:
                self.client.sai_thrift_remove_scheduler_group(i)
        #pdb.set_trace()
        for j in all_leve4_group:
            for i in j:
                self.client.sai_thrift_remove_scheduler_group(i)
        #pdb.set_trace()
        for j in all_leve3_group:
            for i in j:
                self.client.sai_thrift_remove_scheduler_group(i)
        for j in all_leve2_group:
            for i in j:
                self.client.sai_thrift_remove_scheduler_group(i)
        for i in level1_sched_group:
            self.client.sai_thrift_remove_scheduler_group(i)
        for i in root_sched_group:
            self.client.sai_thrift_remove_scheduler_group(i)
        self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
        self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
        self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
        self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
        self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
        self.client.sai_thrift_remove_scheduler_profile(sched_oid6)
        self.client.sai_thrift_remove_scheduler_profile(sched_oid7)
        self.client.sai_thrift_remove_scheduler_profile(sched_oid8)








