import os
import csv

# while True:
os.system("cp ~/Library/Application\ Support/Google/Chrome/Default/History data")
os.system("sqlite3 data/History < get_chrome_history.sql")


with open('data/my-chrome-output.csv', newline='') as f:
    reader = csv.reader(f)
    next(reader,None)
    data = [line for line in reader]
with open('data/my-chrome-output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["time", "url"])
    writer.writerows(filter(lambda row: row[0] > "2018-03-01 00:00:00", data))


# time.sleep(3600)
