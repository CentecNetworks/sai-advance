#!/bin/bash

help() {
echo "Please run this script like:"
echo "./run.sh -c tm ctc      -------  regression centec sai cases"
echo "./run.sh --chip tm sai  -------  regression original sai cases"
echo "./run.sh ctc_sai_queue  -------  regression one module"
echo "./run.sh test_case.txt  -------  regression test case list, could be module list or case list"
echo "./run.sh -r/--restart restart saiserver when case fail or error"
echo "./run.sh -s/--spread spread all case in module"
echo "./run.sh -h"
echo "./run.sh --help"
echo "./run.sh"
echo "Default use tsingma"
exit
}

ARGS=`getopt -o c:hsr -l "chip:,help,spread,restart" -- "$@"`
if [ $? != 0 ]
then
    help
fi
eval set --"${ARGS}"
while true
do
    case "$1" in
        -c|--chip)
         if [ $2 == "goldengate" ] || [ $2 == "gg" ]
         then
             chipname="goldengate";
         elif [ $2 == "duet2" ] || [ $2 == "dt2" ] || [ $2 == "d2" ]
         then
             chipname="duet2";
         elif [ $2 == "tsingma" ] || [ $2 == "tm" ]
         then
             chipname="tsingma";
         else
             help
         fi
         shift 2
         ;;
        -h|--help)
         help;
         shift
         ;;
         -r|--restart)
         restartmode=1;
         shift
         ;;
         -s|--spread)
         spreadmode=1;
         shift
         ;;
         --)
         shift
         break
         ;;
    esac
done

if [ -z $chipname ]
then 
    chipname="tsingma"
fi

if [ -z $restartmode ]
then 
    restartmode=0
fi

if [ -z $spreadmode ]
then 
    spreadmode=0
fi

pid=""
run_one=0
testcase_exist=0
to_restart=0

cd testcase
grep_file="*.py"
if [ ! -z "$@" ]
then
	if [ "$@" = "ctc" ]
		then
		grep_file="ctc_*.py"
	elif [ "$@" = "sai" ]
	then
		grep_file="sai*.py"
    elif [ "$@" = test_case.txt ]
    then
        testcase_exist=1
	elif [[ "$@" ==  *.* ]]
		then
		run_one=1
	else 
		grep_file=$@"*.py"
	fi
fi

echo "*************************Now we run $chipname cases*************************"

#portmap_profile="port_map_file='default_interface_to_front_map.ini';chipname='$chipname'"
portmap_profile="chipname='$chipname'"
interface_list="--interface "'0@eth0'" --interface "'1@eth1'" --interface "'2@eth2'" --interface "'3@eth3'" --interface "'4@eth4'" --interface "'5@eth5'" --interface "'6@eth6'" --interface "'7@eth7'"  --interface "'8@eth8'" --interface "'9@eth9'" --interface "'10@eth10'" --interface "'11@eth11'" --interface "'12@eth12'" --interface "'13@eth13'" --interface "'14@eth14'" --interface "'15@eth15'" --interface "'16@eth16'""

start_dut_cmd=`ps -C saiserver -f -ww |grep $USER |awk -F "saiserver" '{print "./saiserver" $2}' `
#echo $start_dut_cmd

if [ $run_one = 1 ]
	then
    echo "/systest/systest_pub/wtf/Runtime/bin/python load.py $1 -t \"$portmap_profile\""
	eval "/systest/systest_pub/wtf/Runtime/bin/python load.py $1 -t \"$portmap_profile\""
