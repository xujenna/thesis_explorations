import csv
import datetime
import time
import os

def writeToCSV(response):
    with open('responses.tsv', 'a') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(response)

while True:
    os.system("osascript -e \'display notification \"Questionnaire Time!\" with title \"Questionnaire Time!\" sound name \"Pop\"\' -e \'activate application \"Terminal\"\'")

    dateTimeNum = datetime.datetime.now().timestamp()
    timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()
    mood = input("Mood 1-5: ")
    moodNotes = input("Mood description: ")
    trigger = input("Trigger: ")
    activity = input("Activities (Schoolwork/In Class/Leisure/Errands/Eating/Cooking/Reading/Resting/Chatting/Email/With Friends/with Kevin/Therapy): ")
    social = input("# of Unique Interactions: ")
    alone = input("Alone (True/False): ")
    location = input("Location: ")
    morale = input("Morale 1-5: ")
    stress = input("Stress 1-5: ")
    fatigue = input("Fatigue 1-5: ")
    compulsions = input("Compulsion (True/False): ")

    response = [timestamp, mood, moodNotes, trigger, activity, social, alone, location, morale, stress, fatigue, compulsions]

    writeToCSV(response)
    print("\nRecorded responses at " + timestamp + "\n")
    time.sleep(3600)
