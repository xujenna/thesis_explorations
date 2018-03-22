import os
import time

while True:
    os.system("imagesnap -t 10 -w 1 & sleep 3 && killall imagesnap")

    time.sleep(3600)
