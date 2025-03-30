import requests
import polars as pl
import os
from dotenv import load_dotenv
import time
from tqdm import tqdm

load_dotenv()
API_URL = "https://router.huggingface.co/hf-inference/models/google/byt5-base"
headers = {"Authorization": f"Bearer {os.getenv("FRIGID_KEY_HUGGINGFACE")}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

reddit_df = pl.read_csv("./data/reddit_ice_info.csv")
messages = []
for row in reddit_df.iter_rows(named=True):
    content = f'''For this text, answer the following questions, and return the answers in a json format:
    Title: {row["title"]}
    Body: {row["selftext"]}
    Date Posted: {row["created_utc"]}
    Comments: {row["comments"]}
    
    
    1. Does this pertain to ICE, immigration, or detainment of immigrants?
    2. If someone was detained, where were they detained, if applicable?
    3. If someone was detained, when were they detained, if applicable?
    4. If someone was detained, what was their name, if applicable?
    '''

    messages.append(content)

for msg in tqdm(messages):
    with open("reddit_analysis_out.txt", "a+") as f:
        output = query({"inputs": msg})
        f.write(str(output))
