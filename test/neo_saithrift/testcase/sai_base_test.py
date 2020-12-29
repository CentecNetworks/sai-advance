"""
Base classes for test cases

Tests will usually inherit from one of these classes to have the controller
and/or dataplane automatically set up.
"""

import os
import logging
import unittest


import ptf
from ptf.base_tests import BaseTest
from ptf import config
import ptf.dataplane as dataplane
import ptf.testutils as testutils
import sys
import pypxr
from scapy.config import *
from scapy.layers.all import *
import ptf.mask as mask
import pdb


#########################
# packet switch
############################
import subprocess as mysub
import shlex as myshl

if sys.version_info[0] > 2:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse
from thrift.transport import TTransport, TSocket, TSSLSocket, THttpClient
from thrift.protocol.TJSONProtocol import TJSONProtocol   
from thrift.protocol.TBinaryProtocol import TBinaryProtocol  
import switch_sai.switch_sai_rpc  as switch_sai_rpc


interface_to_front_mapping = {}
port_map_loaded=0

def sys_logging(*args):
    logging.debug(args)
    print(args)

def hexstr_to_ascii(h):
    list_s = []
    for i in range(0, len(h), 2):
        list_s.append(chr(int(h[i:i+2],16)))
    return ''.join(list_s)
    
def str_to_hex(s):
    list_h = []
    for c in s:
        list_h.append(str(hex(ord(c))[2:]))
    return ''.join(list_h)
    
