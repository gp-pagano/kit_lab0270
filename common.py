import datetime
import time
import requests
import json

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

def requestHeaders():
    """
    Document function here.

    This is required for Secure connections
    to the Mid Server Web extension.

    """
    auth = ''
    auth += 'POST\n'
    auth += 'application/json\n'
    auth += datetime.datetime.utcnow().strftime(DATE_FORMAT)[:-3] + 'Z\n'
    auth += '/api/mid/sa/metrics'

    return {
        'Date': datetime.datetime.utcnow().strftime(DATE_FORMAT)[:-3] + 'Z',
        'Content-Type': 'application/json'
    }


def readData(fileName):
	values = []
	with open(fileName) as f:
		for line in f:
			values.append(float(line))
	
	return values;
	


def getMidURL(settings):
    url = 'http://' + settings.midServer + ':' + settings.portNum + \
        '/api/mid/sa/metrics'

    return url


class MetricDef(object):
	type = ""
	node = ""
	resource = ""
	fileName = ""
	source = ""
	value = -1

	# The class "constructor" - It's actually an initializer 
	def __init__(self, type, node, resource, fileName, source, value):
		self.type = type
		self.node = node
		self.resource = resource
		self.fileName = fileName
		self.source = source
		self.value = value

class Settings(object):
	midServer = "localhost"
	portNum = 8097
	userName = ""
	password = ""
	
	# The class "constructor" - It's actually an initializer 
	def __init__(self, midServer, portNum, userName, password):
		self.midServer = midServer
		self.portNum = portNum
		self.userName = userName
		self.password = password

def getMidSettings(config):
	return Settings(config.get("MID_SERVER", "MID_HOSTNAME"), config.get("MID_SERVER", "MID_PORT"), 
					config.get("MID_SERVER", "MID_WEB_USER"), config.get("MID_SERVER", "MID_WEB_PASS"))
	
def getMetricDefs(config):
	defs = []
	for section in config.sections():	
		if ("metric" in section.lower()):	#config contains keyword metric
			value = -1
			if "value" in config.options(section):
				value = config.get(section, "VALUE")
				
			metricDef = MetricDef(config.get(section, "TYPE"), config.get(section, "NODE"), 
					config.get(section, "RESOURCE"), config.get(section, "DATA_FILE"), 
					config.get(section, "SOURCE"), value)
					
			defs.append(metricDef)
			
	return defs
	
def prepareJSON(metricDef, time, value):
	data = {
		  "metric_type": metricDef.type,
		  "resource": metricDef.resource,
		  "node": metricDef.node,
		  "value": value,
		  "timestamp": time,
		  "ci_identifier": {
			"node": metricDef.node,
		  },
		  "source": metricDef.source
		}
	return data
	
def sendMetrics(metrics, settings):
	r1 = requests.Session()
	headers = requestHeaders()
	
	res = r1.post(
			getMidURL(settings),
			headers=headers,
			auth=(settings.userName, settings.password),
			data=json.dumps(metrics)
		)
		
	print "Status code " + str(res.status_code)

	return res