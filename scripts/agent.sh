#!/bin/bash

output=$(bash ./memory.sh)
echo "Output de la memory.sh: $output"
curl -X POST -H "Content-Type: application/json" -d "$output" http://192.168.153.128:8000/memory/
echo "rulat"