class ThriftInterface(BaseTest):
    def __init__(self, thrift_port=9199, use_pswitch=1):
        unittest.TestCase.__init__(self)
        config["use_pswitch"] = use_pswitch
        config["thrift_port"] = ptf.config["thirft_port"]
        if 'goldengate' == testutils.test_params_get()['chipname']:
            print "load default_interface_to_front_map_gg.ini"
            config["port_map_file"] = os.path.join(ptf.config['test_dir'], 'default_interface_to_front_map_gg.ini')
        elif 'tsingma_mx' == testutils.test_params_get()['chipname']:
            print "load default_interface_to_front_map_tmmx.ini"
            config["port_map_file"] = os.path.join(ptf.config['test_dir'], 'default_interface_to_front_map_tmmx.ini')
        else:
            #tsingma
            print "load default_interface_to_front_map.ini"
            config["port_map_file"] = os.path.join(ptf.config['test_dir'], 'default_interface_to_front_map.ini')
        
        ################################################################
        #
        # Thrift interface base tests
        #
        ################################################################
        if config["use_pswitch"] == 0:
            import switch_sai_thrift.switch_sai_rpc as switch_sai_rpc
            from thrift.transport import TSocket
            from thrift.transport import TTransport
            from thrift.protocol import TBinaryProtocol
        
        if config["use_pswitch"] == 1:
            if sys.version_info[0] > 2:
                from urllib.parse import urlparse
            else:
                from urlparse import urlparse
            from thrift.transport import TTransport, TSocket, TSSLSocket, THttpClient
            from thrift.protocol.TJSONProtocol import TJSONProtocol   
            from thrift.protocol.TBinaryProtocol import TBinaryProtocol            
            import switch_sai.switch_sai_rpc  as switch_sai_rpc
        
		
        return


    def loadPortMap(self):
        print(config)
        if config["use_pswitch"] == 0:
            global port_map_loaded
            if port_map_loaded:
                print 'port_map already loaded'
                return

                if self.test_params.has_key("port_map"):
              
                 user_input = self.test_params['port_map']
                 splitted_map = user_input.split(",")
                 for item in splitted_map:
                    interface_front_pair = item.split("@")
                    interface_to_front_mapping[interface_front_pair[0]] = interface_front_pair[1]
            elif self.test_params.has_key("port_map_file"):
                user_input = self.test_params['port_map_file']
                f = open(user_input, 'r')
                for line in f:
                    if (len(line) > 0 and (line[0] == '#' or line[0] == ';' or line[0]=='/')):
                        continue;
                    interface_front_pair = line.split("@")
                    interface_to_front_mapping[interface_front_pair[0]] = interface_front_pair[1].strip()
            else:
                exit("No ptf interface<-> switch front port mapping, please specify as parameter or in external file")    
            return
        if config["use_pswitch"] == 1:
            global port_map_loaded
            if port_map_loaded:
                print 'port_map already loaded'
                return
            user_input = config['port_map_file']
            f = open(user_input, 'r')
            for line in f:
                if (len(line) > 0 and (line[0] == '#' or line[0] == ';' or line[0]=='/')):
                    continue;
                interface_front_pair = line.split("@")
                interface_to_front_mapping[interface_front_pair[0]] = interface_front_pair[1].strip()   
            return
           #sock_file="/data01/users/systest/yangsj/xxxsock/mysock"
           #cap_file="mytestpkt.txt"
           #send_file ="mytestsend.txt"
           #self.pypxr = pypxr.pypxr(sock_file)
           #self.pypxr.sendlogfile(send_file)
           #return
           #pswitch_cmd = myshl.split(self.test_params.has_key["pswitch_cmd"])
           #printf("INFO: Packet swtich started with CMD: " + pswitch_cmd)
           #self.packet_swtich=mysub.Popen(pswitch_cmd)
           #sleep(1)




    def createRpcClient(self):
        # Set up thrift client and contact server
        if config["use_pswitch"] == 0:
            if self.test_params.has_key("server"):
                server = self.test_params['server']
            else:
                server = 'localhost'
            
            self.transport = TSocket.TSocket(server, 9092)
            self.transport = TTransport.TBufferedTransport(self.transport)
            self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

            self.client = switch_sai_rpc.Client(self.protocol)
            self.transport.open()
            return

        if config["use_pswitch"] == 1:
            if self.test_params.has_key("server"):
                server = self.test_params['server']
            else:
                server = 'localhost'
            #demo try
            ##### port use 65001
            #server = '10.10.39.187'
            self.transport = TSocket.TSocket(server, config["thrift_port"])
            self.transport = TTransport.TFramedTransport(self.transport)
            #self.protocol = TJSONProtocol(self.transport)
            self.protocol = TBinaryProtocol(self.transport)

            self.client = switch_sai_rpc.Client(self.protocol)
            self.transport.open()
            return    
 
    def setUp(self):
        if config["use_pswitch"] == 0:
            global interface_to_front_mapping
            BaseTest.setUp(self)
            self.test_params = testutils.test_params_get()
            self.loadPortMap()
            self.createRpcClient()
            return

        if config["use_pswitch"] == 1:
            BaseTest.setUp(self)
            self.test_params = testutils.test_params_get()
            self.loadPortMap()
            self.createRpcClient()
            return

    def tearDown(self):
        if config["use_pswitch"] == 0:
            if config["log_dir"] != None:
                self.dataplane.stop_pcap()
            BaseTest.tearDown(self)
            self.transport.close()
        if config["use_pswitch"] == 1:  
            if config["log_dir"] != None:
                self.dataplane.stop_pcap()
            
            dump_status = self.client.sai_thrift_dump_log("dump_all.txt")
            print "dump_status = %d" % dump_status
            
            import filecmp
            dump_file_result = filecmp.cmp('../dump_golden.txt','../dump_all.txt')
            print "dump compare:" , dump_file_result
            if dump_file_result==False:
                self.fail("Dump DB is not same as the golden DB, please check! Check golden file: dump_golden.txt. Check file: dump_all.txt \n")
        
            BaseTest.tearDown(self)
            self.transport.close()


