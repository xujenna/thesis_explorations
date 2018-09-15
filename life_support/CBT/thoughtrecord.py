import csv
import datetime
import time
# import os
from PIL import Image

def writeToCSV(response):
    with open('thoughtrecord.tsv', 'w+') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(response)

while True:
    # os.system("osascript -e \'display notification \"Stress Log Time!\" with title \"Stress Log Time!\" sound name \"Pop\"\' -e \'activate application \"Terminal\"\'")

    img = Image.open('unnamed.jpg')
    img.show()
    feeling = input("\nHow did you feel?\n")
    situation = input("What was the counterproductive thought?:\n")
    # feeling_intensity = input("\nHow strong was that feeling? (0-5):\n")
    # negative_automatic_thought = input("\nIdentify one negative automatic thought to work on. What thoughts were going through your mind? What memories or images were in your mind?\n")
    evidence = input("\nThat's not true because:\n")
    reframe = input("\nA better way of looking at it is: \n")
    plan = input("\nIf x happens, I will y... \n")
    # alternative_thought = input("\nWrite a new thought which takes into account the evidence for and against the original thought:\n")
    # new_feeling = input("\nHow do you feel about the situation now?\n")
    # new_feeling_intensity = input("\nHow strong is this feeling? (0-5):\n")

    dateTimeNum = datetime.datetime.now().timestamp()
    response = [dateTimeNum, feeling, situation, evidence, reframe, plan]

    writeToCSV(response)
    print("\nRecorded responses at " + timestamp + "\n")