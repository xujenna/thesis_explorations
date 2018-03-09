from pynput import keyboard
import datetime
import nltk
from nltk.corpus import words
import json
from watson_developer_cloud import ToneAnalyzerV3
import time
import threading

newKeys = ""
log = []

tone_analyzer = ToneAnalyzerV3(
  version='2017-09-21',
  username='c7f68599-c38f-4dc3-b429-945fbfbb27cd',
  password='RlUTqGU1coLO'
)


def on_press(key):

	if isinstance(key, keyboard.KeyCode):
		global newKeys
		currentKey = str(key.char)  # force it to be a string
		print("Key {} pressed.".format(currentKey))
		newKeys = newKeys + currentKey

	elif (str(key) == "Key.space"):
		newKeys = newKeys + " "

	elif (str(key) == "Key.enter" and len(newKeys) > 0):
		global log
		english = False
		newKeys = newKeys + " "

		for word in newKeys.split():
			if(word in words.words()):
				english = True

		if(english == True):
			log.append(newKeys)
			english = False

		newKeys = ""

	else:
		print("Key {} pressed.".format(str(key)))



def on_release(key):
	print("Key {} released.".format(key))


def analyser():
	global log
	dateTimeNum = datetime.datetime.now().timestamp()
	timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()

	with open('logs/log.txt', 'w+') as text:
		for elem in log:
			text.write(elem + '. ')

	with open('logs/log.txt') as log_txt:
		tone = tone_analyzer.tone(log_txt.read(), content_type="text/plain;charset=utf-8")
		tone["time"] = timestamp

	with open('logs/log.json', 'r') as f:
		brackets = json.load(f)

	with open('logs/log.json', 'w') as f:
		brackets.append(tone)
		json.dump(brackets, f, indent=2)

	print("analyzed", log)
	log = []


def keylogger():
	with keyboard.Listener(
		on_press = on_press,
		on_release = on_release) as listener:
		listener.join()

def analyser_every_hour():
	while True:
		global log
		time.sleep(3600)
        if (len(log) > 1):
            analyser()
        else:
            time.sleep(3600)

t1 = threading.Thread(target=keylogger)
t2 = threading.Thread(target=analyser_every_hour)
t1.start()
t2.start()
