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

# train tracker models on entire dataset for mood, morale, stress, fatigue, compulsion
# test on respective columns of big merged DF
# test predictions become training data for final prediction model
# final prediction model updates every 15 minutes

productivity_mood_SVR = joblib.load('saved_models/productivity_mood_SVR.pkl')
affectiva_mood_LM = joblib.load('saved_models/affectiva_mood_LM.pkl')
stepCount_mood_SVR = joblib.load('saved_models/stepCount_mood_SVR.pkl')
ensemble_mood_SVR = joblib.load('saved_models/ensemble_mood_SVR.pkl')

productivity_lastUpdateTime = 0
affectiva_lastUpdateTime = 0
stepCount_lastUpdateTime = 0
responses_lastUpdateTime = 0

latest_hour = 0
responsesLength = 0
currentIndexPredictions = {}
currentIndexPredictions['predictions'] = []


def convertTimeToStruct(timestamp):
    timestamp = time.gmtime(timestamp)
    return timestamp


def ensemble_model_mood(prediction, type):
    global responsesLength
    global updatedPrediction
    global currentIndexPredictions
    global productivity_pred
    global affectiva_pred
    global stepCount_pred

    responsesDF = pd.read_csv("../../trackers/reporter/responses.tsv", sep='\t', header=0)

    if ((len(responsesDF) - 1) == responsesLength):
        print("updating prediction")
    else:
        print("adding new round of predictions")
        responsesLength = len(responsesDF) - 1
        currentIndexPredictions['mood_index'] = responsesLength
        currentIndexPredictions['predictions'] = []
        updatedPrediction = {}


    # if(currentTime.tm_hour == currentHour.tm_hour):
    #     continue
    # else:
    #     currentHour = currentTime.replace(minute=0, second=0)

    if (type == 'productivity'):
        productivity_pred = prediction
        updatedPrediction['productivity_pred'] = prediction[0]
        print("productivity_pred:")
        print(productivity_pred)
    elif(type == 'affectiva'):
        affectiva_pred = prediction
        updatedPrediction['affectiva_pred'] = prediction[0]
        print("affectiva_pred:")
        print(affectiva_pred)
    elif(type == 'stepCount'):
        stepCount_pred = prediction
        updatedPrediction['stepCount_pred'] = prediction[0]
        print("stepCount_pred:")
        print(stepCount_pred)
    elif(type =='actual_score'):
        currentIndexPredictions['actual_score'] = prediction
        print("actual_score:")
        print(prediction)
        writeToJSON(currentIndexPredictions)

    try:
        latestDataDF = pd.DataFrame()
        latestDataDF['productivity_pred'] = productivity_pred
        latestDataDF['affectiva_pred'] = affectiva_pred
        latestDataDF['stepCount_pred'] = stepCount_pred
        print("predicting on:")
        print(latestDataDF)

        ensemble_pred = ensemble_mood_SVR.predict(latestDataDF)
        print("------------------------------")
        print("------------------------------")
        print("current mood prediction:")
        print(ensemble_pred)
        print("------------------------------")
        print("------------------------------")
        updatedPrediction['ensemble_pred'] = ensemble_pred[0]
        updatedPrediction['timestamp'] = datetime.datetime.now().timestamp()
        currentIndexPredictions['predictions'].append(updatedPrediction)
        updatedPrediction = {}

    except:
        print("waiting to fill row")


def writeToJSON(predictions):

    with open('ensemble_predictions.json', 'r') as f:
        brackets = json.load(f)
    with open('ensemble_predictions.json', 'w') as f:
        brackets.append(predictions)
        json.dump(brackets, f, indent=2)
    print("Wrote to JSON:")
    print(predictions)


productivity_Updated = False
affectiva_Updated = False
stepCount_Updated = False

