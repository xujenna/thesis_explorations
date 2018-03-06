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
    print(efficiency)
    # if efficiency value is less than 50, open xujenna.com/focus
    if efficiency < 50:
        webbrowser.open_new('http://www.xujenna.com/focus')

while True:
    checkProductivity()
    time.sleep(3600)
