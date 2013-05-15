#!/bin/bash

SOUND_LEVEL_HOME=/home/pi/soundLevelMeter

echo ""
echo ---------------Check For Updates---------------
cd $SOUND_LEVEL_HOME

echo -n "Date: "
date

upToDate=$(sudo git remote show origin | grep "local out of date")

if [[ -z "$upToDate" ]]; then
        echo "INFO: No changes - SoundLevelMeter is up to date"
		echo -----------------------------------------------
else
        echo "INFO: Changes available - Fetch new data and restart"
        sudo git fetch --all
        sudo git reset --hard origin/master
		
		cp $SOUND_LEVEL_HOME/administration/soundLevelMeterStart.sh /etc/init.d
				
		echo "INFO: Restart in 10 seconds"
		echo -----------------------------------------------
		sleep 10
		sudo reboot -f
fi
