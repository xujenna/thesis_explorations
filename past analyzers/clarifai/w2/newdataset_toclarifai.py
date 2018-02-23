from clarifai.rest import ClarifaiApp

# Create your API key in your account's `Manage your API keys` page:
# https://clarifai.com/developer/account/keys

app = ClarifaiApp(api_key='b320b70b79384f1db5011f7db371628e')


# get the general model
model = app.models.get("general-v1.3")



import flickrapi
import os
from xml.etree import ElementTree

api_key = '969e8cec0920f61dd8c1822ad9bbd5a3'
api_secret = 'ccb73d787ecbe071'

flickr = flickrapi.FlickrAPI(api_key, api_secret)

flickr.authenticate_via_browser('write')


sets = flickr.photosets_getList(user_id='133005141@N08')
#sets = flickr.people_getPublicPhotos(user_id='133005141@N08')

# ElementTree.dump(sets)

import newphotos
from newphotos import *
import json

# print("dataset2", dataset2)

# allPhotos = []
# datetimes = []
# dataset = []



# for set in sets.getchildren()[0]:
#     for photo in flickr.walk_set(set.get('id')):
#         id = photo.get('id')
#         secret = photo.get('secret')

#         # get datetime
#         exif_xml = flickr.photos_getExif(photo_id=id)
#         exifs = list(exif_xml)[0]
#         for exif in exifs:
#             if exif.get('tag') == 'DateTimeOriginal':
#                 # ElementTree.dump(list(exif)[0])
#                 datetimes.append(exif.find('raw').text)

#         # get url
#         image_url = "http://farm%s.static.flickr.com/%s/%s_%s_m.jpg" % (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
#         allPhotos.append(image_url)
#         print(image_url)        

#     dataset = zip(datetimes,allPhotos)

# sorted(dataset, key=getKey)

# print(dataset)

with open('flickr_dataset2_predictions.json', 'w') as f:
    for x in dataset2:
        print("predicting on %s" % x)
        response = model.predict_by_url(url=x)
        print(json.dumps(response))
        print("done")
        f.write(json.dumps(response) + ",\n")