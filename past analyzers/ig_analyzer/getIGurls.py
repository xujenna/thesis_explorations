# import requests
# from bs4 import BeautifulSoup


# def get_images(user):
#     url = "https://www.instagram.com/" + str(user)
#     source_code = requests.get(url)
#     plain_text = source_code.text
#     soup = BeautifulSoup(plain_text, "html.parser")
#     # print(soup)
#     for image in soup.findAll('img'):
#         href = image.get('src')
#         print(href)
#
# get_images('53964')

# def get_images(user):
#
#     soup = BeautifulSoup(request.urlopen("https://www.instagram.com/"+str(user)),'lxml')
#     for image in soup.findAll('src'):
#         href = image.get('src')
#         print(href)
# get_images('53964')


# access token: 261405032.fe2d6ec.2b58a657a1bf423ab27e1d02dfb57914
# api call: https://api.instagram.com/v1/users/self/media/recent/?access_token=261405032.fe2d6ec.2b58a657a1bf423ab27e1d02dfb57914&max_id=1243644789384054044_261405032

import json
import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.instagram.com/53964/')
soup = BeautifulSoup(r.text, 'lxml')

script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
page_json = script.text.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)
# print(data['entry_data']['ProfilePage'][0]['user']['media'])
count = data['entry_data']['ProfilePage'][0]['user']['media']['count']
nextPage = data['entry_data']['ProfilePage'][0]['user']['media']['page_info']['has_next_page']
end_cursor = data['entry_data']['ProfilePage'][0]['user']['media']['page_info']['end_cursor']
for post in data['entry_data']['ProfilePage'][0]['user']['media']['nodes']:
    image_src = post['thumbnail_resources'][4]['src']
    date = post['date']
    print(image_src)
    print(date)
