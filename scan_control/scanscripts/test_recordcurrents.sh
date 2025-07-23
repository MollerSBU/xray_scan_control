#! /bin/bash

OUTPUT_FILE=${1:-currents.log}
echo "OUTPUT file: $OUTPUT_FILE"
touch "$OUTPUT_FILE"
total=12000
for ((i=1; i<=total; i++))
do
    echo currents | netcat -w 1 -t localhost 50001 >> ${OUTPUT_FILE}
    sleep 0.1

    progress=$((i*100/total))
    bar_width=50
    filled=$((progress * bar_width / 100))
    empty=$((bar_width - filled))
    bar=$(printf "%0.s#" $(seq 1 $filled))
    bar+=$(printf "%0.s-" $(seq 1 $empty))
    printf "\rProgress: [%s] %d%%" "$bar" "$progress"
done