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


with open('responses_copy.tsv', newline='') as f:
	reader = csv.reader(f, delimiter='\t')
	# writer = csv.writer(f, delimiter='\t')
	header = next(reader)
	new_rows = []

	for row in reader:
		if ((row[0] > '2018-05-11T18:00:00.000000' and row[0] < '2018-05-16T20:00:00.000000') or (row[0] > '2018-08-06T18:20:00.000000' and row[0] < '2018-08-13T15:10:00.000000')):
			parsedDate = dateutil.parser.parse(row[0])
			withTimeZone = CHItz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()

			newRow = [row[0], newTimestamp, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]]
			new_rows.append(newRow)

		elif (row[0] > '2018-06-15T18:00:00.000000' and row[0] < '2018-07-08T19:00:00.000000'):
			parsedDate = dateutil.parser.parse(row[0])
			withTimeZone = LAtz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()

			newRow = [row[0], newTimestamp, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]]
			new_rows.append(newRow)

		elif (row[0] > '2018-08-13T15:10:00.000000' and row[0] < '2018-08-18T05:00:00.000000'):
			parsedDate = dateutil.parser.parse(row[0])
			withTimeZone = COtz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()

			newRow = [row[0], newTimestamp, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]]
			new_rows.append(newRow)

		else:
			parsedDate = dateutil.parser.parse(row[0])
			withTimeZone = NYtz.localize(parsedDate)
			newTimestamp = (withTimeZone - epoch).total_seconds()

			newRow = [row[0], newTimestamp, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]]
			new_rows.append(newRow)

with open('new_responses.tsv', 'w+', newline='') as f:
	writer = csv.writer(f, delimiter='\t')
	writer.writerow(header)
	writer.writerows(new_rows)