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


# ML

def makePrediction(df):

    newPredictions = {}
    actual = df.iloc[-1]['mood']
    timestamp = df.iloc[-1]['time']

    newPredictions['actual_mood'] = actual
    newPredictions['time'] = timestamp



    featuresList = list(df.columns.drop('mood').drop('time'))


    from sklearn import linear_model

    newPredictions['linear_model'] = {}

    y = df["mood"][:-1]
    X = df[featuresList][:-1]

    myLinearModel = linear_model.LinearRegression()
    myLinearModel = myLinearModel.fit(X, y)

    #predict mood for latest df row
    X_latest = df.iloc[-1].drop("mood").drop("time")
    LMprediction = myLinearModel.predict([X_latest])
    newPredictions['linear_model']['prediction'] = LMprediction[0]

    #calculate the mean absolute error
    from sklearn.model_selection import train_test_split

    #set aside 20% of the data to use as test data; the rest will be used as training data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42)

    #train a linear model on the training data
    myLinearModel2 = linear_model.LinearRegression()
    myLinearModel2 = myLinearModel2.fit(X_train, y_train)

    #predict on test data and print the results
    y_pred_lm = myLinearModel.predict(X_test)

    from sklearn.metrics import mean_squared_error, mean_absolute_error
    LMmeanAbsoluteError = mean_absolute_error(y_test, y_pred_lm)

    newPredictions['linear_model']['mean_abs_error'] = LMmeanAbsoluteError



    #RANDOM FOREST

    #train a random forest on the training data
    from sklearn import ensemble

    newPredictions['random_forest'] = {}

    random_forest = ensemble.RandomForestRegressor()
    random_forest = random_forest.fit(X, y)

    #predict mood for latest df row
    RFprediction = random_forest.predict([X_latest])
    newPredictions['random_forest']['prediction'] = RFprediction[0]

    #calculate the mean absolute error
    random_forest2 = ensemble.RandomForestRegressor()
    random_forest2 = random_forest2.fit(X_train, y_train)

    #predict on the test data and print the results
    y_pred_rf = random_forest2.predict(X_test)

    RFmeanAbsoluteError = mean_absolute_error(y_test, y_pred_rf)
    newPredictions['random_forest']['mean_abs_error'] = RFmeanAbsoluteError


    with open('predictions.json', 'r') as f:
        brackets = json.load(f)
    with open('predictions.json', 'w') as f:
        brackets.append(newPredictions)
        json.dump(brackets, f, indent=2)


    print(newPredictions)







previousDFlength = 0
currentDFlength = 0

