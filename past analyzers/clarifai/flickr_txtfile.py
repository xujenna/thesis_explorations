from clarifai.rest import ClarifaiApp

# Create your API key in your account's `Manage your API keys` page:
# https://clarifai.com/developer/account/keys

app = ClarifaiApp(api_key='edf321bd0be840e88277d6c0a2f66937')


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

with open('flickr_predictions.json','w') as f:

    for set in sets.getchildren()[0]:
        title = set.getchildren()[0].text

        for photo in flickr.walk_set(set.get('id')):
            currentPhotoID = photo.get('id')
            # ElementTree.dump(photo)
            image_url = "http://farm%s.static.flickr.com/%s/%s_%s_m.jpg" % (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
            print("predicting on %s" % image_url)
            response = model.predict_by_url(url=image_url)
            print(response)
            print("done")
            # extras='url_o'
            # currentPhotoSizes = flickr.photos_getSizes(photo_id=currentPhotoID, extras=extras)
            # sourceURL = currentPhotoSizes.get('source')
            # ElementTree.dump(currentPhotoSizes)
            f.write(str(response) + ",\n")




# flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
# extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
# cats = flickr.photosets_getList(text='133005141@N08', per_page=5, extras=extras)
# photos = cats['photos']
# from pprint import pprint
# pprint(photos)