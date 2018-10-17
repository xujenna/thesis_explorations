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

from keras.models import load_model

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.preprocessing import MinMaxScaler

from pandas import concat

from keras.models import Sequential
from keras.layers import LSTM 
from keras.layers import Dense
from keras.optimizers import Adam
import keras.backend as K

mood_model = load_model('LSTM_mood_predictor_no_reporter.h5')
fatigue_model = load_model('LSTM_fatigue_predictor_no_reporter.h5')
stress_model = load_model('LSTM_stress_predictor_no_reporter.h5')

scaler = joblib.load('scaler.pkl')
scaler_stress = joblib.load('scaler_stress.pkl')

responsesDF = pd.read_csv("../../../trackers/reporter/responses.tsv", sep='\t', header=0)

moodIndex = len(responsesDF) - 1
currentIndexPredictions = {}
currentIndexPredictions['predictions'] = []
latest_hour = 0

finalFeaturesList = ['mood',
'stress',
'fatigue',
 'avg_attention',
 'avg_engagement',
 'avg_valence',
 'blinks',
 'emoji',
 'Sadness_score',
 'Analytical_score',
 'Joy_score',
 'Fear_score',
 'Tentative_score',
 'Anger_score',
 'Confident_score',
 'word_count',
 'uniqueword_ratio',
 'backspace_count',
 'avg_dwelltime',
 'avg_flighttime',
 'stepCount',
 'current_tabCount',
 'current_windowCount',
 'tabs_activated',
 'tabs_created',
 'windows_created',
 'productivity_score',
 'hour']


tempRow = [[0] * len(finalFeaturesList)]
df = pd.DataFrame(tempRow, columns=finalFeaturesList)
df['mood'] = responsesDF['mood'].iloc[-1]
df['fatigue'] = responsesDF['fatigue'].iloc[-1]


prev_df = pd.DataFrame()

keylogger_lastUpdateTime = 0
tabCounter_lastUpdateTime = 0
productivity_lastUpdateTime = 0
affectiva_lastUpdateTime = 0
stepCount_lastUpdateTime = 0
responses_lastUpdateTime = 0


def convertTimeToStruct(timestamp):
    timestamp = time.gmtime(timestamp)
    return timestamp

def predictor(df, label):
    cols = list(df)
    cols.insert(0, cols.pop(cols.index(label)))
    df = df.loc[:,cols]

    values = df.values
    values = values.astype('float32')
    if(label == "stress"):
        test_X = scaler_stress.transform(values)
    else:
        test_X = scaler.transform(values)
    
    print("Predicting on: ")
    print(test_X)

    # make a  prediction
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    yhat = DataFrame(mood_model.predict(test_X))
    test_X = DataFrame(test_X.reshape((test_X.shape[0], test_X.shape[2])))
    # invert scaling for forecast
    inv_yhat = concat((yhat, test_X.iloc[:, 1:]), axis=1)
    inv_yhat = scaler.inverse_transform(inv_yhat)
    inv_yhat = inv_yhat[:,0]

    return inv_yhat


