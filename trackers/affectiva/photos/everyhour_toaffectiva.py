import os
import time
import affectiva.api
import glob

username = 'API_USER'
passwd = 'API_PASSWD'
api = affectiva.api.EmotionAPI(username,passwd)


def toAffectiva(latestFile):

    job_url = api.create_job(latestFile)['self']

    job_status = api.query_job(job_url)['status']

    if status == 'done':
        metrics_json = api.results(job_url)

        with open('analyses.json', 'r') as f:
            existingJSON = json.load(f)

        with open('analyses.json', 'w') as f:
            dateTimeNum = datetime.datetime.now().timestamp()
	        timestamp = datetime.datetime.fromtimestamp(dateTimeNum).isoformat()

            metrics_json["time"] = timestamp

            existingJSON.append(metrics_json)

            json.dump(existingJSON, f, indent=2)

            print("analyzed \n", existingJSON)


while True:
    os.system("imagesnap -t 10 -w 1 & sleep 3 && killall imagesnap")

    time.sleep(10)

    fileList = glob.glob('*.jpg')
    latestFile = max(fileList, key=os.path.getctime)

    toAffectiva(latestFile)

    time.sleep(3600)
