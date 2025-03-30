#!/bin/bash

OUTPUT_FILE="proc_metrics.json"

UUID=$(cat /etc/machine-id)
HOSTNAME=$(hostname)
DATE=$(date +"%Y-%m-%d %H:%M:%S")

TOP_PROCESSES=$(ps aux --sort=-%cpu | head -n 6)

echo "{" > $OUTPUT_FILE
echo "  \"hostname\": \"$HOSTNAME\"," >> $OUTPUT_FILE
echo "  \"timestamp\": \"$DATE\"," >> $OUTPUT_FILE
echo "  \"top_processes\": [" >> $OUTPUT_FILE

FIRST_LINE=true
echo "$TOP_PROCESSES" | while read -r line; do
  if [[ "$line" == *"USER"* ]]; then
    continue
  fi

  USER=$(echo $line | awk '{print $1}')
  PID=$(echo $line | awk '{print $2}')
  CPU=$(echo $line | awk '{print $3}')
  MEM=$(echo $line | awk '{print $4}')
  STAT=$(echo $line | awk '{print $8}')
  START=$(echo $line | awk '{print $9}')
  TIME=$(echo $line | awk '{print $10}')
  COMMAND=$(echo $line | awk '{print $11}')

  if [ "$FIRST_LINE" = true ]; then
    FIRST_LINE=false
  else
    echo "    ," >> $OUTPUT_FILE
  fi
  
  echo "    {" >> $OUTPUT_FILE
  echo "      \"uuid\": \"$UUID\"," >> $OUTPUT_FILE
  echo "      \"timestamp\": \"$DATE\"," >> $OUTPUT_FILE
  echo "      \"hostname\": \"$HOSTNAME\"," >> $OUTPUT_FILE
  echo "      \"user\": \"$USER\"," >> $OUTPUT_FILE
  echo "      \"pid\": \"$PID\"," >> $OUTPUT_FILE
  echo "      \"cpu\": \"$CPU\"," >> $OUTPUT_FILE
  echo "      \"mem\": \"$MEM\"," >> $OUTPUT_FILE
  echo "      \"stat\": \"$STAT\"," >> $OUTPUT_FILE
  echo "      \"start\": \"$START\"," >> $OUTPUT_FILE
  echo "      \"time\": \"$TIME\"," >> $OUTPUT_FILE
  echo "      \"command\": \"$COMMAND\"" >> $OUTPUT_FILE
  echo "    }" >> $OUTPUT_FILE
done

echo "  ]" >> $OUTPUT_FILE
echo "}" >> $OUTPUT_FILE

cat $OUTPUT_FILE
