import ConfigParser
import common
import datetime
import time
import pandas as pd
import requests
import json


# main code

midConfig = ConfigParser.ConfigParser()
midConfig.read("config_mid.ini")

settings = common.getMidSettings(midConfig)

anomalyConfig = ConfigParser.ConfigParser()
anomalyConfig.read("config_change.ini")

frequencyMins = int(anomalyConfig.get("GLOBAL", "FREQUENCY_MINUTES"))

#send change data real time
defs = common.getMetricDefs(anomalyConfig)

#send real time data

curtime = datetime.datetime.now() 
tsPoints = 0
while(True):
	print "Sending data for " + str(curtime)

	metricList = []

	for metricDef in defs:
		values = common.readData(metricDef.fileName)
		index = tsPoints % len(values)
			
		metricList.append(
			common.prepareJSON(metricDef, int(time.mktime(curtime.timetuple()))*1000, values[index])
		)	
	
	common.sendMetrics(metricList, settings)

	time.sleep(frequencyMins * 60)
	curtime = curtime + datetime.timedelta(seconds = frequencyMins * 60)
	tsPoints += 1
