#!/bin/bash

date_time=`date +\%d_\%m_\%Y_\%H_\%M`
scp pi@192.168.1.21:/sys/bus/w1/devices/28-000002ad9190/w1_slave /home/pi/data/data_of_${date_time}.txt
echo "temperature du ${date_time} sauvegardée.\n" >> /home/pi/log/temperature.log

