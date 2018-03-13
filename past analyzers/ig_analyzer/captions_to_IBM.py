import json
from watson_developer_cloud import ToneAnalyzerV3


tone_analyzer = ToneAnalyzerV3(
  version='2017-09-21',
  username='c7f68599-c38f-4dc3-b429-945fbfbb27cd',
  password='RlUTqGU1coLO'
)


with open('captionsToIBM.json', 'w+') as f:
    f.write("[\n")

captions = [];
with open('ig_to_clarifai.json', 'r') as IGjson:
    clarifaiData = json.load(IGjson)
    for elem in clarifaiData:
        if(len(elem["caption"]) > 0):
            currentCaption = elem["caption"]
            currentDate = elem["date"]
            holder = {}
            tone = tone_analyzer.tone(currentCaption, content_type="text/plain;charset=utf-8")
            if isinstance(tone, dict) and "sentences_tone" in tone:
                holder["date"] = currentDate
                holder["tones"] = tone["sentences_tone"]
                captions.append(holder)
                print(captions)
                with open('captionsToIBM.json', 'a') as f:
                    f.write(json.dumps(captions, indent=2) + ",\n")

with open('captionsToIBM.json', 'a') as f:
    f.write("]\n")

# with open('captionsToIBM.json', 'w+') as f:
# 	json.dump(captions, f, indent=2)