def makePrediction(df):
    global moodIndex
    global updatedPrediction
    global currentIndexPredictions
    global productivity_pred
    global affectiva_pred
    global stepCount_pred

    currentHour = time.localtime().tm_hour

    df['hour'] = currentHour

    responsesDF = pd.read_csv("../../../trackers/reporter/responses.tsv", sep='\t', header=0)
    lastResponsesRow = responsesDF.iloc[-1]
    currentIndex = len(responsesDF)

    fatigueDF = df.copy()
    fatigueDF['fatigue'] = lastResponsesRow['fatigue']
    del fatigueDF['mood']
    del fatigueDF['stress']

    moodDF = df.copy()
    moodDF['mood'] = lastResponsesRow['mood']
    del moodDF['fatigue']
    del moodDF['stress']

    stressDF = df.copy()
    stressDF['stress'] = lastResponsesRow['stress']
    del stressDF['fatigue']
    del stressDF['mood']

    
    if (currentIndex == moodIndex):
        mood_prediction = predictor(moodDF, "mood")
        stress_prediction = predictor(stressDF, "stress")
        fatigue_prediction = predictor(fatigueDF, "fatigue")

        print("------------------------")
        print("current mood prediction:")
        print(mood_prediction)
        print("------------------------")
        print("current stress prediction:")
        print(stress_prediction)
        print("------------------------")
        print("current fatigue prediction:")
        print(fatigue_prediction)
        print("------------------------")

        updatedPrediction['LSTM_mood_prediction'] = mood_prediction[0]
        updatedPrediction['LSTM_stress_prediction'] = stress_prediction[0]
        updatedPrediction['LSTM_fatigue_prediction'] = fatigue_prediction[0]
        updatedPrediction['timestamp'] = datetime.datetime.now().timestamp()
        currentIndexPredictions['predictions'].append(updatedPrediction)
        updatedPrediction = {}

    else:
        if(len(currentIndexPredictions['predictions']) > 0):
            mood_prediction = predictor(moodDF, "mood")
            stress_prediction = predictor(stressDF, "stress")
            fatigue_prediction = predictor(fatigueDF, "fatigue")

            updatedPrediction['LSTM_mood_prediction'] = mood_prediction[0]
            updatedPrediction['LSTM_stress_prediction'] = stress_prediction[0]
            updatedPrediction['LSTM_fatigue_prediction'] = fatigue_prediction[0]
            updatedPrediction['timestamp'] = datetime.datetime.now().timestamp()
            currentIndexPredictions['predictions'].append(updatedPrediction)

            print("------------------------")
            print("actual mood for last round: ")
            print(lastResponsesRow['mood'])
            print("last prediction for last round: ")
            print(mood_prediction)
            print("------------------------")
            print("actual stress for last round: ")
            print(lastResponsesRow['stress'])
            print("last prediction for last round: ")
            print(stress_prediction)
            print("------------------------")
            print("actual fatigue for last round: ")
            print(lastResponsesRow['fatigue'])
            print("last prediction for last round: ")
            print(fatigue_prediction)
            print("------------------------")

            currentIndexPredictions['actual_mood'] = lastResponsesRow['mood']
            currentIndexPredictions['actual_stress'] = lastResponsesRow['stress']
            currentIndexPredictions['actual_fatigue'] = lastResponsesRow['fatigue']
            currentIndexPredictions['response_time'] = lastResponsesRow['time']
            writeToJSON(currentIndexPredictions)

        print("starting new round of predictions")
        moodIndex = currentIndex
        currentIndexPredictions['mood_index'] = moodIndex
        currentIndexPredictions['predictions'] = []
        updatedPrediction = {}


def writeToJSON(currentIndexPredictions):
    with open('LSTM_new_predictor.json', 'r') as f:
        brackets = json.load(f)
    with open('LSTM_new_predictor.json', 'w') as f:
        brackets.append(currentIndexPredictions)
        json.dump(brackets, f, indent=2)


