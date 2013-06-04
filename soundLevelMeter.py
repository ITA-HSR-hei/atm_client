#!/usr/bin/env python3
# read abelectronics ADC Pi V2 board inputs with repeating reading from each channel.
# uses quick2wire from http://quick2wire.com/ github: https://github.com/quick2wire/quick2wire-python-api
# Requries Python 3
# GPIO API depends on Quick2Wire GPIO Admin. To install Quick2Wire GPIO Admin, follow instructions at http://github.com/quick2wire/quick2wire-gpio-admin
# I2C API depends on I2C support in the kernel

# Version 2.0  - 18/11/2012
# Version History:
# 1.0 - Initial Release
# 2.0 - Change to code to 18 bit only mode with updates sequential reading
#
# Usage: changechannel(address, hexvalue) to change to new channel on adc chips
# Usage: getadcreading(address) to return value in volts from selected channel.
#
# address = adc_address1 or adc_address2 - Hex address of I2C chips as configured by board header pins.

import quick2wire.i2c as i2c
import requests
import json
import time
import logging
import logging.handlers
import sys
import datetime
import random

#Logfile
logger = logging.getLogger('soundLevelMeter')
LOG_FILENAME = '/home/pi/soundLevelMeter/logs/soundLevelMeter.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=200*1024*1024, backupCount=5 )
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


offsetTime=random.random()*1e6
stationId=''

#webpageGetId='http://152.96.193.217:8080/atm-webapp/public/0/getIdFromMac'
webpageGetId='http://atmng.cnlab.ch/atm/public/0/getIdFromMac'
#webpageReceiveData='http://152.96.193.217:8080/atm-webapp/public/0/receiveData'
webpageReceiveData='http://atmng.cnlab.ch/atm/public/0/receiveData'


#i2c Bus Config
adc_address1 = 0x68
adc_address2 = 0x69

varDivisior = 64 # from pdf sheet on adc addresses and config
varMultiplier = (2.4705882/varDivisior)/1000



with i2c.I2CMaster() as bus:
	def changechannel(address, adcConfig):
		bus.transaction(i2c.writing_bytes(address, adcConfig))
	def getadcreading(address):
		h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
		while (s & 128):
			h, m, l, s  = bus.transaction(i2c.reading(address,4))[0]
		# shift bits to product result
		t = ((h & 0b00000001) << 16) | (m << 8) | l
		# check if positive or negative number and invert if needed
		if (h > 128):
			t = ~(0x020000 - t)
		return t * varMultiplier



	def sleepUntilOffsetReached():

		now=datetime.datetime.now()

		sleepUntilStart=(1e6+offsetTime - now.microsecond)%1e6
		#logger.debug("Time until offset reached (sleep Time):" + str(sleepUntilStart/1e6) + " second")
		time.sleep(sleepUntilStart/1e6)
	
	time.sleep(5)
	print("***** Sound Level Meter started *****")
	logger.info("***** Sound Level Meter started *****")	
	changechannel(adc_address1, 0x9C)
	
	while True:
		try:
			macAddress = open('/sys/class/net/eth0/address').readline()
			macAddress = macAddress.rstrip('\n')
			payloadMacAddress={'macAddress': str(macAddress)}
			r = requests.get(webpageGetId, params=payloadMacAddress)
			
			if (r.status_code == 200):
				responseForId=json.loads(r.text)
				stationId=responseForId['id']
				logger.info("Received Id for this MeasureStation! MAC-Address is: " + str(macAddress)+" received id: "+str(stationId))
				break
			else:
				logger.error("Returned status code was: "+str(r.status_code))
				logger.error("Returned text message was: "+str(r.text))
				time.sleep(60)

		except Exception as e:
			logger.error(str(e))
			time.sleep(60)
	
	
	while True:
		try:
				
			
			measurements = []
			for i in range (1, 4):
				soundLevel = getadcreading(adc_address1)
				soundLevelInDbA=10*(((100*soundLevel)/2 )-25)
				measurements.append(soundLevelInDbA)
				if i <= 2:
					time.sleep(0.33)
		

			
			sleepUntilOffsetReached()
			average = sum(measurements) / len(measurements)
			timestamp=int(time.time()*1000)
			
			if (average < 0 or average > 2000):
				logger.error("Sound Level value is wrong! Microphone is probalby not pluged in!, SoundLevel was: "+str(average))
			
			payload = {"stationId": stationId, "timestamp": timestamp, "soundlevel": average}
			logger.debug("Send data: "+ str(payload))
			headers = { 'content-type': "application/json"}
			r= requests.post(webpageReceiveData, data=json.dumps(payload), headers=headers, timeout=5)

		except Exception as e:
			logger.error(str(e))
			time.sleep(10)

#               changechannel(adc_address1, 0xBC)
#               print ("Channel 2: %02f" % getadcreading(adc_address1))
#               changechannel(adc_address1, 0xDC)
#               print ("Channel 3 :%02f" % getadcreading(adc_address1))
#               changechannel(adc_address1, 0xFC)
#               print ("Channel 4: %02f" % getadcreading(adc_address1))
#               changechannel(adc_address2, 0x9C)
#               print ("Channel 5: %02f" % getadcreading(adc_address2))
#               changechannel(adc_address2, 0xBC)
#               print ("Channel 6: %02f" % getadcreading(adc_address2))
#               changechannel(adc_address2, 0xDC)
#               print ("Channel 7 :%02f" % getadcreading(adc_address2))
#               changechannel(adc_address2, 0xFC)
#               print ("Channel 8: %02f" % getadcreading(adc_address2))
