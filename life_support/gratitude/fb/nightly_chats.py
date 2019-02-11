import os
import time
import datetime
import schedule
import json
import threading
import appscript
import random

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


def getGratitude():
    while True:
        entry = input("I'm grateful for ")

        if entry == "done":
            return

        dateTimeNum = datetime.datetime.now().timestamp()
        # timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()
        date = datetime.datetime.fromtimestamp(dateTimeNum).date().isoformat()

        response = {}
        response['date'] = date
        response['gratitude_entries'] = []
        response['gratitude_entries'].append({
            'timestamp': dateTimeNum,
            'entry': entry
            })

        writeToJSON(response)


def job():
    os.system("osascript -e \'display notification \"Gratitude Time!\" with title \"Gratitude Time!\" sound name \"Pop\"\' -e \'activate application \"Terminal\"\'")

    with open('gratitude.json', 'r') as infile:
        try: 
            gratitude_log = json.load(infile)
        except ValueError:
            print("nothing in gratitude log")

    dateTimeNum = datetime.datetime.now().timestamp()
    date = datetime.datetime.fromtimestamp(dateTimeNum).date().isoformat()

    if gratitude_log[-1]['date'] == date:
        todaysGratitude = gratitude_log[-1]['gratitude_entries']
        gratitudeList = list(map(lambda x: x['entry'], todaysGratitude))
    else:
        getGratitude()
        with open('gratitude.json', 'r') as infile:
            try: 
                gratitude_log = json.load(infile)
                todaysGratitude = gratitude_log[-1]['gratitude_entries']
                gratitudeList = list(map(lambda x: x['entry'], todaysGratitude))

            except ValueError:
                print("nothing in gratitude log")

    print(gratitudeList)

    contacts = ["Barak Chamo", "Chian Huang", "Michelle Maeng", "Gunvor B. G. Dreijer", "Anna Clements", "Sam Chasan", "Kellee Massey", "Alexandra Lopez", "Asha Veeraswamy", "Isabella Cruz-Chong", "Junie Lee", "Katya Rozanova", "Max Horwich", "Ridwan Madon", "Kemi Sijuwade-Ukadike", "Dan Shin", "Kathy Wu", "Jasmyne Robertson", "Kenzo Nakamura", "Lin Zhang", "Susan Churchfield", "Liz Wallace", "Helen Tang", "Rushali Paratey", "Nick Wallace", "Zohreh Zadbood", "Carrie Sijia Wang", "Akmyrat Tuyliyev", "Alejandro Nicolás Sanín Ordoñez", "Luigi Menduni", "Sandy Hsieh", "Christina Coclanes", "Json Yung", "Mary Notari"]

    # name = contacts[random.randint(0,len(contacts))]
    name = "Barak Chamo"

    intro = "Hey " + name + "! I\'m Jenna\'s thesis assistant, contacting you to see if you\'d like to share a gratitude practice with her today. It\'s super simple: you\'ll just exchange a brief list of good things that happened in each of your days. If you\'re game, simply respond to this message. If not, just ignore this message. Thanks!"
    
    appscript.app('Terminal').do_script("cd /Users/jxu2/github/thesis_explorations/life_support/gratitude/fb/ && messer --command='m \"" + name + "\" " + intro + "' ")

schedule.every().day.at("22:30").do(job)


def runScheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


t1 = threading.Thread(target=getGratitude)
t2 = threading.Thread(target=runScheduler)
t1.start()
t2.start()