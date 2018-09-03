import json


with open('merged_file.json', 'r') as f:
	originalFile = json.load(f)


newFile = {}

for dict in originalFile:
	currentKey = dict['time']
	newFile[currentKey] = dict

with open('new_merged_file.json', 'w+') as f:
	json.dump(newFile, f, indent=2, sort_keys=True)