import praw
import polars as pl
from IPython.display import HTML
import time
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import json

load_dotenv()

# @title Reddit API Setup
client_id = os.getenv("REDDIT_CLIENTID") # @param {type:"string"} # Get from https://www.reddit.com/prefs/apps
client_secret = os.getenv("REDDIT_CLIENTSECRET") # @param {type:"string"}
user_agent = os.getenv("REDDIT_USER") # @param {type:"string"}

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# @title Scraper Configuration
subreddit_name = "newark" # @param {type:"string"}
post_limit = 1000 # @param {type:"slider", min:100, max:1000, step:100}
output_filename = "../data/reddit_ice_info.json" # @param {type:"string"}
keywords = {"ICE", "immigrant", "detain"}

print(f"⚙️ Targeting r/{subreddit_name} for {post_limit} posts")

def display_clickable(df):
    df_display = df.copy()
    df_display['url'] = df['url'].apply(lambda x: f'<a href="{x}" target="_blank">🔗 Link</a>')
    return HTML(df_display[['title', 'label', 'url']].to_html(escape=False))

def utc_to_datetime(utc_timestamp):
  """Converts a UTC timestamp to a datetime object.

  Args:
    utc_timestamp: A numeric UTC timestamp (seconds since epoch).

  Returns:
    A datetime object representing the UTC time, or None if the input is invalid.
  """
  try:
    return datetime.fromtimestamp(utc_timestamp, tz=timezone.utc)
  except (TypeError, ValueError):
    return None

def get_comments(id):
    comment_stream = reddit.submission(id)
    comment_stream.comments.replace_more(limit=None)
    return "\n".join([c.body for c in comment_stream.comments.list()])

# @title Paginated Scraper
def scrape_subreddit():
    posts = []
    subreddit = reddit.subreddit(subreddit_name)
    search_results = subreddit.search("ICE", sort="new", syntax="plain", limit=None)
    last_post = None
    start_time = time.time()

    print(f"⏳ Scanning r/{subreddit_name} for {post_limit} polarized posts...")

    try:
        while len(posts) < post_limit:
            # Get next batch (max 100 per request)
            
            batch = list(search_results)
            if not batch:
                break  # No more posts
            for post in batch:
                for kw in keywords:
                    if kw in str(post.title) or kw in str(post.selftext): # or kw in get_comments(post.id):
                        posts.append({
                            "title": post.title if post.title else " ",
                            "selftext": str(post.selftext) if post.selftext else " ",
                            "upvote_ratio": post.upvote_ratio,
                            "url": f"https://reddit.com{post.permalink}",
                            "num_comments": post.num_comments,
                            "id": post.id,
                            "created_utc": utc_to_datetime(post.created_utc).strftime('%Y-%m-%d %H:%M'),
                            #"comments": get_comments(post.id)
                        })
                        break

            last_post = batch[-1].fullname  # Pagination marker
            print(f"Progress: {len(posts)}/{post_limit} posts with keywords {keywords}")

            # Rate limit protection
            if len(posts) % 300 == 0:
                time.sleep(2)

            if len(batch) < 100:
                break  # Reached end of available posts

        print(f"\n✅ Found {len(posts)} posts in {(time.time()-start_time):.1f}s")
        return pl.DataFrame(posts)

    except Exception as e:
        print(f"\n⚠️ Partial results: {len(posts)} posts before error")
        print(f"Error: {str(e)}")
        return pl.DataFrame(posts) if posts else None

print("✅ Scraper loaded!")

try:
    # Scrape data
    df = scrape_subreddit()

    if df is not None and not df.is_empty():
        # Save to CSV
        json.dump(df.to_dict(as_series=False), open(output_filename, "w+"))
except Exception as e:
    print(f"❌ Fatal error: {str(e)}")

