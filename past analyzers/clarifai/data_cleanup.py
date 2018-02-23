import json

with open('flickr_predictions.json', 'r+') as json_data:
    d = json_data.read()
    json_data.write(json.dumps(d))
