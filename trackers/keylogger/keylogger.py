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

onPressTime = 0
prev_onPressTime = 0
onReleaseTime = 0
dwellTimes = [] # duration of key press
flightTimes = [] # duration between key presses

tone_analyzer = ToneAnalyzerV3(
  version='2017-09-21',
  username='c7f68599-c38f-4dc3-b429-945fbfbb27cd',
  password='RlUTqGU1coLO'
)


def on_press(key):

	onPressTime = datetime.datetime.now().timestamp()
	currentFlightTime = onPressTime - prev_onPressTime
	flightTimes.append(currentFlightTime)

	if isinstance(key, keyboard.KeyCode):
		global newKeys
		currentKey = str(key.char)  # force it to be a string
		print("Key {} pressed at {}.".format(currentKey, onPressTime))
		newKeys = newKeys + currentKey

	elif (str(key) == "Key.space"):
		newKeys = newKeys + " "

	elif (str(key) == "Key.backspace"):
		newKeys = newKeys[:-1]

	elif (str(key) == "Key.enter" and len(newKeys) > 0):
		global log
		# english = False
		newKeys = newKeys + " "

		wordcount = 0
		for word in newKeys.split():
			if(word in words.words()):
				wordcount += 1;

		if(wordcount > 2):
			log.append(newKeys)
			print(log)
			wordcount = 0

		newKeys = ""

		prev_onPressTime = onPressTime

	else:
		print("Key {} pressed.".format(str(key)))



def on_release(key):
	onReleaseTime = datetime.datetime.now().timestamp()
	currentDwellTime = onReleaseTime - onPressTime
	dwellTimes.append(currentDwellTime)

	print("Key {} released at {}.".format(key,onReleaseTime))


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

		wordcount = 0
		unique_words = []
		charcount = 0
		for sentence in log:
			for word in sentence.split():
				if(word in words.words()):
					wordcount += 1;
					charcount += len(word)

					if not(word in unique_words):
						unique_words.append(word)

		tone["word_count"] = wordcount
		tone["uniqueword_count"] = len(unique_words)
		tone["char_count"] = charcount
		tone["avg_dwelltime"] = sum(dwellTimes) / len(dwellTimes)
		tone["avg_flighttime"] = sum(flightTimes) / len(flightTimes)


	with open('logs/log_new.json', 'r') as f:
		brackets = json.load(f)

	with open('logs/log_new.json', 'w') as f:
		brackets.append(tone)
		json.dump(brackets, f, indent=2)

	print("analyzed", log)
	print("Word Count: ", wordcount)
	print("Unique Word Count: ", len(unique_words))
	print("Character Count: ", charcount)
	print("Average Dwell Time: ", sum(dwellTimes) / len(dwellTimes))
	print("Average Flight Time: ", sum(flightTimes) / len(flightTimes))
	log = []
	dwellTimes = []
	flightTimes = []

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
