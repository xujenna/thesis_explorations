#! /usr/bin/env python
#-*- coding: utf-8 -*-

import json
import httplib2

import time
from datetime import datetime
from datetime import timedelta
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

# Copy your credentials from the Google Developers Console
CLIENT_ID = '1004366226772-s8jsvjt512nn3tep97ec41moa5274mlm.apps.googleusercontent.com'
CLIENT_SECRET = 'kSp8e9w5v1vqQ057DKPDOCYr'

# Check https://developers.google.com/fit/rest/v1/reference/users/dataSources/datasets/get
# for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'

# DATA SOURCE
DATA_SOURCE = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"

# The ID is formatted like: "startTime-endTime" where startTime and endTime are
# 64 bit integers (epoch time with nanoseconds).
# TODAY = datetime.today().date()
NOW = datetime.today()
START = 1527741710291550000
END = int(time.mktime(NOW.timetuple())*1000000000)
DATA_SET = "%s-%s" % (START, END)

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

def retrieve_data():
    """
    Run through the OAuth flow and retrieve credentials.
    Returns a dataset (Users.dataSources.datasets):
    https://developers.google.com/fit/rest/v1/reference/users/dataSources/datasets
    """
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print('Go to the following link in your browser:')
    print(authorize_url)
    code = input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)

    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)

    fitness_service = build('fitness', 'v1', http=http)

    while True:
        dataset = fitness_service.users().dataSources(). \
                  datasets(). \
                  get(userId='me', dataSourceId=DATA_SOURCE, datasetId=DATA_SET). \
                  execute()
                  
        with open('dataset.json', 'w+') as outfile:
            json.dump(dataset, outfile, indent=2)

        starts = []
        ends = []
        values = []
        for point in dataset["point"]:
            if int(point["startTimeNanos"]) > START:
                starts.append(int(point["startTimeNanos"]))
                ends.append(int(point["endTimeNanos"]))
                values.append(point['value'][0]['intVal'])
        print ("From: ", nanoseconds(min(starts)))
        print ("To: ", nanoseconds(max(ends)))
        print ("Steps: %d" % sum(values))

        time.sleep(3600)

def nanoseconds(nanotime):
    """
    Convert epoch time with nanoseconds to human-readable.
    """
    dt = datetime.fromtimestamp(nanotime // 1000000000)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    # Point of entry in execution mode:
        dataset = retrieve_data()
