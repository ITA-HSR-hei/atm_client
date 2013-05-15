#! /bin/bash 
# Script Description
# 1. Adds crontab for which checks for script updates
# 2. Adds soundLevelMeter Script to startup


SOUND_LEVEL_HOME=/home/pi/soundLevelMeter
WHO_AM_I=$(whoami)

echo "INFO: Start install script"
sleep 1


if [[ "$WHO_AM_I" != "root" ]]; then
	echo "You must be root to run this script!!!"
	exit 1
fi

echo "INFO: Add cronjob which checks for updates"

CRON_ENTRY="0 1 * * * ${SOUND_LEVEL_HOME}/administration/checkForUpdates.sh >> ${SOUND_LEVEL_HOME}/logs/checkForUpdates.log 2>&1"
TEMP_FILE=/tmp/temp_crontab_entries.txt

crontab -l -u root | grep -v "checkForUpdates.sh" > $TEMP_FILE
echo "$CRON_ENTRY" >> $TEMP_FILE
crontab -u root $TEMP_FILE


echo "INFO: add soundLevelMeter script to startup routine"
cp "${SOUND_LEVEL_HOME}/administration/soundLevelMeterStart.sh" /etc/init.d

update-rc.d soundLevelMeterStart.sh defaults

echo -n "INFO: Finished install script"