while True:

    # KEYLOGGER DF

    tone_names = ['Sadness', 'Analytical', 'Joy', 'Fear', 'Tentative', 'Anger', 'Confident']
    tone_names

    with open('../../trackers/keylogger/logs/log_new.json', 'r') as f:
        keyloggerData = json.load(f)

    # tzinfos = { "EDT" : gettz("America/New_York") }

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
    # keyloggerDF.time = keyloggerDF.time.apply(roundTime)
    #keyloggerDF.time.apply(roundTime)



    # AFFECTIVA DF

    with open('../../trackers/affectiva/analyses/merged_file.json', 'r') as f:
        affectivaData = json.load(f)

    for x in range(0, len(affectivaData)):
    #         affectivaData[x]['time'] = time.gmtime(affectivaData[x]['time']/ 1e3)
            affectivaData[x]['time'] = affectivaData[x]['time']/ 1e3

    #     affectivaData[x]['time'] = utc_to_local(datetime.datetime.fromtimestamp((affectivaData[x]['time']/ 1e3)))

    affectivaDF = DataFrame(affectivaData)
    # affectivaDF.time = affectivaDF.time.apply(roundTime)
    # affectivaDF.time.apply(roundTime)
    #affectivaDF.emoji = affectivaDF.emoji.apply(lambda x: ",".join(x))
    del affectivaDF['emoji']
    #affectivaDF.emotions = affectivaDF.emotions.apply(lambda x: ",".join(x))
    del affectivaDF['emotions']
    del affectivaDF['max_attention']
    del affectivaDF['min_attention']
    del affectivaDF['max_engagement']
    del affectivaDF['min_engagement']
    del affectivaDF['max_valence']
    del affectivaDF['min_valence']
    # affectivaDF.time = affectivaDF.time.apply(roundTime)




    #MOOD REPORTER DF

    responsesDF = pd.read_csv("../../trackers/reporter/responses.tsv", sep='\t', header=0)

    timeValues = responsesDF.unix_time.values

    def roundUnixTime(timestamp):
        timestamp = timestamp - (timestamp % 3600)
        return timestamp

    def convertTime(timestamp):
        timestamp = time.gmtime(timestamp)
        return timestamp

    # for x in range(0, len(timeValues)):
    #     timestamp = time.gmtime(timeValues[x])
    #     print(timestamp)
    #     timeValues[x] = timestamp

    #     timeValues[x] = utc_to_local(datetime.datetime.fromtimestamp(timeValues[x]))
    #     timeValues[x] = dateutil.parser.parse(timeValues[x] + " EDT", tzinfos=tzinfos)


    # responsesData.time = timeValues
    #responsesData.time = responsesData.time.apply(roundTime)

    activity_names = list(set(list(map(lambda x: x.lower().strip(), reduce(lambda x,y: x+y, [x.split(",") for x in list(responsesDF.activity.values)])))))

    for activity_name in activity_names:
        responsesDF[activity_name.replace(" ", "_") + "_activity"] = responsesDF.activity.apply(lambda x: activity_name in x.lower())

    location_names = list(set(list(map(lambda x: x.lower().strip(), reduce(lambda x,y: x+y, [x.split(",") for x in list(responsesDF.location.values)])))))

    def split_locations(locations):
        return list(map(lambda x: x.lower().strip(), locations.split(",")))

    for location_name in location_names:
        responsesDF[location_name.replace(" ", "_") + "_location"] = responsesDF.location.apply(lambda x: location_name in split_locations(x))

    # responsesDF.time = responsesDF.unix_time.apply(roundUnixTime)
    # responsesDF.time = responsesDF.time.apply(convertTime)
    responsesDF.time = responsesDF.unix_time

    del responsesDF['moodNotes']
    del responsesDF['trigger']
    del responsesDF['activity']
    del responsesDF['location']
    del responsesDF['unix_time']




    #PRODUCTIVTY DF

    from dateutil import parser
    import calendar

    with open('../../trackers/getAPIdata/productivity.json', 'r') as f:
        productivityFile = json.load(f)

    productivityData = productivityFile['rows']

    final_productivityData = [];
    UTC = pytz.timezone('UTC')

    for x in range(0, len(productivityData)):
    #     if(productivityData[x][0] > '2018-04-01T00:00:00'):
        date = parser.parse(productivityData[x][0])
        dateutc = str(date.astimezone(UTC))
        dateutc2 = dateutc[:19] + "UTC"
        newtime = time.strptime(dateutc2, "%Y-%m-%d %H:%M:%S%Z")
        finalTime = calendar.timegm(newtime)
        prod_score = productivityData[x][4]
        final_productivityData.append((finalTime, prod_score))

    productivityDF = DataFrame(final_productivityData, columns=['time', 'productivity_score'])
    #productivityDF.time = productivityDF.time.apply(roundTime)
    # productivityDF.time.apply(roundTime)











    #TABCOUNTER

    with open('../../trackers/getAPIdata/chromeactivity.json', 'r') as f:
        tabCounterData = json.load(f)

    newTabData = []

    for key in tabCounterData:
        timestamp = int(key) / 1e3

    #     timestamp = time.gmtime(int(key) / 1e3)
    #     time = utc_to_local(datetime.datetime.fromtimestamp((int(key)/ 1e3)))
        current_tabCount = tabCounterData[key]['current_tabCount']
        current_windowCount = tabCounterData[key]['current_windowCount']
        tabs_activated = tabCounterData[key]['tabs_activated']
        tabs_created = tabCounterData[key]['tabs_created']
        windows_created = tabCounterData[key]['windows_created']

        newTabData.append([timestamp, current_tabCount, current_windowCount,tabs_activated,tabs_created,windows_created])

    tabColumns = ['time', 'current_tabCount', 'current_windowCount','tabs_activated','tabs_created','windows_created']
    tabCounterDF = DataFrame(newTabData, columns=tabColumns)
    # tabCounterDF.time = tabCounterDF.time.apply(roundTime)





    # MERGED DF
    import time

    def convertTime(timestamp):
        timestamp = time.gmtime(timestamp)
        return timestamp

    mergedData = []

    all_columns = list(responsesDF.columns) + list(keyloggerDF.columns.drop('time')) + list(affectivaDF.columns.drop('time')) + list(productivityDF.columns.drop('time')) + list(tabCounterDF.columns.drop('time'))

    def process_row(row):
        current_time = row['time']

        output_values = list(row.values)

        for other_df in [keyloggerDF, affectivaDF, productivityDF, tabCounterDF]:
            candidates = other_df[(current_time >= other_df['time']) &
                                  (((current_time - other_df['time']) / 3600) < 3.5)]

    #         candidates = other_df[(current_time >= other_df['time']) &
    #                               (current_time - other_df['time'] < datetime.timedelta(hours=3.5))]
            if candidates.empty:
                return None
            else:
                index_of_max = candidates['time'].argmax()
                candidate = candidates.ix[index_of_max].drop('time')
                output_values += list(candidate.values)
        return output_values

    for index, row in responsesDF.iterrows():
        processed_row = process_row(row)
        if processed_row is not None:
            mergedData.append(processed_row)

    mergedDF = DataFrame(mergedData, columns = all_columns)

    # mergedDF.time = mergedDF.time.apply(convertTime)








    #ADD HOUR COLUMN

    def hourOnly(timestamp):
        timestamp = timestamp.hour
        if (timestamp < 6):
            timestamp = timestamp + 24
        return timestamp



    hourColumn = pd.to_datetime(mergedDF.time, unit='s')
    hourColumn = hourColumn.apply(hourOnly)

    mergedDF = mergedDF.assign(time_of_day=pd.Series(hourColumn).values)

    mergedDF = mergedDF.fillna(0)




    previousDFlength = currentDFlength
    currentDFlength = len(mergedDF)


    if (previousDFlength < currentDFlength):
        makePrediction(mergedDF)
        time.sleep(3600)
    elif (previousDFlength == currentDFlength):
        time.sleep(600)



