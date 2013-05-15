#!/bin/bash
# Add this script to the crontab as root user
# sudo crontab -e
# 0 1 * * */home/pi/soundLevelMeter/administration/checkForUpdates.sh >> /home/pi/soundLevelMeter/logs/checkForUpdates.log 2>&1

echo ""
echo ---------------Check For Updates---------------
cd /home/pi/soundLevelMeter

echo -n "Date: "
date

upToDate=$(sudo git remote show origin | grep "local out of date")

if [[ -z "$upToDate" ]]; then
        echo "INFO: No changes - SoundLevelMeter is up to date"
		echo -----------------------------------------------
else
        echo "INFO: Changes available - Fetsch new data and restart"
        sudo git fetch --all
        sudo git reset --hard origin/master
		
		
		echo "INFO: Restart in 10 seconds"
		echo -----------------------------------------------
		sleep 10
		sudo reboot -f
fi
