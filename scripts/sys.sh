#!/bin/bash

OUTPUT_FILE="sys_info.json"

UUID=$(cat /etc/machine-id)
HOSTNAME=$(hostname)
OS=$(cat /etc/os-release | grep "PRETTY_NAME" | awk -F '"' '{print $2}')
CPU=$(cat /proc/cpuinfo | grep "model name" | uniq | awk -F ': ' '{print $2}')

echo "{" > $OUTPUT_FILE
echo "  \"uuid\": \"$UUID\"," >> $OUTPUT_FILE
echo "  \"hostname\": \"$HOSTNAME\"," >> $OUTPUT_FILE
echo "  \"os\": \"$OS\"," >> $OUTPUT_FILE
echo "  \"cpu\": \"$CPU\"">> $OUTPUT_FILE
echo "}" >> $OUTPUT_FILE

cat $OUTPUT_FILE


