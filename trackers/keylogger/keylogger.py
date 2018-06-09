from pynput import keyboard
import datetime
import nltk
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
import json
from watson_developer_cloud import ToneAnalyzerV3
import time
import threading

newKeys = ""
log = []

wordcount = 0
charcount = 0
unique_words = []
onPressTime = 0
prev_onPressTime = 0
onReleaseTime = 0
backspaceCount = 0
dwellTimes = [] # duration of key press
flightTimes = [] # duration between key presses



tone_analyzer = ToneAnalyzerV3(
  version='2017-09-21',
  username='c7f68599-c38f-4dc3-b429-945fbfbb27cd',
  password='RlUTqGU1coLO'
)


def on_press(key):
	global prev_onPressTime
	global dwellTimes
	global flightTimes
	global onPressTime
	global backspaceCount
	currentFlightTime = 0

	onPressTime = datetime.datetime.now().timestamp()

	if(prev_onPressTime > 0):
		currentFlightTime = onPressTime - prev_onPressTime
		if(currentFlightTime < 2):
			flightTimes.append(currentFlightTime)


	if isinstance(key, keyboard.KeyCode):
		global newKeys
		global wordcount
		global charcount
		global unique_words

		currentKey = str(key.char)  # force it to be a string
		print("Key {} pressed at {}.".format(currentKey, onPressTime))
		newKeys = newKeys + currentKey
		prev_onPressTime = onPressTime

	elif (str(key) == "Key.space"):
		newKeys = newKeys + " "
		prev_onPressTime = onPressTime

	elif (str(key) == "Key.backspace"):
		newKeys = newKeys[:-1]
		backspaceCount += 1
		prev_onPressTime = onPressTime

	elif (str(key) == "Key.enter" and len(newKeys) > 0):
		global log
		# english = False
		# newKeys = newKeys + " "

		sentence = newKeys

		for letter in sentence:
			if not letter.isalpha() and letter != " ":
				sentence = sentence.replace(letter, "")

		tokens = nltk.word_tokenize(sentence)
		tags = nltk.pos_tag(tokens)
		current_wordcount = 0

		for tag in tags:
			wordnet_lemmatizer = WordNetLemmatizer()
			if tag[1].startswith('V'):
				word = wordnet_lemmatizer.lemmatize(tag[0], pos='v')
			else:
				word = wordnet_lemmatizer.lemmatize(tag[0])
			# print("lemmatized word", word)

			if(word in words.words()):
				# print("real word", word)
				current_wordcount += 1
				wordcount += 1
				charcount += len(word)

				if not(word in unique_words):
					unique_words.append(word)

		# print("wordcount", wordcount)
		if(current_wordcount > 1):
			if newKeys.endswith("/"):
				newKeys = newKeys[:-1]
				newKeys = newKeys + "?"
			log.append(newKeys)

			print(log)
			print("current char count: ", charcount)
			print("current word count: ", wordcount)
			print("current unique word count: ", len(unique_words))
			if(len(flightTimes) > 0):
				print("current avg flight time: ", sum(flightTimes) / len(flightTimes))
			print("current avg dwell time: ", sum(dwellTimes) / len(dwellTimes))
			print("backspace count: ", backspaceCount)

			current_wordcount = 0
			prev_onPressTime = 0

		newKeys = ""

	else:
		print("Key {} pressed.".format(str(key)))



def on_release(key):
	global onPressTime
	onReleaseTime = datetime.datetime.now().timestamp()
	currentDwellTime = onReleaseTime - onPressTime
	dwellTimes.append(currentDwellTime)

	print("Key {} released at {}.".format(key,onReleaseTime))



def analyser():
	global log
	global dwellTimes
	global flightTimes
	global wordcount
	global charcount
	global unique_words
	global backspaceCount

	dateTimeNum = datetime.datetime.now().timestamp()
	timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()

	with open('logs/log.txt', 'w+') as text:
		for elem in log:
			text.write(elem + '. ')

	with open('logs/log.txt') as log_txt:
		tone = tone_analyzer.tone(log_txt.read(), content_type="text/plain;charset=utf-8")
		tone["time"] = timestamp
		tone["word_count"] = wordcount
		tone["uniqueword_count"] = len(unique_words)
		tone["char_count"] = charcount
		tone["backspace_count"] = backspaceCount
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
	print("backspace count: ", backspaceCount)
	print("Average Dwell Time: ", sum(dwellTimes) / len(dwellTimes))
	print("Average Flight Time: ", sum(flightTimes) / len(flightTimes))

	log = []
	dwellTimes = []
	flightTimes = []
	wordcount = 0
	unique_words = []
	charcount = 0
	backspaceCount = 0

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
