import csv
import datetime
import time
# import os
from PIL import Image

def writeToCSV(response):
    with open('thoughtrecord.tsv', 'a') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(response)

while True:
    # os.system("osascript -e \'display notification \"Stress Log Time!\" with title \"Stress Log Time!\" sound name \"Pop\"\' -e \'activate application \"Terminal\"\'")

    situation = input("Describe what happened (who, what, when, where?):\n")
    img = Image.open('unnamed.jpg')
    img.show()
    feeling = input("\nHow did you feel?\n")
    feeling_intensity = input("\nHow strong was that feeling? (0-5):\n")
    negative_automatic_thought = input("\nIdentify one negative automatic thought to work on. What thoughts were going through your mind? What memories or images were in your mind?\n")
    negative_evidence = input("\nWhat facts support the truthfulness of this thought?\n")
    contrary_evidence = input("\nWhat evidence/experiences indicate that this thought is not completely true all of the time? Are there any that contradict this thought? What are alternate explanations?\n")
    alternative_thought = input("\nWrite a new thought which takes into account the evidence for and against the original thought:\n")
    new_feeling = input("\nHow do you feel about the situation now?\n")
    new_feeling_intensity = input("\nHow strong is this feeling? (0-5):\n")

    dateTimeNum = datetime.datetime.now().timestamp()
    timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()
    response = [timestamp, situation, feeling, feeling_intensity, negative_automatic_thought, negative_evidence, contrary_evidence, alternative_thought, new_feeling, new_feeling_intensity]

    writeToCSV(response)
    print("\nRecorded responses at " + timestamp + "\n")