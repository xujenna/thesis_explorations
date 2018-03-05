.headers on
.mode csv
.output data/my-chrome-output.csv
SELECT datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime'), url FROM urls ORDER BY last_visit_time DESC;
