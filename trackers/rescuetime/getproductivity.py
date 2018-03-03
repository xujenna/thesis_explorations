import requests
import json

# get updated json from rescue time
r = requests.get(url='https://www.rescuetime.com/anapi/data?key=B63X_PtvpSERKQwozOFH_6oXpXwlXTcWh3c3OxfE&perspective=interval&restrict_kind=efficiency&interval=hour&restrict_begin=2018-02-15&restrict_end=2018-03-02&format=json')

data = r.json()

#save json to file
with open('productivity.json', 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)

rows = data['rows']

efficiency = rows[-1][4]

print(efficiency)
# isolate "Efficiency (percent)" value of last array: rows > index number (by hour) > 4
# if efficiency value is less than 50, open xujenna.com/focus
