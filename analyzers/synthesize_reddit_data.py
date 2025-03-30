import polars as pl
import json

infodf = pl.from_dict(json.load(open("../data/reddit_ice_info.json", "r+")))
sentimentdf = pl.from_dict(json.load(open("../data/reddit_sentiment_analysis.json", "r+")))

new_df = infodf.join(sentimentdf, on="id")
new_df[3, "place"] = "Neptune, New Brunswick, Paulsboro, Newark, Lakewood, Belmar"
json.dump(new_df.to_dict(as_series=False), open("../data/reddit_final_data.json", "w+"))