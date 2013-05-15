#!/bin/bash
# Add this script to the crontab as root user
# sudo crontab -e
# 0 * * * * /home/pi/soundLevelMeterAdministration/checkForUpdates.sh &> /home/pi/soundLevelMeter/logs



cd /home/pi/soundLevelMeter
upToDate=$(sudo git remote show origin | grep "local out of date")

if [[ -z "$upToDate" ]]; then
        echo "No changes - SoundLevelMeter is up to date"
        exit 0
else
        echo "Changes available - Fetsch new data and restart"
        sudo git fetch --all
        sudo git reset --hard origin/master
        sudo reboot -f
fi
