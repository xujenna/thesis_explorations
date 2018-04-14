import json
import glob

result = []
avg_results = {}

for f in glob.glob("*.json"):
    with open(f, "rb") as infile:
        avg_results = {}
        print(f)
        j = json.load(infile)
        emotions = []

        attention_values = list(map(lambda x: x.get('attention',0), j))
        avg_attention = sum(attention_values)/len(attention_values)
        avg_results["attention"] = avg_attention

        valence_values = list(map(lambda x: x.get('valence',0), j))
        avg_valence = sum(valence_values)/len(valence_values)
        avg_results["valence"] = avg_valence

        engagement_values = list(map(lambda x: x.get('engagement',0), j))
        avg_engagement = sum(engagement_values)/len(engagement_values)
        avg_results["engagement"] = sum(engagement_values)/len(engagement_values)

        time_values = list(map(lambda x: x.get('time', 0), j))
        avg_results["time"] = time_values[0]

        emoji_values = list(map(lambda x: x.get('emoji', 0), j))
        unique_emoji = list(set(emoji_values))
        avg_results["emoji"] = unique_emoji

        blink_values = list(filter(lambda x: x!=0, map(lambda x: x.get('eyeClosure', 0), j)))
        blinks = int(len(blink_values) / 2)
        avg_results["blinks"] = blinks

        anger_values = list(filter(lambda x: x!=0, map(lambda x: x.get('anger', 0), j)))
        if(len(anger_values) > 0):
            emotions.append("anger")

        contempt_values = list(filter(lambda x: x!=0, map(lambda x: x.get('contempt', 0), j)))
        if(len(contempt_values) > 0):
            emotions.append("contempt")

        disgust_values = list(filter(lambda x: x!=0, map(lambda x: x.get('disgust', 0), j)))
        if(len(disgust_values) > 0):
            emotions.append("disgust")

        fear_values = list(filter(lambda x: x!=0, map(lambda x: x.get('fear', 0), j)))
        if(len(fear_values) > 0):
            emotions.append("fear")

        joy_values = list(filter(lambda x: x!=0, map(lambda x: x.get('joy', 0), j)))
        if(len(joy_values) > 0):
            emotions.append("joy")

        sadness_values = list(filter(lambda x: x!=0, map(lambda x: x.get('sadness', 0), j)))
        if(len(sadness_values) > 0):
            emotions.append("sadness")

        surprise_values = list(filter(lambda x: x!=0, map(lambda x: x.get('surprise', 0), j)))
        if(len(surprise_values) > 0):
            emotions.append("surprise")

        # result += json.load(infile)
        avg_results["emotions"] = emotions
        result.append(avg_results)



with open("merged_file.json", "w") as outfile:
     json.dump(result, outfile, indent=2)
