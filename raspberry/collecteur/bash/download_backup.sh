#!/bin/bash

date_time=`date +\%d_\%m_\%Y_\%H_\%M_\%S`
scp pi@192.168.1.21:/home/pi/data/* /home/pi/data/
sleep 5

echo "temperature du ${date_time} sauvegardée.\n" >> /home/pi/log/temperature.log

