import requests
import json
import webbrowser
import time
import datetime


def checkProductivity():
    dt = datetime.datetime.now()
    currentDate = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
    url = "https://www.rescuetime.com/anapi/data?key=B63X_PtvpSERKQwozOFH_6oXpXwlXTcWh3c3OxfE&perspective=interval&restrict_kind=efficiency&interval=hour&restrict_begin=2018-03-01&restrict_end=" + currentDate + "&format=json"
    # get updated json from rescue time
    r = requests.get(url=url)

    data = r.json()

    #save json to file
    with open('productivity.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

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
