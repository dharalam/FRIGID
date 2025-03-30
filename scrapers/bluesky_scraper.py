import time
from atproto import Client, client_utils
import json

import numpy as np

from transformers import pipeline

def main():
    pipe = pipeline("token-classification", model="dslim/bert-base-NER")

    client = Client()
    profile = client.login('ioannoid.bsky.social', '0sX1H8ostJX7fGs$nKfsx')
    print('Welcome,', profile.display_name)
    
    cursor = None

    dict_NER = {}
    n=20


    for i in range(n):
        print(f'Page {i}/{n}')
        params = {'q': 'ice detention+nj', 'limit': 100}
        if cursor:
            params['cursor'] = cursor
        data = client.app.bsky.feed.search_posts(params)
        cursor = data.cursor
        for post in json.loads(data.json())['posts']:
            post_text = post['record']['text']
            out = pipe(post_text)

            i = 0

            while i < len(out):
                loc = ''
                if out[i]['entity'] == 'B-LOC':
                    dict_NER[out[i]['word']] = dict_NER.get(out[i]['word'], 0) + 1 
                elif out[i]['entity'] == 'I-LOC':
                    dict_NER[out[i]['word']] = dict_NER.get(out[i]['word'], 0) + 1 

                i+=1
        time.sleep(0.5)
        if cursor is None:
            break


    dict_NER = {k: v for k, v in sorted(dict_NER.items(), key=lambda item: item[1], reverse=True)}

    with open('dump.jsonl', 'w') as f:
        f.write(str(dict_NER))

if __name__ == '__main__':
    main()


