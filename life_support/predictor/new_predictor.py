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
from sklearn.externals import joblib
from sklearn import ensemble

morale_RF = joblib.load('saved_models/combined_model/morale_RF.pkl')
mood_mean_diff_RF = joblib.load('saved_models/combined_model/mood_mean_diff_RF.pkl')
finalMergedDF = joblib.load('saved_models/combined_model/finalMergedDF.pkl')


responsesDF = pd.read_csv("../../trackers/reporter/responses.tsv", sep='\t', header=0)

moodIndex = len(responsesDF) - 1
currentIndexPredictions = {}
currentIndexPredictions['predictions'] = []



def convertTimeToStruct(timestamp):
	timestamp = time.gmtime(timestamp)
	return timestamp

def makePrediction(df):
	global moodIndex
    global updatedPrediction
    global currentIndexPredictions
    global productivity_pred
    global affectiva_pred
    global stepCount_pred


    responsesDF = pd.read_csv("../../trackers/reporter/responses.tsv", sep='\t', header=0)
    currentIndex = len(responsesDF) - 1


    if (currentIndex == moodIndex):
        print("updating this round's prediction")
    else:
        currentIndexPredictions['actual_mood'] = responsesDF['mood']
        currentIndexPredictions['actual_morale'] = responsesDF['morale']
        currentIndexPredictions['response_time'] = responsesDF['time']
    	writeToJSON(currentIndexPredictions)

        print("adding new round of predictions")
        moodIndex = currentIndex
        currentIndexPredictions['mood_index'] = moodIndex
        currentIndexPredictions['predictions'] = []
        updatedPrediction = {}

    rolling_mood_mean = responsesDF.iloc[-25:-1].mean()
    mood_prediction = mood_mean_diff_RF.predict(df) + rolling_mood_mean
    morale_prediction = morale_RF.predict(df)

    updatedPrediction['mood_prediction'] = mood_prediction
    updatedPrediction['morale_prediction'] = morale_prediction
    updatedPrediction['timestamp'] = datetime.datetime.now().timestamp()
    currentIndexPredictions['predictions'].append(updatedPrediction)
    updatedPrediction = {}


def writeToJSON(currentIndexPredictions):
	with open('RF_mood_predictions.json', 'r') as f:
		brackets = json.load(f)
	with open('RF_mood_predictions.json', 'r') as f:
		brackets.append(currentIndexPredictions)
		json.dump(brackets, f, indent=2)


def updateData():
	# get last row value of all trackers except responses
	# make df
	# if(df.equals(prev_df)):
	#	break
	# else:
	#	makePrediction(df)