while True:
    print("checking for file updates...")
    productivityFile_lastUpdateTime = os.path.getmtime('../../trackers/getAPIdata/productivity.json')
    affectivaFile_lastUpdateTime = os.path.getmtime('../../trackers/getAPIdata/merged_file.json')
    stepCountFile_lastUpdateTime = os.path.getmtime('../../trackers/google_fit/dataset.json')
    responsesFile_lastUpdateTime = os.path.getmtime('../../trackers/reporter/responses.tsv')

    #update productivity prediction
    if(productivityFile_lastUpdateTime > productivity_lastUpdateTime):
        print("productivity file updated")
        with open('../../trackers/getAPIdata/productivity.json', 'r') as f:
            productivityFile = json.load(f)

        productivityData = productivityFile['rows']
        latestProductivityScore = productivityData[-1][4]
        latestProductivityMoodPred = productivity_mood_SVR.predict(latestProductivityScore)
        # print("productivity prediction:")
        # print(latestProductivityMoodPred)
        ensemble_model_mood(latestProductivityMoodPred, 'productivity')

        productivity_lastUpdateTime = datetime.datetime.now().timestamp()
        productivity_Updated = True

    #update affectiva prediction
    if(affectivaFile_lastUpdateTime > affectiva_lastUpdateTime):
        print("affectiva file updated")
        with open('../../trackers/getAPIdata/merged_file.json', 'r') as f:
            affectivaFile = json.load(f)

        latestAffectivaData = []
        latestAffectivaData.append(affectivaFile[-1])

        latestAffectivaDF = DataFrame(latestAffectivaData)
        affectivaFeaturesList = ['avg_attention', 'avg_engagement', 'avg_valence', 'blinks']

        finalAffectivaDF = latestAffectivaDF[affectivaFeaturesList]

        latestAffectivaMoodPred = affectiva_mood_LM.predict(finalAffectivaDF)
        # print("affectiva prediction:")
        # print(latestAffectivaMoodPred)
        ensemble_model_mood(latestAffectivaMoodPred, 'affectiva')

        affectiva_lastUpdateTime = datetime.datetime.now().timestamp()
        affectiva_Updated = True

    #update stepCount prediction
    if(stepCountFile_lastUpdateTime > stepCount_lastUpdateTime):
        print("stepCount file updated")
        with open('../../trackers/google_fit/dataset.json', 'r') as f:
            fitFile = json.load(f)
            fitData = fitFile['point']

        if(convertTimeToStruct(int(fitData[len(fitData)-1]['endTimeNanos']) / 1e9) == latest_hour):
            latestStepCount = 0
            lateststepCountMoodPred = stepCount_mood_SVR.predict(latestStepCount)
        else:

            latest_hour = convertTimeToStruct(int(fitData[len(fitData)-1]['endTimeNanos']) / 1e9)
            latestStepCount = 0

            for index in range(len(fitData) - 1, 0, -1):
                current_hour = convertTimeToStruct(int(fitData[index]['endTimeNanos']) / 1e9)
                if (latest_hour.tm_year == current_hour.tm_year and latest_hour.tm_mon == current_hour.tm_mon and latest_hour.tm_mday == current_hour.tm_mday and latest_hour.tm_hour == current_hour.tm_hour):
                    latestStepCount += int(fitData[index]['value'][0]['intVal'])
                else:
                    break

            latestStepCountMoodPred = stepCount_mood_SVR.predict(latestStepCount)
            # print("stepCount prediction:")
            # print(latestStepCountMoodPred)
        ensemble_model_mood(latestStepCountMoodPred, 'stepCount')

        stepCount_lastUpdateTime = datetime.datetime.now().timestamp()
        stepCount_Updated = True


    #update actual mood score
    if(responsesFile_lastUpdateTime > responses_lastUpdateTime and productivity_Updated == True and affectiva_Updated == True and stepCount_Updated == True):
        print("all files have updated")
        responsesDF = pd.read_csv("../../trackers/reporter/responses.tsv", sep='\t', header=0)

        latestMoodScore = responsesDF.iloc[-1]['mood']
        # print("actual mood score:")
        # print(latestMoodScore)        
        ensemble_model_mood(latestMoodScore, 'actual_score')

        responses_lastUpdateTime = datetime.datetime.now().timestamp()
        productivity_Updated = False
        affectiva_Updated = False
        stepCount_Updated = False

    time.sleep(900)




