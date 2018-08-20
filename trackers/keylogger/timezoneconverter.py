import dateutil.parser
import datetime
import pytz
from pytz import timezone
import json

NYtz = timezone('America/New_York')
CHItz = timezone('America/Chicago')
LAtz = timezone('America/Los_Angeles')
COtz = timezone('America/Denver')
epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.UTC)

with open('log_new_copy.json', 'r') as f:
	keyloggerData = json.load(f)

# keyloggerData = keyloggerFile['rows']


with open('newlog.json', 'w+') as f:
	for x in range(0, len(keyloggerData)):
		if ((keyloggerData[x]['time'] > '2018-05-11T18:00:00.000000' and keyloggerData[x]['time'] < '2018-05-16T20:00:00.000000') or (keyloggerData[x]['time'] > '2018-08-06T18:20:00.000000' and keyloggerData[x]['time'] < '2018-08-13T15:10:00.000000')):
			parsedDate = dateutil.parser.parse(keyloggerData[x]['time'])
			withTimeZone = CHItz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()
			keyloggerData[x]['unix_time'] = newTimestamp
		elif (keyloggerData[x]['time'] > '2018-06-15T18:00:00.000000' and keyloggerData[x]['time'] < '2018-07-08T19:00:00.000000'):
			parsedDate = dateutil.parser.parse(keyloggerData[x]['time'])
			withTimeZone = LAtz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()
			keyloggerData[x]['unix_time'] = newTimestamp
		elif (keyloggerData[x]['time'] > '2018-08-13T15:10:00.000000' and keyloggerData[x]['time'] < '2018-08-18T05:00:00.000000'):
			parsedDate = dateutil.parser.parse(keyloggerData[x]['time'])
			withTimeZone = COtz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()
			keyloggerData[x]['unix_time'] = newTimestamp
		else:
			parsedDate = dateutil.parser.parse(keyloggerData[x]['time'])
			withTimeZone = NYtz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()
			keyloggerData[x]['unix_time'] = newTimestamp

	json.dump(keyloggerData, f, indent=2)