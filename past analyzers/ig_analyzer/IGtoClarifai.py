# open csv
# go to row
# select display_src (row[2])
# send url color model and general model
# write response to json
# write date (row[15])
# write caption (row[6])
# {}


from clarifai.rest import ClarifaiApp
from clarifai.rest import Workflow
from clarifai.rest import Image as ClImage
import csv
import json

app = ClarifaiApp(api_key='e81e6dc3ae354599a65468ac9148d43d')
workflow = Workflow(app.api, workflow_id="colorgeneral")

imgs = []

with open('53964_Instagram.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader,None)
    for row in reader:
        currentImg = {}
        currentImg["date"] = row[15]
        currentImg["display_src"] = row[2]
        currentImg["caption"] = row[6]
        currentImg["likes_count"] = row[9]
        currentImg["comments_count"] = row[4]
        imgs.append(currentImg)

with open('IGtoClarifai.json', 'w') as f:
    f.write("[\n")
    for img in imgs:
        currentImgURL = img["display_src"]
        print("predicting on %s" % currentImgURL)
        currentImg = ClImage(url=currentImgURL)
        response = workflow.predict([currentImg])
        img["general_predictions"] = response["results"][0]["outputs"][0]["data"]["concepts"]
        img["color_predictions"] = response["results"][0]["outputs"][1]["data"]["colors"]
        print(img)
        print("done")
        f.write(json.dumps(img, indent=2) + ",\n")
    f.write("]\n")
