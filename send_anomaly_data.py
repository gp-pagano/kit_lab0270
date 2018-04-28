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
anomalyConfig.read("config_anomaly.ini")

defs = common.getMetricDefs(anomalyConfig)

#send anomaly data

metricList = []
# stagger the anomaly events being generated
metricTime = datetime.datetime.now() - datetime.timedelta(seconds = len(defs) * 60)
print(metricTime)
for metricDef in defs:			
	metricTime = metricTime + datetime.timedelta(seconds = 60)
	
	print "Sending data for " + str(metricTime)

	metricList.append(
		common.prepareJSON(metricDef, int(time.mktime(metricTime.timetuple()))*1000, metricDef.value)
	)	
	
common.sendMetrics(metricList, settings)
