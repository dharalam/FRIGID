import polars as pl
import json

df = pl.from_dict(json.load(open("../data/reddit_ice_info.json", "r+")))
results = []
df = df.unique()
for row in df.iter_rows(named=True):
    content = f'''For this text, answer the following questions, and return the answers in a json format:
    Title: {row["title"]}
    Body: {row["selftext"]}
    Date Posted: {row["created_utc"]}'''
    print(content)
    data = {}
    data["relevant"] = input("Is this relevant?")
    if not eval(data["relevant"]):
        continue
    data["place"] = input("Where did this happen?")
    data["who"] = input("Who did this happen to?")
    data["when"] = row["created_utc"]
    data["id"] = row["id"]
    results.append(data)

results = {"id": [d["id"] for d in results],
           "place": [d["place"] for d in results],
           "who": [d["who"] for d in results],
           "when": [d["when"] for d in results]
           }

json.dump(results, open("reddit_sentiment_analysis.json", "w+"))