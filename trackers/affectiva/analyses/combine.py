import json
import glob

result = []

for f in glob.glob("*.json"):
    with open(f, "rb") as infile:
        result += json.load(infile)
        # result.append(json.load(infile))


with open("merged_file.json", "w") as outfile:
     json.dump(result, outfile, indent=2)
