import csv

with open('pupil_positions.csv') as f:
    reader = csv.reader(f)
    data = [line for line in reader]
with open('pupil_cleanup.csv', 'w+') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow([row[13]])
