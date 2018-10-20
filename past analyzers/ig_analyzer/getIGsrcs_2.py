import urllib.request
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver

import csv
import time
import datetime
from http.client import IncompleteRead

page_url = "https://www.instagram.com/53964/"



def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try:
            time.sleep(5)
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)
            print("Error fur URL {}: {}".format(url, datetime.datetime.now()))
            print("retrying.")
        except IncompleteRead:
            time.sleep(5)
             # Oh well, reconnect and keep trucking
            continue
        # except SocketError as e:
        #     errorcode = e[0]
        #     time.sleep(5)
        #     if errorcode!=errno.ECONNREFUSED:
        #         print("There is a time-out")
        #         # Not the error we are looking for, re-raise
        #         raise e

    return response.read().decode('utf-8')

# def get_more_posts(page_url, end_cursor, my_id):
#     # url = "https://instagram.com/graphql/query/?query_id=17888483320059182&id=" + my_id + "&first=12&after=" + end_cursor
#     # print("url")
#     # print(url)

#     # page_source = request_until_succeed(url)

#     # I used Firefox; you can use whichever browser you like.
#     browser = webdriver.Firefox()

#     # Tell Selenium to get the URL you're interested in.
#     browser.get(page_url)

#     # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
#     lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#         match=False
#             while(match==False):
#                     lastCount = lenOfPage
#                     time.sleep(3)
#                     lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#                     if lastCount==lenOfPage:
#                         match=True

#     # Now that the page is fully scrolled, grab the source code.
#     source_data = browser.page_source

#     # Throw your source into BeautifulSoup and start parsing!
#     page = bs(source_data)


#     # page = BeautifulSoup(page_source,"lxml")
#     scripts = page.find_all('script')
#     for script in scripts:
#         if script.text[:18] == "window._sharedData":
#             break
#     json_data = json.loads(script.contents[0][21:-1])
#     return json_data

def process_post(json_data):
    owner_id = json_data['node']['owner']['id']
    post_id = json_data['node']['id']
    display_src = json_data['node']['display_url']
    media_preview = json_data['node']['media_preview']
    comments_count = json_data['node']['edge_media_to_comment']['count']
    gating_info = json_data['node']['gating_info']
    caption = ''
    try:
        caption = json_data['node']['edge_media_to_caption']['edges']['node']['text']
    except:
        pass
    thumbnail_src = json_data['node']['thumbnail_src']
    comments_disabled = json_data['node']['comments_disabled']
    likes_count = json_data['node']['edge_media_preview_like']['count']
    is_video = json_data['node']['is_video']
    dimensions = json_data['node']['dimensions']
    typename = json_data['node']['__typename']
    code = json_data['node']['shortcode']
    link = 'https://www.instagram.com/p/' + code
    video_views = ''
    try:
        video_views = json_data['node']['video_views']
    except:
        pass
    date = json_data['node']['taken_at_timestamp']
    date = str(datetime.datetime.utcfromtimestamp(date).year)+'-'+str(datetime.datetime.utcfromtimestamp(date).month)+'-'+str(datetime.datetime.utcfromtimestamp(date).day)+' '+str(datetime.datetime.utcfromtimestamp(date).hour)+':'+str(datetime.datetime.utcfromtimestamp(date).minute)+':'+str(datetime.datetime.utcfromtimestamp(date).second)
    date = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    date = date + datetime.timedelta(hours=-5) #EST
    return(owner_id, post_id, display_src, media_preview, comments_count, gating_info, caption, thumbnail_src, comments_disabled, likes_count, is_video, dimensions, typename, link, video_views, date)

def scrape_instagram(page_url):

    scrape_starttime = datetime.datetime.now()

    # I used Firefox; you can use whichever browser you like.
    browser = webdriver.Firefox()

    # Tell Selenium to get the URL you're interested in.
    browser.get(page_url)

    # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True

    # Now that the page is fully scrolled, grab the source code.
    source_data = browser.page_source
    print("source_data")
    print(source_data)
    # Throw your source into BeautifulSoup and start parsing!
    page = bs(source_data, "lxml")

    imgs = page.find_all('img')

    all_posts = []
    for img in imgs:
        newImg = {}
        

    print("script")
    print(script)

    # has_next_page = True
    # num_posts = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count']
    # username = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['username']
    # num_processed = 0
    # print("Scraping {}'s {} Instagram Posts: {}\n".format(username, num_posts, scrape_starttime))
    # with open('{}_Instagram.csv'.format(username),'w', newline='', encoding='utf-8') as file:
    #     csv.writer(file).writerow(["owner_id", "post_id", "display_src", \
    #         "media_preview", "comments_count", "gating_info", "caption", \
    #         "thumbnail_src", "comments_disabled", "likes_count", "is_video", \
    #         "dimensions", "typename", "code", "video_views", "date"])
    #     while has_next_page:
    #         for i in range(0,len(json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'])):
    #             post_to_process = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]
    #             csv.writer(file).writerow(process_post(post_to_process))
    #             num_processed += 1
    #             if num_processed % 100 == 0:
    #                 print("{} Statuses Processed: {}".format(num_processed, datetime.datetime.now()))
    #         has_next_page = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
    #         if has_next_page == True:
    #             end_cursor = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    #             my_id = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['id']
    #             json_data = get_more_posts(page_url, end_cursor, my_id)

    #         else:
    #             has_next_page = False
    # file.close()
    # print("Done! {} posts processed in {}".format(num_processed, datetime.datetime.now() - scrape_starttime))

scrape_instagram(page_url)
