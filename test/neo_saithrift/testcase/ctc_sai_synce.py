# Copyright 2013-present Centec Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Thrift SAI interface synceE tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask
import pdb

@group('synce')

class func_01_create_synce_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        recovered_port = 1
        clock_divider = 1
        syncE_oid = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)
        sys_logging("###the syncE_oid %x ###" %syncE_oid)
        try:
            assert(0 != syncE_oid)
            
        finally:
            self.client.sai_thrift_remove_synce(syncE_oid)


class func_02_set_synce_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        recovered_port = 1
        clock_divider = 1
        syncE_oid = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)
        clock_divider1 =7
        sys_logging("###the syncE_oid %x ###" %syncE_oid)
        attr_value = sai_thrift_attribute_value_t(u16=clock_divider1)
        attr = sai_thrift_attribute_t(id=SAI_SYNCE_ATTR_CLOCK_DIVIDER, value=attr_value)
        self.client.sai_thrift_set_synce_attribute(syncE_oid, attr)
        attrs = self.client.sai_thrift_get_synce_attribute(syncE_oid)
        
        for a in attrs.attr_list:
                if a.id == SAI_SYNCE_ATTR_RECOVERED_PORT:
                    print "SyncE lport is %d" %a.value.u16

                if a.id == SAI_SYNCE_ATTR_CLOCK_DIVIDER:
                    print " SyncE divider 0x%lx" %a.value.u16
                    if a.value.u16 != clock_divider1:
                        raise NotImplementedError()

        try:
            assert(0 != syncE_oid)
            
        finally:
            self.client.sai_thrift_remove_synce(syncE_oid)

