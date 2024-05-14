#!/bin/sh

upower_output=$(upower -i $(upower -e | grep 'BAT'))

battery_state=$(echo "$upower_output" | grep 'state' | awk '{print $2}')

if [ "$battery_state" != "charging" ]
then
    energy_rate=$(echo "$upower_output" | grep 'energy-rate' | awk '{print $2" W"}')
    echo "$energy_rate"
else
    echo "⚡"
fi