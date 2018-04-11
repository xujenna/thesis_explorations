import webbrowser
import time

url = 'http://localhost:8888/index2.html'
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

while True:
    webbrowser.get(chrome_path).open(url)
    time.sleep(3600)

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import time
#
#
# CHROME_PATH = '/Applications/Google Chrome.app'
# CHROMEDRIVER_PATH = '/Users/jxu2/Downloads/chromedriver'
#
# # CHROMEDRIVER_PATH = '/usr/local/Cellar/chromedriver'
# WINDOW_SIZE = "1920,1080"
#
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# # chrome_options.add_argument("--disable-web-security")
# # chrome_options.add_argument("--reduce-security-for-testing")
# # chrome_options.add_argument("--disable-user-media-security")
# # chrome_options.add_experimental_option('prefs',{'profile.default_content_setting_values.notifications':1})
# # chrome_options.add_argument("--enable-kiosk-mode")
# chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# # chrome_options.binary_location = CHROME_PATH
#
# driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
#                           chrome_options=chrome_options
#                          )
# driver.get("http://localhost:8888/index2.html")
# driver.get_screenshot_as_file("capture.png")
# time.sleep(70)
# driver.close()
