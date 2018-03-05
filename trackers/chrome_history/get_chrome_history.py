import os

os.system("cp ~/Library/Application\ Support/Google/Chrome/Default/History data")
os.system("sqlite3 data/History < get_chrome_history.sql")
