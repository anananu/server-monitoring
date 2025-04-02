#!/bin/bash

sysinfo=$(bash /home/ana/Desktop/data_collection/scripts/sys.sh)
cpu=$(bash /home/ana/Desktop/data_collection/scripts/cpu.sh)
memory=$(bash /home/ana/Desktop/data_collection/scripts/memory.sh)
network=$(bash /home/ana/Desktop/data_collection/scripts/network.sh)
proc=$(bash /home/ana/Desktop/data_collection/scripts/proc.sh)
disk=$(bash /home/ana/Desktop/data_collection/scripts/disk.sh)

#echo "Output de la memory.sh: $output"
curl -X POST -H "Content-Type: application/json" -d "$sysinfo" http://192.168.153.128:8000/sysinfo/
curl -X POST -H "Content-Type: application/json" -d "$cpu" http://192.168.153.128:8000/cpu/
curl -X POST -H "Content-Type: application/json" -d "$memory" http://192.168.153.128:8000/memory/
curl -X POST -H "Content-Type: application/json" -d "$network" http://192.168.153.128:8000/network/
curl -X POST -H "Content-Type: application/json" -d "$proc" http://192.168.153.128:8000/proc/
curl -X POST -H "Content-Type: application/json" -d "$disk" http://192.168.153.128:8000/disk/
echo "rulat"



