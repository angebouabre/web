#!/bin/bash

source /home/pi/raspberry_env/bin/activate
python /home/pi/web/raspberry/manage.py loaddata /home/pi/fixture/*
