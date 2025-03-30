# import requests
# import json
# import time
#
# with open('news12.json', 'w') as f:
#     data = []
#     for i in range(0,1000,6):
#         r = requests.get(f'https://newjersey.news12.com/api/contentful/collection?skip={i}&categories=5UB6tVXBkd7ARvCyvOS8bO&regions=22cHKtE2AFPCc3BJGwRDiG,5g2XMQgs47iQJwz6fi9xnf,1H3vrQbJ0zU8HAcSAA9gMN,5Fh5vPC7p0LsYyI9RfLA4I,57YhTpGKbXsF2NlnDZfH0,64Yt6apvEZsviUQbS4GCsc,67ToDy2u8uXYg6Fj4qZWgH')
#
#         data.extend(r.json()['stories'])
#         time.sleep(0.05)
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
        
        contents = response.xpath('//div[@gridarea="content"]/div/div/text()').getall()
        date = response.xpath('//div[@class="sc-fsYfdN Mnyxl sc-eTNRI dPtPJq"]/p/text()').getall()
        
        yield {''.join(date): contents,}

        
