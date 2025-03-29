# Use a pipeline as a high-level helper
from transformers import pipeline
import polars as pl



reddit_df = pl.read_csv("..\data\reddit_ice_info.csv")
for row in reddit_df.iter_rows():
    content = f'''For this text, answer the following questions, and return the answers in a json format:
    {}
    '''



    messages = [
        {"role": "user", "content": "Who are you?"},
    ]
    pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-V3-0324", trust_remote_code=True)
    pipe(messages)