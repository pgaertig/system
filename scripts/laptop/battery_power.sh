#!/bin/sh

upower_output=$(upower -i $(upower -e | grep 'BAT'))

battery_state=$(echo "$upower_output" | grep 'state' | awk '{print $2}')

if [ "$battery_state" = "charging" ]
then
    echo -n "B⚡ "
fi

energy_rate=$(echo "$upower_output" | grep 'energy-rate' | awk '{print $2" W"}')
if [ "$energy_rate" = "0 W" ]
then
    echo "Full"
else
    echo "$energy_rate"
fi

LAST_ENERGY_FILE="/tmp/last_energy_uj"
if [ ! -f $LAST_ENERGY_FILE ] || [ ! -s $LAST_ENERGY_FILE ]; then
    echo $(cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj) > $LAST_ENERGY_FILE
fi
LAST_MJ=$(cat $LAST_ENERGY_FILE)
MJ=$(cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj)
VAL=$(echo "scale=2; ($MJ - $LAST_MJ) / 1000000" | bc)
echo "CPU $VAL W"
echo $MJ > $LAST_ENERGY_FILE
