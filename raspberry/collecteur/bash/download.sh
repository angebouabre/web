#!/bin/bash

date_time=`date +\%d_\%m_\%Y_\%H_\%M_\%S`
scp pi@192.168.1.21:/sys/bus/w1/devices/28-000002ad9190/w1_slave /home/pi/data/data_of_28-000002ad9190_`date +\%d_\%m_\%Y_\%H_\%M_\%S`.txt
sleep 2
scp pi@192.168.1.21:/sys/bus/w1/devices/28-000005d305e4/w1_slave /home/pi/data/data_of_28-000005d305e4_`date +\%d_\%m_\%Y_\%H_\%M_\%S`.txt
sleep 2
scp pi@192.168.1.21:/sys/bus/w1/devices/28-000005d31e24/w1_slave /home/pi/data/data_of_28-000005d31e24_`date +\%d_\%m_\%Y_\%H_\%M_\%S`.txt
sleep 2
ssh pi@192.168.1.21 < /home/bouable/esigetel/web/raspberry/collecteur/bash/hygro.sh 
sleep 2
scp pi@192.168.1.21:/home/pi/data/hygro.txt /home/pi/data/data_hygrometrie_`date +\%d_\%m_\%Y_\%H_\%M_\%S`.txt

echo "temperature du ${date_time} sauvegardée.\n" >> /home/pi/log/temperature.log

