import json


with open('log_new_copy.json', 'r') as f:
	keyloggerData = json.load(f)


with open('newlog.json', 'w+') as f:
	for x in range(0, len(keyloggerData)):
		try:
			uniquewords = keyloggerData[x]['uniqueword_count']
			words = keyloggerData[x]['word_count']
			keyloggerData[x]['uniqueword_ratio'] = uniquewords / words
		except:
			continue

	json.dump(keyloggerData, f, indent=2)