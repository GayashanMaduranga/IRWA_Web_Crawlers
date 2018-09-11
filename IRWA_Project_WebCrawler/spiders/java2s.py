# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from time import sleep
import random


class Java2sSpider(scrapy.Spider):
    name = 'java2s'
    allowed_domains = ['java2s.com']
    start_urls = ['http://java2s.com/Tutorial/Java/CatalogJava.htm']

    def parse(self, response):
        main_links = response.xpath('//td[not(contains(@class, "tutorialFolderTitle"))]/a/@href').extract()
        # print('\n\n\n Enter Level 1 \n\n\n')
        for link in main_links:
            absolute_url = response.urljoin(link)
            yield Request(absolute_url, callback=self.parse_main_link)

    def parse_main_link(self, response):
        main_links = response.xpath('//td[not(contains(@class, "tutorialFolderTitle"))]/a/@href').extract()
        # print('\n\n\n Enter Level 2 \n\n\n')
        # sleep(random.randrange(1, 3))
        for link in main_links:
            absolute_url = response.urljoin(link)
            yield Request(absolute_url, callback=self.parse_level2_links)

        data = response.xpath('//pre').extract()
        print(len(data))
        extracted_data = []
        if len(data) != 0:
            for d in data:
                soup = BeautifulSoup(d, 'html.parser')
                extracted_data.append(soup.getText())

            yield {'URL': response.url,
                   'Code': extracted_data}

    def parse_level2_links(self, response):
        codes = response.xpath('//pre').extract()
        # print(len(codes))
        title = response.xpath('//h1/text()').extract_first()
        extracted_codes = []
        description = response.xpath('//p[not(contains(@class, "pull-right"))]/text()').extract()
        if len(codes) != 0:
            for d in codes:
                soup = BeautifulSoup(d, 'html.parser')
                extracted_codes.append(soup.getText())

            yield {'URL': response.url,
                   'Title': title,
                   'Code': extracted_codes,
                   'Description': description
                   }
