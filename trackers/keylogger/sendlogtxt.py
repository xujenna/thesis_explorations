from pynput import keyboard
import datetime
import nltk
from nltk.corpus import words
import json
from watson_developer_cloud import ToneAnalyzerV3
import time
import threading


tone_analyzer = ToneAnalyzerV3(
  version='2017-09-21',
  username='c7f68599-c38f-4dc3-b429-945fbfbb27cd',
  password='RlUTqGU1coLO'
)


dateTimeNum = datetime.datetime.now().timestamp()
timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()

with open('logs/log.txt') as log_txt:
	tone = tone_analyzer.tone(log_txt.read(), content_type="text/plain;charset=utf-8")
	tone["time"] = timestamp

with open('logs/log_new.json', 'r') as f:
	brackets = json.load(f)

with open('logs/log_new.json', 'w') as f:
	brackets.append(tone)
	json.dump(brackets, f, indent=2)

print("analyzed")
