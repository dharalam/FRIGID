import time
from atproto import Client, client_utils
import json

import numpy as np

def main():

    client = Client()
    profile = client.login('ioannoid.bsky.social', '0sX1H8ostJX7fGs$nKfsx')
    print('Welcome,', profile.display_name)
    
    cursor = None

    dict_NER = {}
    n=20

    params = {'q' : 'ice detention+new jersey', 'limit': 100, 'cursor': '100',}

    data = client.app.bsky.feed.search_posts(params)

    print(data)

if __name__ == '__main__':
    main()


