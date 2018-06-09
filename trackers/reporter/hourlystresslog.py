import csv
import datetime
import time
import os

def writeToCSV(response):
    with open('stresslog_responses.tsv', 'a') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(response)

while True:
    os.system("osascript -e \'display notification \"Stress Log Time!\" with title \"Stress Log Time!\" sound name \"Pop\"\' -e \'activate application \"Terminal\"\'")


    depletion = input("Depletion: ")
    concentration = input("Concentration: ")
    forgetfulness = input("Forgetfulness: ")
    sociallyAvoidant = input("Feeling socially avoidant: ")
    pessimism = input("Pessimism: ")
    cynicism = input("Cynicism: ")
    apathy = input("Apathy: ")
    engagement = input("Engagement: ")
    energy = input("Energy: ")

    dateTimeNum = datetime.datetime.now().timestamp()
    timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()
    response = [timestamp, depletion, concentration, forgetfulness, sociallyAvoidant, pessimism, cynicism, apathy, engagement, energy]

    writeToCSV(response)
    print("\nRecorded responses at " + timestamp + "\n")
    time.sleep(3600)