#!/bin/sh

# in milli-watt (1000 = 1W) because shell arithmetic doesn't do floating point
while true; do
    LAST_MJ=$MJ
    MJ=$(cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj)
    echo $(((MJ - LAST_MJ) / 1000))
    sleep 1
done

# energy_uj shows usage in joules, so we convert it to watt-hours by dividing by 3.6 million
