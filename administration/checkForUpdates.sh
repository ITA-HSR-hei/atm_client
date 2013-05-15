#!/bin/bash

SOUND_LEVEL_HOME=/home/pi/soundLevelMeter
WHO_AM_I=$(whoami)

echo ""
echo ---------------Check For Updates---------------
cd $SOUND_LEVEL_HOME

echo -n "Date: "
date

if [[ "$WHO_AM_I" != "root" ]]; then
	echo "You must be root to run this script!!!"
	exit 1
fi

upToDate=$(git remote show origin | grep "local out of date")

if [[ -z "$upToDate" ]]; then
        echo "INFO: No changes - SoundLevelMeter is up to date"
		echo -----------------------------------------------
else
        echo "INFO: Changes available - Fetch new data and restart"
        git fetch --all
        git reset --hard origin/master
		
		cp $SOUND_LEVEL_HOME/administration/soundLevelMeterStart.sh /etc/init.d
		
		echo "INFO: Restart in 10 seconds"
		echo -----------------------------------------------
		sleep 10
		sudo reboot -f
fi
