#! /bin/bash 
# Script Description
# 1. Adds crontab for which checks for script updates
# 2. Adds soundLevelMeter Script to startup


installSoundLevelMeter
WHO_AM_I=$(whoami)
if [[ "$WHO_AM_I" != "root"]]; then
	echo "You must be root to install soundLevelMeter"
	exit 1
fi

# Remove and add crontab
CRON_ENTRY="* * * * * /home/pi/soundLevelMeter/administration/checkForUpdates.sh >> /home/pi/soundLevelMeter/logs/checkForUpdates.log 2>&1"
TEMP_FILE=/tmp/temp_crontab_entries.txt

crontab -l -u root | grep -v "checkForUpdates.sh" > $TEMP_FILE
echo $CRON_ENTRY >> $TEMP_FILE
crontab -u root $TEMP_FILE


