from pynput import keyboard
import datetime
import nltk
from nltk.corpus import words
import csv

newKeys = ""
log = []
english = "false"

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
		newKeys = newKeys + " "
		timestamp = datetime.datetime.now().timestamp()
		# newKeys = newKeys + '\n' + datetime.datetime.fromtimestamp(timestamp).isoformat()
		log.append(datetime.datetime.fromtimestamp(timestamp).isoformat() + "," + newKeys)
		print(log)
		newKeys = ""

	elif (str(key) == "Key.esc"):
		with open('logs/log.csv', 'a+') as f:
			for ele in log:
				f.write(ele + '\n')
		tone_analyser()
		log = []

	else:
		print("Key {} pressed.".format(str(key)))



def on_release(key):
	print("Key {} released.".format(key))
	# if str(key) == 'key.esc':
	# 	print("Exiting...")
	# 	return False


def tone_analyser():
	for elem in log:
		if(len(elem.split()) > 2 ):
			for word in elem.split():
				if(word in words.words()):
					english = "true"

	if(english == "true"):
		writethis = []
		writethis.append = filter(lambda row: row[1], log)
		print(writethis)

with keyboard.Listener(
	on_press = on_press,
	on_release = on_release) as listener:
	listener.join()
