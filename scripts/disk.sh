#!/bin/bash

OUTPUT_FILE="disk_metrics.json"

UUID=$(cat /etc/machine-id)
HOSTNAME=$(hostname)
DATE=$(date +"%Y-%m-%d %H:%M:%S")


disk_total_GB=$(df -h / | awk 'NR==2 {print $2}' | sed 's/[A-Za-z]$//')
disk_free_GB=$(df -h / | awk 'NR==2 {print $4}' | sed 's/[A-Za-z]$//')
disk_usage_GB=$(df -h / | awk 'NR==2 {print $3}' | sed 's/[A-Za-z]$//')


disk_reads_sectors=$(awk '{s+=$4} END {print s}' /proc/diskstats)
disk_writes_sectors=$(awk '{s+=$8} END {print s}' /proc/diskstats)

disk_queue_length=$(awk '{s+=$9} END {print s}' /proc/diskstats)

disk_partitions=$(ls /sys/block/sda | grep -E "sda[0-9]+" | wc -l)

echo "{" > $OUTPUT_FILE
echo "  \"uuid\": \"$UUID\"," >> $OUTPUT_FILE
echo "  \"hostname\": \"$HOSTNAME\"," >> $OUTPUT_FILE
echo "  \"timestamp\": \"$DATE\"," >> $OUTPUT_FILE
echo "  \"disk_total_GB\": \"$disk_total_GB\"," >> $OUTPUT_FILE
echo "  \"disk_usage_GB\": \"$disk_usage_GB\"," >> $OUTPUT_FILE
echo "  \"disk_free_GB\": \"$disk_free_GB\"," >> $OUTPUT_FILE
echo "  \"disk_reads_sectors\": \"$disk_reads_sectors\"," >> $OUTPUT_FILE
echo "  \"disk_writes_sectors\": \"$disk_writes_sectors\"," >> $OUTPUT_FILE
echo "  \"disk_queue_length\": \"$disk_queue_length\"," >> $OUTPUT_FILE
echo "  \"nr_disk_partitions\": \"$disk_partitions\"" >> $OUTPUT_FILE
echo "}" >> $OUTPUT_FILE

cat $OUTPUT_FILE
