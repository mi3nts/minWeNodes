#!/bin/bash
#
sleep 5

kill $(pgrep -f 'ips7100ReaderV1.py')
sleep 5

kill $(pgrep -f 'ips7100ReaderV1Ser.py')
sleep 5

kill $(pgrep -f 'readI2c.py')
sleep 5

kill $(pgrep -f 'GPSReader.py')
sleep 5

kill $(pgrep -f 'batteryReader.py')