# -*- coding: utf-8 -*-
import scrapy


class JavadocTestSpider(scrapy.Spider):
    name = 'javaDoc-test'
    allowed_domains = ['docs.oracle.com']
    start_urls = ['http://docs.oracle.com/']

    def parse(self, response):
        pass
