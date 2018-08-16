# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class JavadocSpider(CrawlSpider):
    name = 'javaDoc'
    allowed_domains = ['docs.oracle.com']
    start_urls = ['https://docs.oracle.com/javase/8/docs/api/']

    rules = (Rule(LinkExtractor(),callback='parse', follow=False), )
    
    def parse(self, response):
        print(response.url)


#deny_domains='google.com',allow='java'