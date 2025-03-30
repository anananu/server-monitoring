#!/bin/bash

OUTPUT_FILE="network_metrics.json"

UUID=$(cat /etc/machine-id)
HOSTNAME=$(hostname)
DATE=$(date +"%Y-%m-%d %H:%M:%S")

echo "{" > $OUTPUT_FILE
echo "  \"uuid\": \"$UUID\"," >> $OUTPUT_FILE
echo "  \"hostname\": \"$HOSTNAME\"," >> $OUTPUT_FILE
echo "  \"timestamp\": \"$DATE\"," >> $OUTPUT_FILE
echo "  \"interfaces\": [" >> $OUTPUT_FILE

for INTERFACE in $(ls /sys/class/net/ | grep -v "lo"); do
    route_count=$(grep -c "^[^ ]" /proc/net/route)

    ipv4_address=$(ip -4 addr show $INTERFACE | grep -oP 'inet \K[\d.]+')

    ipv6_address=$(ip -6 addr show $INTERFACE | grep -oP 'inet6 \K[\da-f:]+')


    if [[ $route_count -gt 0 ]]; then
        connectivity="Connected"
    else
        connectivity="Not Connected"
    fi

    interface_status=$(cat /sys/class/net/$INTERFACE/operstate)
    if [[ $interface_status == "up" ]]; then
        availability="Available"
    else
        availability="Not Available"
    fi

    rx_bytes_1=$(cat /sys/class/net/$INTERFACE/statistics/rx_bytes)
    tx_bytes_1=$(cat /sys/class/net/$INTERFACE/statistics/tx_bytes)

    sleep 1 

    rx_bytes_2=$(cat /sys/class/net/$INTERFACE/statistics/rx_bytes)
    tx_bytes_2=$(cat /sys/class/net/$INTERFACE/statistics/tx_bytes)

    rx_rate=$((rx_bytes_2 - rx_bytes_1))
    tx_rate=$((tx_bytes_2 - tx_bytes_1))

    rx_rate_human=$(echo "scale=2; $rx_rate / 1024" | bc)
    tx_rate_human=$(echo "scale=2; $tx_rate / 1024" | bc)

    echo "    {" >> $OUTPUT_FILE
    echo "      \"interface\": \"$INTERFACE\"," >> $OUTPUT_FILE
    echo "      \"connectivity\": \"$connectivity\"," >> $OUTPUT_FILE
    echo "      \"availability\": \"$availability\"," >> $OUTPUT_FILE

    if [[ -n "$ipv4_address" ]]; then
        echo "      \"ipv4_address\": \"$ipv4_address\"," >> $OUTPUT_FILE
    else
        echo "      \"ipv4_address\": \"Not Available\"," >> $OUTPUT_FILE
    fi

    if [[ -n "$ipv6_address" ]]; then
        echo "      \"ipv6_address\": \"$ipv6_address\"," >> $OUTPUT_FILE
    else
        echo "      \"ipv6_address\": \"Not Available\"," >> $OUTPUT_FILE
    fi

    echo "      \"throughput_rx\": \"$rx_rate_human KB/s\"," >> $OUTPUT_FILE
    echo "      \"throughput_tx\": \"$tx_rate_human KB/s\"" >> $OUTPUT_FILE

    if [[ $(ls /sys/class/net/ | grep -v "lo" | wc -l) -gt 1 ]]; then
        echo "    }," >> $OUTPUT_FILE
    else
        echo "    }" >> $OUTPUT_FILE
    fi
done

echo "  ]" >> $OUTPUT_FILE
echo "}" >> $OUTPUT_FILE

cat $OUTPUT_FILE
