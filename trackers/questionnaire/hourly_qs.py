import csv
import datetime
import time
import os

def writeToCSV(response):
    with open('responses.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(response)

while True:
    time.sleep(5)
    os.system("osascript -e \'display notification \"Questionnaire Time!\" with title \"Questionnaire Time!\" sound name \"Pop\"\' -e \'activate application \"Terminal\"\'")

    dateTimeNum = datetime.datetime.now().timestamp()
    timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()
    mood = input("Mood 1-5: ")
    moodNotes = input("Mood notes: ")
    trigger = input("Trigger: ")
    activity = input("Activities: ")
    morale = input("Morale 1-5: ")
    stress = input("Stress 1-5: ")
    fatigue = input("Fatigue 1-5: ")
    compulsions = input("Compulsion: ")

    response = []
    response.append(timestamp)
    response.append(mood)
    response.append(moodNotes)
    response.append(trigger)
    response.append(activity)
    response.append(morale)
    response.append(stress)
    response.append(fatigue)
    response.append(compulsions)

    writeToCSV(response)
    print("\nRecorded responses at " + timestamp + "\n")
    time.sleep(3600)
