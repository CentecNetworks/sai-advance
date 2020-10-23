# Overview
   The Switch Abstraction Interface(SAI) defines the API to provide a vendor-independent way of controlling forwarding elements, such as a switching ASIC, an NPU or a software switch in a uniform manner.

   This repository contains SAI implementation for Centec switching ASICs. Customers can configure Centec switching ASICs by SAI APIs in SONiC or other networking OS. This software release is Centec's contribution to the open community of its implementation of the SAI 1.5.1 as specified on the SAI Github at https://github.com/opencomputeproject/SAI, and the SAI release supports the Centec CTC7132.
   
   This software release also support some private features by Centec, not defined in SAI. See below tables.

# Public Features
| SAI Module     | Supported   |
|----------------|-------------|
| ACL            |     Y       |
| BFD            |     Y       |
| Bridge         |     Y       |
| Buffer         |     Y       |
| Counter        |     Y       |
| DebugCounter   |     Y       |
| Fdb            |     Y       |
| Hash           |     Y       |
| HostIntf       |     Y       |
| IsolationGroup |     Y       |
| Lag            |     Y       |
| Mirror         |     Y       |
| Multicast      |     Y       |
| Mpls           |     Y       |
| NAT            |     Y       |
| Neighbor       |     Y       |
| Nexthop        |     Y       |
| Nexthopgroup   |     Y       |
| Policer        |     Y       |
| Port           |     Y       |
| QoSmaps        |     Y       |
| Queue          |     Y       |
| Route          |     Y       |
| Router         |     Y       |
| RouterIntf     |     Y       |
| Samplepacket   |     Y       |
| Scheduler      |     Y       | 
| Schedulergroup |     Y       |
| STP            |     Y       |
| Switch         |     Y       |
| Tunnel         |     Y       |
| UDF            |     Y       |
| VirtualRouter  |     Y       |
| Vlan           |     Y       |
| WRED           |     Y       |
| Ipmc           |     Y       |
| Ipmcgroup      |     Y       |
| L2mc           |     Y       |
| L2mcgroup      |     Y       |
| Mcastfdb       |     Y       |
| Rpfgroup       |     Y       |
| Warmboot       |     Y       |
| TAM            |     Planed  |
| Dtel           |     Planed  |


# Private Features
| SAI Module     | Supported   |
|----------------|-------------|
| MPLS VPN       |     Y       |
| BFD for VPN&TP |     Y       |
| ES             |     Y       |
| PTP            |     Y       |
| SYNCE          |     Y       |
| TWAMP          |     Y       |
| Y1731          |     Y       |
| APS for VPN    |     Y       |
| NetFlow        |     Planed  |
| Buffer Monitor |     Y       |
| Latency Monitor|     Y       |
| Service QoS    |     Y       |
| NPM            |     Y       |
| SD Detect      |     Y       |

# Testing
The Centec SAI use PTF framework to do testing. Centec add more than cases. More detail information refer to [PTF Tests](https://github.com/CentecNetworks/sai-advance/wiki/PTF-Tests)

# Contact us

Website: [http://www.centecnetworks.com]<BR>
Issue tracker: [https://github.com/CentecNetworks/sai-advance/issues]<BR>
Support email: support@centecnetworks.com<BR>
Sales email: sales@centecnetworks.com<BR>

# Release Log
## 2020-05-29
  Initial release.<BR>
  tag：CTC-v1.0.0-SAI-1.5.0
### Feature Added:
    Support CTC7132
    Support SAI 1.5
    Support above feature list
### Dependencies
 This pakage depends on Centec SDK V5.5.6RC

## 2020-07-31
  Second release.<BR>
  tag：CTC-v1.1.0-SAI-1.5.0
### Feature Added:
    Support CTC7132
    Support SAI 1.5
    Support new feature list: 
        APS for VPN, Buffer/Latency Monitor, 
        Service QoS, NPM for 1564,2544
        Signal Degrade Detect
### Dependencies
 This pakage depends on Centec SDK V5.6.0.21

## 2020-10-23
  3rd release.<BR>
  tag：CTC-v1.1.1-SAI-1.5.0
### Feature Added:
    Support CTC7132
    Support SAI 1.5
    Support new feature list: 
         More support for L2/L3 VPN
### Dependencies
 This pakage depends on Centec SDK V5.6.1
 
# How to compile

## 1. Preparation
- This SAI plugin requires Centec SDK support, so first step, you need to get Centec SDK for your switch chip, and copy them to $SAI\_SOURCE\_DIR/sdk
- To get SDK, please contact Centec.
- Prepare nessary directories: $SAI\_SOURCE\_DIR/lib/$chipname, and copy compiled libctcsdk.so to the directories.

$SAI\_SOURCE\_DIR/ctcsdk like this:

    [centec@sw1 ctcsdk]$ ls
    app  core         ctc_shell          dkits  driver     Makefile         Makefile.one_lib  sal        torvars.bat
    cfg  compile.bat  ctccli  dal        docs   libctccli  Makefile.kernel  Makefile.user     mk         script

## 2. Edit CMakeLists.txt and make
You can modify the CMakeLists.txt following here:
First we need to edit $SAI\_SOURCE\_DIR/**CMakeLists.txt**, which located in this folder. With this file, cmake can generate Makefile automatically. Here we give an example, which provides a switch box with x86 CPU and Centec CTC7132(TsingMa) switch chip:

    SET(ARCH "board")
    SET(CHIPNAME "tsingma")
    SET(SDKHOME "../sdk/")

If you want to enable warmboot feature, you will be need redis support,and set below flag, and set the correct REDIS_INCLUDE_DIR

    SET(CONFIG_DBCLIENT 1)

After this, let us enter folder ***build/***, and run these command:

    [centec@sw0 build]$ rm -rf *
    [centec@sw0 build]$ cmake ../

Then you can see we have ***Makefile*** now, and let us make it:

    [centec@sw0 build]$ ls
    app  centec  CMakeCache.txt  CMakeFiles  cmake_install.cmake  db  Makefile
    [centec@sw0 build]$ make   

## 3. Get your sai-advance
Enter into lib/chipname/ folder, you can see these files here:

    [centec@sw0 tsingma]$ ls 
    libctcsdk.so libdb.so.1 libsai.so.1 libsai.so.1.5
  