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

logger = logging.getLogger('soundLevelMeter')
LOG_FILENAME = 'home/pi/soundLevelMeter/logs/soundLevelMeter.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=200*1024*1024, backupCount=5 )
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

offsetTime=random.random()*1e6


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
		logger.debug("Time until offset reached (sleep Time):" + str(sleepUntilStart/1e6) + " second")
		time.sleep(sleepUntilStart/1e6)
	
	time.sleep(5)
	print("***** Sound Level Meter started *****")
	logger.info("***** Sound Level Meter started *****")	
	changechannel(adc_address1, 0x9C)

	while True:
		try:
				
			
			measurements = []
			for i in range (1, 4):
				soundLevel = getadcreading(adc_address1)
				soundLevelInDbA=10*(((100*soundLevel)/2 )-25)
				measurements.append(soundLevelInDbA)
				if i <= 2:
					time.sleep(0.33)
		

			
			#print("now: "+ str(time.time()))
			#print("")
			sleepUntilOffsetReached()
			average = sum(measurements) / len(measurements)
			timestamp=int(time.time()*1000)
			stationId = 2
			
			if (average < 0 or average > 2000):
				soundLevelInDb=-1
			
			payload = {"stationId": stationId, "timestamp": timestamp, "soundlevel": average}
			logger.debug("Send data: "+ str(payload))
			headers = { 'content-type': "application/json"}
			r= requests.post("http://atmng.cnlab.ch:8080/atm/public/0/receiveData", data=json.dumps(payload), headers=headers, timeout=2)

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

