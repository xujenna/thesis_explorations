import json
import csv
import pandas as pd
from pandas import DataFrame, Series
import dateutil.parser
from dateutil.tz import gettz
import datetime
import pytz
from functools import reduce



def roundTime(dt):
	dt = dt - datetime.timedelta(minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond)
	return dt


#keylogger DF

keyloggerData = json.loads(log.json)

tzinfos = { "EDT" : gettz("America/New_York") }

def extract_keyloggerData(data):
	result = []

	for d in data:
		tones = d['document_tone']['tones']
		if len(tones):
			for x in range(0, len(tones)):
				score = tones[x]['score']
				tone_name = tones[x]['tone_name']
				time = dateutil.parser.parse(d['time'] + " EDT", tzinfos=tzinfos)
				result.append((tone_name, score, time))
	return result

keyloggerDF = DataFrame(extract_keyloggerData(keyloggerData), columns=['tone_name', 'score', 'time'])
keyloggerDF.time = keyloggerDF.time.apply(roundTime)
keyloggerDF.time.apply(roundTime)


#affectiva DF

local_tz = gettz('America/New_York')

def utc_to_local(utc_dt):
	return utc_dt.replace(tzinfo=local_tz)

affectivaData = json.loads(merged_file.json)

for x in range(0, len(affectivaData)):
	affectivaData[x]['time'] = utc_to_local(datetime.datetime.fromtimestamp((affectivaData[x]['time']/ 1e3)))

affectivaDF = DataFrame(affectivaData)
affectivaDF.time = affectivaDF.time.apply(roundTime)
affectivaDF.time.apply(roundTime)
affectivaDF.emoji = affectivaDF.emoji.apply(lambda x: ",".join(x))
affectivaDF.emotions = affectivaDF.emotions.apply(lambda x: ",'".join(x))


#mood reporter DF

responsesData = pd.read_csv(responses.tsv, sep='\t', header=0)

timeValues = responsesData.time.values

for x in range(0, len(timeValues)):
	timeValues[x] = dateutil.parser.parse(timeValues[x] + " EDT", tzinfos=tzinfos)


timeValues = responsesData.time.values

for x in range(0, len(timeValues)):
	timeValues[x] = dateutil.parser.parse(timeValues[x] + " EDT", tzinfos=tzinfos)

# responsesData.time = timeValues
responsesData.time = responsesData.time.apply(roundTime)
responsesData.time.apply(roundTime)




#productivity DF

productivityFile = json.loads(productivity.json)

productivityData = productivityFile['rows']

final_productivityData = [];

for x in range(0, len(productivityData)):
	if(productivityData[x][0] > '2018-04-09T90:00:00'):
		time = dateutil.parser.parse(productivityData[x][0] + " EDT", tzinfos=tzinfos)
		prod_score = productivityData[x][4]
		final_productivityData.append((time, prod_score))

productivityDF = DataFrame(final_productivityData, columns=['time', 'productivity_score'])
productivityDF.time = productivityDF.time.apply(roundTime)
productivityDF.time.apply(roundTime)



#merge 

dfs = [keyloggerDF, affectivaDF, responsesData, productivityDF]
df_final = reduce(lambda left, right: pd.merge(left,right,on='time', how='inner'), dfs)


