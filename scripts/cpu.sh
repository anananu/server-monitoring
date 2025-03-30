#!/bin/bash

OUTPUT_FILE="cpu_metrics.json"

UUID=$(cat /etc/machine-id)
HOSTNAME=$(hostname)
DATE=$(date +"%Y-%m-%d %H:%M:%S")
LOAD_AVG1=$(cat /proc/loadavg | awk '{print $1}')
LOAD_AVG2=$(cat /proc/loadavg | awk '{print $2}')
LOAD_AVG3=$(cat /proc/loadavg | awk '{print $3}')
#TOP_PROCESSES=$(ps -eo pid,ppid,cmd,%cpu --sort=-%cpu | tail -n +2 | head -n 6 | awk '{print "{\"pid\": "$1", \"ppid\": "$2", \"cmd\": \""substr($0, index($0,$3))"\", \"cpu\": "$4"},"}')
CPU_FREQ=$(grep "cpu MHz" /proc/cpuinfo | awk -F ': ' '{print $2}' | awk '{print "\"core" NR "\": " $1 ","}')
MODEL_NAME=$(cat /proc/cpuinfo | grep "model name" | uniq | awk -F ': ' '{print $2}')

echo "{" > $OUTPUT_FILE
echo "  \"uuid\": \"$UUID\"," >> $OUTPUT_FILE
echo "  \"hostname\": \"$HOSTNAME\"," >> $OUTPUT_FILE
echo "  \"timestamp\": \"$DATE\"," >> $OUTPUT_FILE
echo "  \"model_name\": \"$MODEL_NAME\",">> $OUTPUT_FILE
echo "  \"load_avg1\": \"$LOAD_AVG1\"," >> $OUTPUT_FILE
echo "  \"load_avg2\": \"$LOAD_AVG2\"," >> $OUTPUT_FILE
echo "  \"load_avg3\": \"$LOAD_AVG3\"," >> $OUTPUT_FILE
echo "  \"cpu_frequency\": {" >> $OUTPUT_FILE
echo "$CPU_FREQ" | sed '$ s/,$//' >> $OUTPUT_FILE
echo "  } " >> $OUTPUT_FILE
#echo "  \"top_processes\": [" >> $OUTPUT_FILE
#echo "$TOP_PROCESSES" | sed '$ s/,$//' >> $OUTPUT_FILE
#echo "  ]" >> $OUTPUT_FILE
echo "}" >> $OUTPUT_FILE

cat $OUTPUT_FILE
