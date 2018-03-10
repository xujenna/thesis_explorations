import urllib.request
import json
from bs4 import BeautifulSoup
import csv
import time
import datetime

page_url = "https://www.ins2tagram.com/53964/"

def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)
            print("Error fur URL {}: {}".format(url, datetime.datetime.now()))
            print("retrying.")
    return response.read().decode('utf-8')

def get_more_posts(page_url, end_cursor):
    url = page_url + '?max_id=' + end_cursor
    page_source = request_until_succeed(url)
    page = BeautifulSoup(page_source)
    scripts = page.find_all('script')
    for script in scripts:
        if script.text[:18] == "window._sharedData":
            break
    json_data = json.loads(script.contents[0][21:-1])
    return json_data

def process_post(json_data):
    owner_id = json_data['owner']['id']
    post_id = json_data['id']
    display_src = json_data['display_src']
    media_preview = json_data['media_preview']
    comments_count = json_data['comments']['count']
    gating_info = json_data['gating_info']
    caption = ''
    try:
        caption = json_data['caption']
    except:
        pass
    thumbnail_src = json_data['thumbnail_src']
    comments_disabled = json_data['comments_disabled']
    likes_count = json_data['likes']['count']
    is_video = json_data['is_video']
    dimensions = json_data['dimensions']
    typename = json_data['__typename']
    code = json_data['code']
    link = 'https://www.instagram.com/p/' + code
    video_views = ''
    try:
        video_views = json_data['video_views']
    except:
        pass
    date = json_data['date']
    date = str(datetime.datetime.utcfromtimestamp(date).year)+'-'+str(datetime.datetime.utcfromtimestamp(date).month)+'-'+str(datetime.datetime.utcfromtimestamp(date).day)+' '+str(datetime.datetime.utcfromtimestamp(date).hour)+':'+str(datetime.datetime.utcfromtimestamp(date).minute)+':'+str(datetime.datetime.utcfromtimestamp(date).second)
    date = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    date = date + datetime.timedelta(hours=-5) #EST
    return(owner_id, post_id, display_src, media_preview, comments_count, gating_info, caption, thumbnail_src, comments_disabled, likes_count, is_video, dimensions, typename, link, video_views, date)

def scrape_instagram(page_url):
    scrape_starttime = datetime.datetime.now()
    page_source = request_until_succeed(page_url)
    page = BeautifulSoup(page_source)
    scripts = page.find_all('script')
    for script in scripts:
        if script.text[:18] == "window._sharedData":
            break
    json_data = json.loads(script.contents[0][21:-1])
    has_next_page = True
    num_posts = json_data['entry_data']['ProfilePage'][0]['user']['media']['count']
    username = json_data['entry_data']['ProfilePage'][0]['user']['username']
    num_processed = 0
    print("Scraping {}'s {} Instagram Posts: {}\n".format(username, num_posts, scrape_starttime))
    with open('C:\\Users\\xhargrav\\Desktop\\{}_Instagram.csv'.format(username),'w', newline='', encoding='utf-8') as file:
        csv.writer(file).writerow(["owner_id", "post_id", "display_src", \
            "media_preview", "comments_count", "gating_info", "caption", \
            "thumbnail_src", "comments_disabled", "likes_count", "is_video", \
            "dimensions", "typename", "code", "video_views", "date"])
        while has_next_page:
            for i in range(0,len(json_data['entry_data']['ProfilePage'][0]['user']['media']['nodes'])):
                post_to_process = json_data['entry_data']['ProfilePage'][0]['user']['media']['nodes'][i]
                csv.writer(file).writerow(process_post(post_to_process))
                num_processed += 1
                if num_processed % 100 == 0:
                    print("{} Statuses Processed: {}".format(num_processed, datetime.datetime.now()))
            has_next_page = json_data['entry_data']['ProfilePage'][0]['user']['media']['page_info']['has_next_page']
            if has_next_page == True:
                end_cursor = json_data['entry_data']['ProfilePage'][0]['user']['media']['page_info']['end_cursor']
                json_data = get_more_posts(page_url, end_cursor)
            else:
                has_next_page = False
    file.close()
    print("Done! {} posts processed in {}".format(num_processed, datetime.datetime.now() - scrape_starttime))

scrape_instagram(page_url)