else
    
    if [ $testcase_exist = 0 ]
    then
        ls $grep_file > test_case.txt 
        #sed -i 's/\.py//g' test_case.txt 
    fi
    
    if [ $spreadmode = 1 ]
    then
        if [ $testcase_exist = 0 ]
        then
            echo ""
        else
            grep_file=`cat test_case.txt`
        fi
        grep -E "^class" $grep_file | sed -n -e 's/tests\///' -e 's/\.py//' -e 's/class *//' -e 's/:/./' -e 's/(.*$//p' > test_case_list.txt 
    else
        cp test_case.txt test_case_list.txt
    fi
    
    sed -i 's/\.py//g' test_case_list.txt 
    #exit
    
	
	time=`date +"%Y-%m-%d-%H-%M-%S"`
    log_dir="./regression_log_${time}"
    if [ ! -d $log_dir ]
    then
        mkdir $log_dir
    fi
    echo "log dir" $log_dir    
	#log_path="./log_${time}.txt"
	nopass_log="./nopass_log_${time}.txt"
    report="./test_report_${time}.csv"
    #echo "case," >> $report
	echo "test begin>>>"
	for str in `cat test_case_list.txt`
		do
        log_module_dir="${log_dir}/${str}"
        log_path="./log_${time}_${str}.txt"
        echo "/systest/systest_pub/wtf/Runtime/bin/python load.py $str --log-dir \"$log_module_dir\" -t \"$portmap_profile\" > $log_path 2>&1"
		eval "/systest/systest_pub/wtf/Runtime/bin/python load.py $str --log-dir \"$log_module_dir\" -t \"$portmap_profile\" > $log_path 2>&1"
            
                #if [ $? == 0 ]
                #then 
                #      echo "$str,PASS" >> $report
                #      echo -e "$str                                                    \t\tPASS"
                #else
                #      echo "$str,FAIL">> $report
                #      echo -e "$str                                                     \t\t\033[40;31;1mFAIL \033[0m"
                #fi
		#pid=`pgrep saiserver -u shanz`
		#if [[ "$pid" == "" ]]
		#	then
		#	echo "SAI Server Break Interrupt! Please Restart Server!"
		#	break
		#fi
        
        grep "Result:" ${log_module_dir}/main.log | awk '{print $6}' > test_res.txt
        to_restart=0
    
        #get result
        for str in `cat test_res.txt`
            do
            grep "${str}.*Result.*PASS" ${log_module_dir}/main.log
            if [ $? == 0 ]
            then
                echo "$str,PASS" >> $report
                echo -e "$str"
            fi
            
            grep "${str}.*Result.*FAILED" ${log_module_dir}/main.log
            if [ $? == 0 ]
            then
                echo "$str,FAILED" >> $report
                echo -e "$str"
                
                if [ $restartmode == 1 ]
                then
                    echo "fail and restart "
                    to_restart=1
                fi
            fi
            
            grep "${str}.*Result.*ERROR" ${log_module_dir}/main.log
            if [ $? == 0 ]
            then
                echo "$str,ERROR" >> $report
                echo -e "$str"
                
                if [ $restartmode == 1 ]
                then
                    echo "error and restart "
                    to_restart=1
                fi
            fi
            
            done
        
            
            if [ $to_restart == 1 ]
            then
                echo "kill saiserver for error occour!"
                killall -9 saiserver
                killall -9 pswitchd
                
                echo "Wait 20 sec for saiserver restart !"
                cd ..
                xterm -e './pswitchd -p a -t topo-1dut.txt' &
                xterm -e $start_dut_cmd &
                dut_pid=$!
                sleep 10
                
                echo "The test setup finish! saiserver=$dut_pid!!"
                
                
                cd testcase
            fi
        
		done
        
        
    
    
    
        
	#grep -E "^ERROR:" $log_path | sed -n  -e 's/ERROR: *//p' >> $nopass_log
	#grep -E "^FAIL:" $log_path | sed -n  -e 's/FAIL: *//p' >> $nopass_log
    
    for str in `cat test_case_list.txt`
        do
        log_path="./log_${time}_${str}.txt"
        mv $log_path $log_dir
        done
    mv $report $log_dir
	
	echo "<<<test end"
	echo "log path:"$log_dir
	#echo "nopass log path:"$nopass_log
fi
cd ..