class ThriftInterfaceDataPlane(ThriftInterface):
    """
    Root class that sets up the thrift interface and dataplane
    """
    def setUp(self):
        if config["use_pswitch"] == 0:
            ThriftInterface.setUp(self)
            self.dataplane = ptf.dataplane_instance
            if self.dataplane != None:
                self.dataplane.flush()
                if config["log_dir"] != None:
                    filename = os.path.join(config["log_dir"], str(self)) + ".pcap"
                    self.dataplane.start_pcap(filename)

        if config["use_pswitch"] == 1:
            ThriftInterface.setUp(self)
            self.dataplane = ptf.dataplane_instance
            if self.dataplane != None:
                #demotry
                self.dataplane.pxr_start(config)
                self.dataplane.pxr_capture_start()
                self.dataplane.flush()
                if config["log_dir"] != None:
                    filename = os.path.join(config["log_dir"], str(self)) + ".pcap"
                    self.dataplane.start_pcap(filename)        
            return

    def tearDown(self):
        if config["use_pswitch"] == 0:
            if config["log_dir"] != None:
                self.dataplane.stop_pcap()
            ThriftInterface.tearDown(self)

        if config["use_pswitch"] == 1:
            #demotry
            self.dataplane.pxr_capture_stop()
            ###self.dataplane.pxr_stop()
            if config["log_dir"] != None:
                self.dataplane.stop_pcap()
            ThriftInterface.tearDown(self)
    
    def ctc_send_packet(self, port_id, pkt, count=1):
        device, port = testutils.port_to_tuple(port_id)
        sendport = port + 1
        for n in range(count):
            testutils.pxr_send(self,sendport, str(pkt))    
        time.sleep(3)
        testutils.pxr_getPacketBuffer(self)
        return
        
    def ctc_verify_packets(self, pkt, ports=[], cmpSeq=None, device_number=0):
        for device, port in testutils.ptf_ports():
            if device != device_number:
                continue
            if port in ports:
                rcvport = port + 1   
                testutils.pxr_verify(self, rcvport, pkt, cmpSeq)
                
        return
                    
    def ctc_verify_packet(self, pkt, port_id, cmpSeq=None):
        #testutils.pxr_getPacketBuffer(self)
        rcvport = port_id + 1   
        testutils.pxr_verify(self, rcvport, pkt, cmpSeq)
        return
        
    def ctc_verify_no_packet(self, pkt, port_id, timeout=None):
        print "verify no packet"
        #testutils.pxr_getPacketBuffer(self)
        rcvport = port_id + 1  
        #cmpPkt = pkt.encode('hex')
        srcPkt = self.dataplane.pxr_getPktData(rcvport, None)
        if len(srcPkt) == 0:
            return
        else:
            self.fail("Expected no packets received on port %d. \n" %(port_id))
        return
        
    def ctc_verify_any_packet_any_port(self, pkts=[], ports=[], device_number=0):
        print "verify any packet any port"
        #pdb.set_trace()
        #testutils.pxr_getPacketBuffer(self)
        match_index = 0
        totalrcv = 0
        for pkt in pkts:
            packetrcv = 0
            use_pkt_match = 0
            if isinstance(pkt, mask.Mask):
                if not pkt.is_valid():
                    assert(1)
                use_pkt_match = 1
            else :
                cmpPkt = str(pkt)
                cmpPkt = cmpPkt.encode('hex')
            for port in ports:
                rcvport = port + 1
                rcvpktnum = self.dataplane.pxr_getPortPktNum(rcvport)
                if rcvpktnum == 0:
                    continue
                for cmpSeq in range(rcvpktnum+1):
                    if cmpSeq == 0:
                        continue
                    srcPkt = self.dataplane.pxr_getPktData(rcvport, cmpSeq)
                
                    if len(srcPkt) == 0:
                        continue
                    else:
                        if use_pkt_match == 1:
                            srcPkt = srcPkt[0][0:-9]
                            srcPkt = srcPkt.decode('hex')
                            packetrcv = 0
                            if pkt.pkt_match(srcPkt):
                                match_index = port
                                packetrcv = 1
                                break
                            else:
                                continue
                        else:
                            srcPkt = srcPkt[0][0:-9]
                            srcPktlen = len(srcPkt)
                            cmpPktlen = len(cmpPkt)

                            if ( srcPktlen != cmpPktlen ):
                                continue

                            for i in range(cmpPktlen):
                                packetrcv = 1
                                if (ord(srcPkt[i]) != ord(cmpPkt[i])):
                                    packetrcv = 0
                                    break
                            if packetrcv == 1:
                                match_index = port
                                break
                            else:
                                continue
                totalrcv |= packetrcv
                if packetrcv == 0:
                    continue
                else:
                    break
        if totalrcv == 0:
            self.fail("Expected but no packets received on any port. \n" )
                
        return match_index
                    
                    

    def ctc_verify_no_packet_any(self, pkt, ports=[], device_number=0):
        print "verify no packet any port"
        #testutils.pxr_getPacketBuffer(self)
        for port in ports:
            rcvport = port + 1  
            #cmpPkt = pkt.encode('hex')
            srcPkt = self.dataplane.pxr_getPktData(rcvport, None)
            if len(srcPkt) == 0:
                continue
            else:
                self.fail("Expected no packets received on port %d. \n" %(port))
                
        return
        
    def ctc_verify_each_packet_on_each_port(self, pkts=[], ports=[], device_number=0):
        print "verify each packet each port"
        self.assertTrue(len(pkts) == len(ports),"packet list count does not match port list count")
        for port, pkt in zip(ports, pkts):
            list_pkt = [pkt]
            list_port = [port]
            self.ctc_verify_any_packet_any_port(list_pkt, list_port)
        
        return
            
    def ctc_verify_packets_any(self, pkt, ports=[], device_number=0):
        print "verify packet in any port"
        list_pkt = [pkt]
        self.ctc_verify_any_packet_any_port(list_pkt, ports)
        
        return
        
    def ctc_count_matched_packets(self, cmpPkt, port, device_number=0, timeout=None):
        print "count matched packets"
        total_rcv_pkt_cnt = 0
        rcvport = port + 1
        rcvpktnum = self.dataplane.pxr_getPortPktNum(rcvport)
        for cmpSeq in range(rcvpktnum+1):
            if cmpSeq == 0:
                continue
            srcPkt = self.dataplane.pxr_getPktData(rcvport, cmpSeq)
        
            if len(srcPkt) == 0:
                continue
            else:
                srcPkt = srcPkt[0][0:-9]
                srcPktlen = len(srcPkt)
                cmpPktlen = len(cmpPkt)

                if ( srcPktlen != cmpPktlen ):
                    continue

                for i in range(cmpPktlen):
                    packetrcv = 1
                    if (ord(srcPkt[i]) != ord(cmpPkt[i])):
                        packetrcv = 0
                        break
                if packetrcv == 1:
                    total_rcv_pkt_cnt += 1
                    
        return total_rcv_pkt_cnt
        
    def ctc_verify_packet_any_port(self, pkt, ports=[], device_number=0):
        print "verify packet in any port, return port index & rcv pkt"
        list_pkt = [pkt]
        portindex = self.ctc_verify_any_packet_any_port(list_pkt, ports)
        
        return (portindex, pkt)
            
    def ctc_show_packet(self, port_id, cmpSeq=None, compare_pkt=None, is_cpu_tx=None):
        time.sleep(5)
        testutils.pxr_getPacketBuffer(self)
        print "get packet on port %d " %(port_id)   
        port = port_id + 1
        srcPkt = self.dataplane.pxr_getPktData(port, cmpSeq)
        print "Origin Received Packet (Include CRC) : %s \n" %(srcPkt[-1])
        srcPkt = srcPkt[-1][0:-9]
        print "Process Received Packet (NO CRC) : %s \n" %(srcPkt)        
        if compare_pkt != None:
            compare_pkt = compare_pkt.encode('hex')
            print "Compare Packet (Include CRC) : %s \n" %(compare_pkt)

            if is_cpu_tx == None:
                compare_pkt = compare_pkt[0:-8]

            print "Compare Packet (NO CRC) : %s \n" %(compare_pkt)
            print "Compare the receive pkt!"
            result = compare_pkt == srcPkt
            print "Compare result is: " , result
            if result==False:
                self.fail("pkt is not same!\n")


    def ctc_show_packet_twamp(self, port_id, compare_pkt, mask_offset=None, mask_len=None):
    
        time.sleep(5)
        cmpSeq=None
        
        testutils.pxr_getPacketBuffer(self)
        
        print "get packet on port %d " %(port_id) 
        
        port = port_id + 1
        
        srcPkt = self.dataplane.pxr_getPktData(port, cmpSeq)
        
        print "Origin Received Packet (Include CRC) : %s \n" %(srcPkt[-1])
        
        srcPkt = srcPkt[-1][0:-9]
        
        print "Process Received Packet (NO CRC) : %s \n" %(srcPkt)  
        
        compare_pkt = compare_pkt.encode('hex')
        
        print "Compare Packet (NO CRC) : %s \n" %(compare_pkt)

        if mask_offset != None:
            srcPkt = srcPkt[0:(mask_offset*2)] + srcPkt[(mask_offset*2+mask_len*2):]        
            compare_pkt = compare_pkt[0:(mask_offset*2)] + compare_pkt[(mask_offset*2+mask_len*2):] 

        result = compare_pkt == srcPkt

        print "Compare Packet Result is: " , result

        if result==False:
            self.fail("pkt is not same!\n")        
        
        
                
