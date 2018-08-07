import csv
import datetime
import time
import os
import json


def writeToJSON(response):
    with open('gratitude.json', 'r') as infile:
        try:
            gratitude_log = json.load(infile)
        except ValueError:
            gratitude_log = []


        if len(gratitude_log) > 0 and response['date'] == gratitude_log[-1]['date']:
            gratitude_log[-1]['gratitude_entries'].append(response['gratitude_entries'][0])

            with open('gratitude.json', 'w') as outfile:
                json.dump(gratitude_log, outfile, indent=2)

            print("Appended entry to today's log")

        else:
            gratitude_log.append(response)

            with open('gratitude.json', 'w') as outfile:
                json.dump(gratitude_log, outfile, indent=2)

            print("Added new log for today")


while True:

    entry = input("I'm grateful for ")

    dateTimeNum = datetime.datetime.now().timestamp()
    timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()
    date = datetime.datetime.fromtimestamp(dateTimeNum).date().isoformat()

    response = {}
    response['date'] = date
    response['gratitude_entries'] = []
    response['gratitude_entries'].append({
        'timestamp': timestamp,
        'entry': entry
        })

    writeToJSON(response)
