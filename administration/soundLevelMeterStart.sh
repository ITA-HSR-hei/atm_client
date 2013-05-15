#!/bin/bash

SOUND_LEVEL_HOME=/home/pi/soundLevelMeter
START_LOG=/home/pi/soundLevelMeter/logs/startScript.log


echo ---------------Start soundLevelMeter--------------- >> $START_LOG
echo -n "Date: " >> $START_LOG


#Check if 
diff -q $SOUND_LEVEL_HOME/administration/checkForUpdates.sh $SOUND_LEVEL_HOME/administration/local_checkForUpdates.sh >> $START_LOG 2>&1
if [[ $? -ne 0 ]]; then
	echo "INFO: There was an update in checkForUpdates.sh replace local copy" >> $START_LOG
	cp $SOUND_LEVEL_HOME/administration/checkForUpdates.sh $SOUND_LEVEL_HOME/administration/local_checkForUpdates.sh >> $START_LOG 2>&1
fi



date >> $START_LOG
sudo python3.2 /home/pi/soundLevelMeter/soundLevelMeter.py >> $START_LOG 2>&1 &

sleep 5
echo --------------------------------------------------- >> $START_LOG