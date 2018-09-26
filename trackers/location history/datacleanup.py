import json


data = []


with open("Location_History.json", "r") as f:
	raw = json.load(f)
	raw_locations = raw['locations']



	for obj in raw_locations:
		if (int(obj['timestampMs']) >= 1524628800):
			holder = {}
			holder['time'] = int(obj['timestampMs'])
			holder['coordinates'] = [(obj['longitudeE7'] * 0.0000001),(obj['latitudeE7'] * 0.0000001)]
			data.append(holder)
			holder = {}

with open("LocationHistory_cleaned.json", "w+") as f:
	json.dump(data, f)

