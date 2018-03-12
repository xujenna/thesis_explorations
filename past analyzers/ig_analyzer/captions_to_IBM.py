import json
from watson_developer_cloud import ToneAnalyzerV3


tone_analyzer = ToneAnalyzerV3(
  version='2017-09-21',
  username='c7f68599-c38f-4dc3-b429-945fbfbb27cd',
  password='RlUTqGU1coLO'
)



captions = [];
with open('ig_to_clarifai.json', 'r') as IGjson:
    clarifaiData = json.load(IGjson)
    for elem in clarifaiData:
        currentCaption = elem["caption"]
        currentDate = elem["date"]
        holder = {}
        tone = tone_analyzer.tone(currentCaption, content_type="text/plain;charset=utf-8")
        holder["date"] = currentDate
        holder["tones"] = tone["sentences_tone"]
        captions.append(holder)
        break

with open('captionsToIBM.json', 'w+') as f:
	json.dump(captions, f, indent=2)
