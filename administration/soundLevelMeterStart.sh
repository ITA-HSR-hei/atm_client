#!/bin/bash

START_LOG=/home/pi/soundLevelMeter/logs/startScript.log

echo ---------------Start soundLevelMeter--------------- >> $START_LOG
echo -n "Date: " >> $START_LOG
date >> $START_LOG
sudo python3.2 /home/pi/soundLevelMeter/soundLevelMeter.py >> $START_LOG 2>&1 &

sleep 5
echo --------------------------------------------------- >> $START_LOG