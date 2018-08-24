import requests
import json
import webbrowser
import time
import datetime


def checkProductivity():
    dt = datetime.datetime.now()
    currentDate = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
    url = "https://www.rescuetime.com/anapi/data?key=B63X_PtvpSERKQwozOFH_6oXpXwlXTcWh3c3OxfE&perspective=interval&restrict_kind=efficiency&interval=hour&restrict_begin=" + currentDate + "&restrict_end=" + currentDate + "&format=json"
    
    # get updated json from rescue time

    success = False
    global r
    global data

    while success is False:
        try:
            r = requests.get(url=url)
            data = r.json()
            success = True
        except Exception as e:
            print("Error:")
            print(e)
            time.sleep(10)
            print("retrying...")

    #save json to file

    newData = data['rows'][-1]
    print(newData)

    with open('productivity.json', 'r') as f:
        allData = json.load(f)

    with open('productivity.json', 'w') as f:
        allData['rows'].append(newData)
        json.dump(allData, f, indent=4, sort_keys=True)

    # isolate "Efficiency (percent)" value of last array: rows > index number (by hour) > 4
    rows = data['rows']
    efficiency = rows[-1][4]
    print("efficiency score:", efficiency)


def getChromeActivity():
    url = "https://tabcounter-3aab1.firebaseio.com/users/xujenna/metrics.json"
    r = requests.get(url=url)

    chromeData = r.json()

    with open('chromeactivity.json', 'w+') as f:
        json.dump(chromeData, f, indent=4, sort_keys=True)

    lastTime = list(chromeData.keys())[-1]
    print("tabs created: ", chromeData[lastTime]['tabs_created'])
    print("tabs activated: ", chromeData[lastTime]['tabs_activated'])


while True:
    checkProductivity()
    getChromeActivity()
    time.sleep(3600)
