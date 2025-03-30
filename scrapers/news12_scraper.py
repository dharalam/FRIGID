# import requests
# import json
# import time
#
# with open('news12.json', 'w') as f:
#     data = []
#     for i in range(0,1000,6):
#         r = requests.get(f'https://newjersey.news12.com/api/contentful/collection?skip={i}&categories=2brih7NOlAOnRZ7REArZlS&regions=22cHKtE2AFPCc3BJGwRDiG')
#
#         data.extend(r.json()['stories'])
#         time.sleep(0.005)
#
#     json.dump(data, f)
import re
import json
import argparse
from urllib.parse import urljoin

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


# doesn't really work rn bc it has to be site-specific for traversal but this is a good template

class News12Spider(scrapy.Spider):
    name = 'news12_spider'
    allowed_domains = ['newjersey.news12.com']
    start_urls = ['https://newjersey.news12.com/category/immigration']
    
    def __init__(self, *args, **kwargs):
        super(News12Spider, self).__init__(*args, **kwargs)
        
        self.start_urls = []

        with open('articles_news12.json', 'r') as f:
            articles = json.load(f)
            self.start_urls.extend(articles)
            
    def parse(self, response):
        # Extract post links from the subreddit page 
        
        contents = response.xpath('//div[@gridarea="content"]').getall()
        
        yield {''.join(date): contents,}

        
