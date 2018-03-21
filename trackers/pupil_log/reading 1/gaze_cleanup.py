import csv

with open('gaze_positions.csv') as f:
    reader = csv.reader(f)
    data = [line for line in reader]
with open('gaze_cleanup.csv', 'w+') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow([row[6], row[7]])
