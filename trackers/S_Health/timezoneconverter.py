import dateutil.parser
import datetime
import pytz
from pytz import timezone
import csv

NYtz = timezone('America/New_York')
CHItz = timezone('America/Chicago')
LAtz = timezone('America/Los_Angeles')
COtz = timezone('America/Denver')
epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.UTC)


with open('com.samsung.health.exercise.201808301232.csv', newline='') as f:
	reader = csv.reader(f, delimiter=',')
	# writer = csv.writer(f, delimiter='\t')
	header = next(reader)
	newHeader = [header[3], header[8], header[18], header[20], header[34]]
	new_rows = []

	for row in reader:

		if ((row[18] > '2018-05-11 18:00:00.000' and row[18] < '2018-05-16 20:00:00.000') or (row[18] > '2018-08-06T18:20:00.000000' and row[18] < '2018-08-13T15:10:00.000000')):
			newStr = row[18].replace(" ", "T")
			parsedDate = dateutil.parser.parse(newStr)
			withTimeZone = CHItz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()

			newRow = [row[3], row[8], newTimestamp, row[20], row[34]]
			new_rows.append(newRow)

		elif (row[18] > '2018-06-15 18:00:00.000' and row[18] < '2018-07-08 19:00:00.000'):
			newStr = row[18].replace(" ", "T")
			parsedDate = dateutil.parser.parse(newStr)
			withTimeZone = LAtz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()

			newRow = [row[3], row[8], newTimestamp, row[20], row[34]]
			new_rows.append(newRow)

		elif (row[18] > '2018-08-13 15:10:00.000' and row[18] < '2018-08-18 05:00:00.000'):
			newStr = row[18].replace(" ", "T")
			parsedDate = dateutil.parser.parse(newStr)
			withTimeZone = COtz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()

			newRow = [row[3], row[8], newTimestamp, row[20], row[34]]
			new_rows.append(newRow)

		else:
			newStr = row[18].replace(" ", "T")
			print(row[18])
			parsedDate = dateutil.parser.parse(newStr)
			withTimeZone = NYtz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()

			newRow = [row[3], row[8], newTimestamp, row[20], row[34]]
			new_rows.append(newRow)

with open('new_exercise.tsv', 'w+', newline='') as f:
	writer = csv.writer(f, delimiter='\t')
	writer.writerow(newHeader)
	writer.writerows(new_rows)