while True:
    print("checking for file updates...")
    df_updated = False

    keyloggerFile_lastUpdateTime = os.path.getmtime('../../../trackers/keylogger/logs/log_new.json')
    productivityFile_lastUpdateTime = os.path.getmtime('../../../trackers/getAPIdata/productivity.json')
    affectivaFile_lastUpdateTime = os.path.getmtime('../../../trackers/getAPIdata/merged_file.json')
    stepCountFile_lastUpdateTime = os.path.getmtime('../../../trackers/google_fit/dataset.json')
    responsesFile_lastUpdateTime = os.path.getmtime('../../../trackers/reporter/responses.tsv')
    tabCounterFile_lastUpdateTime = os.path.getmtime('../../../trackers/getAPIdata/chromeactivity.json')
    # heartRateFile_lastUpdateTime = os.path.getmtime('../../../trackers/webcam-pulse-detector-no_openmdao/heartRate.csv')
    
    # keylogger update
    if(keyloggerFile_lastUpdateTime > keylogger_lastUpdateTime):
        print("keylogger file updated")
        with open('../../../trackers/keylogger/logs/log_new.json', 'r') as f:
            keyloggerFile = json.load(f)

        tone_names = ['Sadness', 'Analytical', 'Joy', 'Fear', 'Tentative', 'Anger', 'Confident']

        def extract_keyloggerData(data):
            result= [0] * (len(tone_names))
            tones = data['document_tone']['tones']
            for i in range(len(tones)):
                score = tones[i]['score']
                tone_name = tones[i]['tone_name']
                tone_index = tone_names.index(tone_name)
                result[tone_index] = score			

            return result


        keyloggerData = keyloggerFile[-1]

        df.loc[[0],'word_count'] = keyloggerData['word_count']
        df.loc[[0],'uniqueword_ratio'] = keyloggerData['uniqueword_ratio']
        df.loc[[0],'backspace_count'] = keyloggerData['backspace_count']
        df.loc[[0],'avg_dwelltime'] = keyloggerData['avg_dwelltime']
        df.loc[[0],'avg_flighttime'] = keyloggerData['avg_flighttime']

        sentimentData = extract_keyloggerData(keyloggerData)

        df.loc[[0],'Sadness_score'] = sentimentData[0]
        df.loc[[0],'Analytical_score'] = sentimentData[1]
        df.loc[[0],'Joy_score'] = sentimentData[2]
        df.loc[[0],'Fear_score'] = sentimentData[3]
        df.loc[[0],'Tentative_score'] = sentimentData[4]
        df.loc[[0],'Anger_score'] = sentimentData[5]
        df.loc[[0],'Confident_score'] = sentimentData[6]

        keylogger_lastUpdateTime = datetime.datetime.now().timestamp()
        df_updated = True



    # productivity update
    if(productivityFile_lastUpdateTime > productivity_lastUpdateTime):
        print("productivity file updated")
        with open('../../../trackers/getAPIdata/productivity.json', 'r') as f:
            productivityFile = json.load(f)

        productivityData = productivityFile['rows']
        df['productivity_score'] = productivityData[-1][4]

        productivity_lastUpdateTime = datetime.datetime.now().timestamp()
        df_updated = True


    # affectiva update
    if(affectivaFile_lastUpdateTime > affectiva_lastUpdateTime):
        print("affectiva file updated")
        with open('../../../trackers/getAPIdata/merged_file.json', 'r') as f:
            affectivaFile = json.load(f)

        affectivaData = affectivaFile[-1]

        df.loc[[0],'avg_attention'] = affectivaData['avg_attention']
        df.loc[[0],'avg_engagement'] = affectivaData['avg_engagement']
        df.loc[[0],'avg_valence'] = affectivaData['avg_valence']
        df.loc[[0],'blinks'] = affectivaData['blinks']

        affectiva_lastUpdateTime = datetime.datetime.now().timestamp()
        df_updated = True


    #tabcounter

    if(tabCounterFile_lastUpdateTime > tabCounter_lastUpdateTime):
        print("tabCounter file updated")
        with open('../../../trackers/getAPIdata/chromeactivity.json', 'r') as f:
            tabCounterFile = json.load(f)

        lastKey = list(tabCounterFile.keys())[-1]
        tabCounterData = tabCounterFile[lastKey]

        df.loc[[0],'current_tabCount'] = tabCounterData['current_tabCount']
        df.loc[[0],'current_windowCount'] = tabCounterData['current_windowCount']
        df.loc[[0],'tabs_activated'] = tabCounterData['tabs_activated']
        df.loc[[0],'tabs_created'] = tabCounterData['tabs_created']
        df.loc[[0],'windows_created'] = tabCounterData['windows_created']

        tabCounter_lastUpdateTime = datetime.datetime.now().timestamp()
        df_updated = True


    # stepCount update
    if(stepCountFile_lastUpdateTime > stepCount_lastUpdateTime):
        print("stepCount file updated")
        with open('../../../trackers/google_fit/dataset.json', 'r') as f:
            fitFile = json.load(f)
            fitData = fitFile['point'][-20:-1]

        if(convertTimeToStruct(int(fitData[len(fitData)-1]['endTimeNanos']) / 1e9) == latest_hour):
            latestStepCount = 0
        else:
            latest_hour = convertTimeToStruct(int(fitData[len(fitData)-1]['endTimeNanos']) / 1e9)
            latestStepCount = 0

            for index in range(len(fitData) - 1, 0, -1):
                current_hour = convertTimeToStruct(int(fitData[index]['endTimeNanos']) / 1e9)
                if (latest_hour.tm_year == current_hour.tm_year and latest_hour.tm_mon == current_hour.tm_mon and latest_hour.tm_mday == current_hour.tm_mday and latest_hour.tm_hour == current_hour.tm_hour):
                    latestStepCount += int(fitData[index]['value'][0]['intVal'])
                else:
                    break

        df.loc[[0],'stepCount'] = latestStepCount
        stepCount_lastUpdateTime = datetime.datetime.now().timestamp()
        df_updated = True


    #heart rate update
    # if(heartRateFile_lastUpdateTime > heartRate_lastUpdateTime):
    # 	heartRateDF = pd.read_csv("../webcam-pulse-detector-no_openmdao/heartRate.csv", sep=',', header=0)
    # 	df.loc[[0], 'heart']
    # 	heartRateDF.iloc[-1]

    # if not(df.equals(prev_df)):
    # 	makePrediction(df)
    # 	prev_df = df.copy()
    # else:
    # 	print("no new data")

    if(df_updated):
        makePrediction(df)
        prev_df = df.copy()
    else:
        print("no new data")

    time.sleep(900)

