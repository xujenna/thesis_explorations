import json
import csv
import pandas as pd
from pandas import DataFrame, Series
import dateutil.parser
from dateutil.tz import gettz
import datetime
import pytz
from functools import reduce
import time
import codecs
import os

# train tracker models on entire dataset for mood, morale, stress, fatigue, compulsion
# test on respective columns of big merged DF
# test predictions become training data for final prediction model
# final prediction model updates every 15 minutes


# browser activity tv column (amazon.com)

def roundUnixTime(timestamp):
    timestamp = timestamp - (timestamp % 3600)
    return timestamp

def convertTime(timestamp):
    timestamp = time.gmtime(timestamp)
    return timestamp

def convertUTCToTimestamp(timestamp):
    nanosecondTimestamp = timestamp * 1e9
    timestamp = pd.Timestamp(nanosecondTimestamp, tz='US/Eastern')
    return timestamp


# Mood Reporter DF

responsesDF = pd.read_csv("../../trackers/reporter/responses.tsv", sep='\t', header=0)

activity_names = list(set(list(map(lambda x: x.lower().strip(), reduce(lambda x,y: x+y, [x.split(",") for x in list(responsesDF.activity.values)])))))

for activity_name in activity_names:
    responsesDF[activity_name.replace(" ", "_") + "_activity"] = responsesDF.activity.apply(lambda x: activity_name in x.lower())

location_names = list(set(list(map(lambda x: x.lower().strip(), reduce(lambda x,y: x+y, [x.split(",") for x in list(responsesDF.location.values)])))))

def split_locations(locations):
    return list(map(lambda x: x.lower().strip(), locations.split(",")))

for location_name in location_names:
    responsesDF[location_name.replace(" ", "_") + "_location"] = responsesDF.location.apply(lambda x: location_name in split_locations(x))

responsesDF.time = responsesDF.unix_time

responsesDF.time = responsesDF.time.apply(convertUTCToTimestamp)

del responsesDF['moodNotes']
del responsesDF['trigger']
del responsesDF['activity']
del responsesDF['location']
del responsesDF['unix_time']

moodDF = responsesDF[['time','mood']].copy()
moraleDF = responsesDF[['time', 'morale']].copy()
stressDF = responsesDF[['time', 'stress']].copy()
fatigueDF = responsesDF[['time', 'fatigue']].copy()
compulsionDF = responsesDF[['time', 'compulsions']].copy()




# Keylogger Model

def trainKeylogger():
    tone_names = ['Sadness', 'Analytical', 'Joy', 'Fear', 'Tentative', 'Anger', 'Confident']

    with open('../../trackers/keylogger/logs/log_new.json', 'r') as f:
        keyloggerData = json.load(f)

    def extract_keyloggerData(data):
        results = []

        for d in data:
            result = [0]*(len(tone_names) + 6)
            try:
                result[7] = d['word_count']
    #             result[8] = d['uniqueword_count']
                result[8] = d['uniqueword_ratio']
    #             result[9] = d['char_count']
                result[9] = d['backspace_count']
                result[10] = d['avg_dwelltime']
                result[11] = d['avg_flighttime']

                tones = d['document_tone']['tones']
                for i in range(len(tones)):
                    score = tones[i]['score']
                    tone_name = tones[i]['tone_name']
                    tone_index = tone_names.index(tone_name)
                    result[tone_index] = score            

    #             time = utc_to_local(datetime.datetime.fromtimestamp(d['unix_time']))
    #             result[-1] = time.gmtime(d['unix_time'])
                result[-1] = d['unix_time']

                results.append(tuple(result))
            except:
                continue
                
        return results

    keyloggerDF = DataFrame(extract_keyloggerData(keyloggerData),
                            columns=[tone_name+"_score" for tone_name in tone_names] + ['word_count','uniqueword_ratio', 'backspace_count','avg_dwelltime','avg_flighttime','time'])

    keyloggerDF.time = keyloggerDF.time.apply(convertUTCToTimestamp)
    
    pd.merge_asof(moodDF, keyloggerDF, on='time', tolerance=(3600*2))

    keyloggerFeatures = list(keyloggerDF.columns.drop())



def keyloggerModel():




# Final Prediction Model

def finalPredictions():
    keyloggerPrediction = keyloggerModel()
    affectivaPrediction = affectivaModel()
    productivityPrediction = productivityModel()
    browserActivityPrediction = browserActivityModel()
    stepCountPrediction = stepCountModel()
    timePrediction = timeModel()


