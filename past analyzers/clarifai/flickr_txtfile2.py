import os

import flickr_api as flickr

# If all you want to do is get public information,
# then you need to set the api key and secret

flickr.set_keys(api_key='969e8cec0920f61dd8c1822ad9bbd5a3', api_secret='ccb73d787ecbe071')

# If you want to fetch private/hidden information
# then in addition to the api key and secret,
# you also need to authorize your application.

# To do that, we request the authorization URL
# to get the value of `oauth_verifier`, which
# is what we need.

# This step is done only once, and we save
# the token. So naturally, we first check
# if the token exists or not:

if os.path.isfile('token.key'):
    flickr.set_auth_handler('token.key')
else:
    # This is the first time we are running,
    # so get the token and save it
    auth = flickr.auth.AuthHandler()
    url = auth.get_authorization_url('read')  # Get read permissions
    session_key = raw_input('''
                 Please visit {} and then copy the value of oauth_verifier:'''.format(url))

    if len(session_key.strip()):
        auth.set_verifier(session_key.strip())
        flickr.set_auth_handler(auth)

        # Save this token for next time
        auth.save('token.key')
    else:
        raise Exception("No authorization token provided, quitting.")

# If we reached this point, we are good to go!
# First thing we want to do is enable the cache, so
# we don't hit the API when not needed

flickr.enable_cache()

# Fetching a user, by their username

user = flickr.Person.findByUserName('username')

# Or, we don't know the username:

user = flickr.Person.findByEmail('some@user.com')

# Or, if we want to use the authenticated user

user = flickr.test.login()

# Next, fetch the photosets and their corresponding photos:

photo_sets = user.getPhotosets()
for pset in photo_sets:
    print("Getting pictures for {}".format(pset.title))
    photos = pset.getPhotos()
    for photo in photos:
        print('{}'.format(photo.info.title))

# Or, just get me _all_ the photos:

photos = user.getPhotos()

# If you haven't logged in,
# photos = user.getPublicPhotos()

for photo in photos:
    print('{}'.format(photo.info.title))