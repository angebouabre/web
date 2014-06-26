#!/bin/bash

count=0

source /home/bouable/esigetel/raspberry_env/bin/activate

for file in $( ls -1p /home/pi/fixture/)
do 
    python /home/bouable/esigetel/web/raspberry/manage.py loaddata /home/pi/fixture/${file}
    count=$((count + 1))
done

printf '... %d\n' ${count}
