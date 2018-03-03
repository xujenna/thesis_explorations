# laptop

import requests

r = requests.get(url='https://www.rescuetime.com/anapi/data?key=B63X_PtvpSERKQwozOFH_6oXpXwlXTcWh3c3OxfE&perspective=interval&restrict_kind=efficiency&interval=hour&restrict_begin=2018-03-02&restrict_end=2018-03-02&format=json')

print (r.json())

# get updated json from rescue time
