import pkg_resources as myload
import pprint
pp = pprint.PrettyPrinter(indent=3)
pp.pprint(myload.__file__)
import sys
import os
import subprocess
import time
#setup 
current_path = os.getcwd()
thirft_lib = os.path.join(os.path.dirname(current_path), "gen-py")
sys.path.append(thirft_lib)

 
cmd="ps -C saiserver -f -ww | grep " + os.environ['USER']
pinfo=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
result=pinfo.communicate()
strlist=result[0].split()
if strlist.count("-t") == 1 and strlist.count("-h") == 1 and ( sys.argv.count("--pypxr-sockfile") == 0 or sys.argv.count("--thirft-port") == 0 ) :
    index = strlist.index("-h")
    sys.argv.append("--pypxr-sockfile")
    sys.argv.append(strlist[index+1])
    index = strlist.index("-t")
    sys.argv.append("--thirft-port")
    sys.argv.append(strlist[index+1])
else :
    print("!!! Two saiserver or No saiserver started , can't use auto select mode!")
    print(cmd+result[0])
    exit()

starttime=str(time.ctime()).replace(' ','_')
starttime=starttime.replace(':','-')

logdir = "log_"+starttime   

if ( sys.argv.count("--log-dir") == 0  ):
    sys.argv.append("--log-dir")
    sys.argv.append(os.path.join(current_path,logdir))

if ( sys.argv.count("--test-dir") == 0  ):
    sys.argv.append("--test-dir")
    sys.argv.append(current_path)    


#xmldir = "xml_" + starttime    
#if ( sys.argv.count("--xunit") == 0  ):
#    sys.argv.append("--xunit")        
#   
#if ( sys.argv.count("--xunit-dir") == 0  ):
#    sys.argv.append("--xunit-dir")            
#    sys.argv.append(xmldir)    
    
#usage: load.py [-h] [-v] [--list] [--list-test-names] [--allow-user]
#               [--pypath PYPATH] [-f TEST_FILE] --test-dir TEST_DIR
#               [--test-order {default,lexico,rand}]
#               [--test-order-seed TEST_ORDER_SEED] [-P PLATFORM]
#               [-a PLATFORM_ARGS] [--platform-dir PLATFORM_DIR]
#               [--interface INTERFACE] [--device-socket DEVICE-SOCKET]
#               [--log-file LOG_FILE] [--log-dir LOG_DIR]
#               [--debug {verbose,debug,info,warn,warning,error,critical}]
#               [--verbose] [-q] [--profile] [--profile-file PROFILE_FILE]
#               [--xunit] [--xunit-dir XUNIT_DIR] [--relax] [--failfast]
#               [-t TEST_PARAMS] [--fail-skipped]
#               [--default-timeout DEFAULT_TIMEOUT]
#               [--default-negative-timeout DEFAULT_NEGATIVE_TIMEOUT]
#               [--minsize MINSIZE] [--random-seed RANDOM_SEED]
#               [--disable-ipv6] [--qlen QLEN]
#               [--test-case-timeout TEST_CASE_TIMEOUT] [--disable-vxlan]
#               [--disable-geneve] [--disable-erspan] [--disable-mpls]
#               [--disable-nvgre] [--socket-recv-size SOCKET_RECV_SIZE]
#               [test_specs [test_specs ...]]

myload.run_script('ptf==0.9.1', 'ptf')

