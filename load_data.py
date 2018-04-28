import ConfigParser
import common
import datetime
import time
import pandas as pd

def generateJson(metricDef, values, startTime, endTime, frequencyMins, requestMetricCount):

	#  generate a date range to use for the time series generation

	dateRangeList = pd.date_range(start=startTime,
								  end=endTime, freq=str(
								   frequencyMins)+'min')
	
	valueIdx = 0
	idx = 0
	metricValues = []

	for tstamp in dateRangeList:
		if (valueIdx == len(values)):
			valueIdx = 0

		metricValues.append(
			common.prepareJSON(metricDef, int(time.mktime(tstamp.timetuple()))*1000, values[valueIdx])
		)		
		
		valueIdx += 1
		idx += 1

	chunkLength = requestMetricCount
	batchedMetrics = [
		metricValues[j:j + chunkLength] for j in xrange(
			0, len(metricValues), chunkLength)]

	return batchedMetrics
			
# main code

midConfig = ConfigParser.ConfigParser()
midConfig.read("config_mid.ini")

settings = common.getMidSettings(midConfig)

config = ConfigParser.ConfigParser()
config.read("config_metrics_weekly.ini")

pastDays = int(config.get("GLOBAL", "DAYS_OF_PAST_DATA"))
frequencyMins = int(config.get("GLOBAL", "FREQUENCY_MINUTES"))
requestMetricCount = int(config.get("GLOBAL", "NUMBER_OF_SAMPLES_PER_REQUEST"))
	
weeklyDefs = common.getMetricDefs(config)
startTime = datetime.datetime.now() - datetime.timedelta(days=pastDays)
endTime = datetime.datetime.now()

# push historical data based on the defs
print datetime.datetime.now()
print "Sending historical data for " + str(pastDays) + " days"
for metricDef in weeklyDefs:
	print("Sending data for " + metricDef.node + " " + metricDef.resource + " " + metricDef.type)
	values = common.readData(metricDef.fileName)
			
	batchedMetrics = generateJson(metricDef, values, startTime, endTime, frequencyMins, requestMetricCount)	
	for batch in batchedMetrics:
		common.sendMetrics(batch, settings)

print("Completed loading historical data for weekly seasonality")
print datetime.datetime.now()

config.read("config_metrics.ini")
defs = common.getMetricDefs(config)

pastDays = int(config.get("GLOBAL", "DAYS_OF_PAST_DATA"))
frequencyMins = int(config.get("GLOBAL", "FREQUENCY_MINUTES"))

startTime = datetime.datetime.now() - datetime.timedelta(days=pastDays)
endTime = datetime.datetime.now()

# load data only if the def is not in weekly
for metricDef in defs:
	if (metricDef not in weeklyDefs):
		print("Sending data for " + metricDef.node + " " + metricDef.resource + " " + metricDef.type)
		values = common.readData(metricDef.fileName)
			
		batchedMetrics = generateJson(metricDef, values, startTime, endTime, frequencyMins, requestMetricCount)	
		for batch in batchedMetrics:
			common.sendMetrics(batch, settings)

print("Completed loading historical data")


