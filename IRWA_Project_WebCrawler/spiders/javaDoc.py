# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request


class JavadocSpider(scrapy.Spider):
    name = 'javaDoc'
    allowed_domains = ['docs.oracle.com']
    start_urls = ['https://docs.oracle.com/javase/8/docs/api/allclasses-frame.html']

    def parse(self, response):
        links = response.xpath('//div[@class="indexContainer"]/ul/li')
        for link in links:
            rel_link = link.xpath('.//a/@href').extract_first()
            absolute_url = response.urljoin(rel_link)
            yield Request(absolute_url, callback=self.parse_doc)

    def parse_doc(self, response):
        class_name = response.xpath('//h2/text()').extract_first()
        description = response.xpath('//*[@class="description"]/ul/li/div')
        field_detail = response.xpath('//*[@class="details"]/ul/li/ul/li/a[@name="field.detail"]/../ul/li')
        constructor_detail = response.xpath('//*[@class="details"]/ul/li/ul/li/a[@name="constructor.detail"]/../ul/li')
        method_detail = response.xpath('//*[@class="details"]/ul/li/ul/li/a[@name="method.detail"]/../ul/li')

        description_paras = description.xpath('.//p').extract()

        # Scrape Description
        description_list = []

        for p in description_paras:
            soup = BeautifulSoup(p, 'html.parser')
            description_list.append(soup.getText())

        # Scrape Fields
        field_dictionary_list = []

        for field in field_detail:
            field_name = field.xpath('.//h4/text()').extract_first()
            field_details = field.xpath('.//div').extract_first()
            soup = BeautifulSoup(field_details, 'html.parser')
            field_details_new = soup.getText()
            field_dictionary_list.append({'Field_name': field_name, 'Field_details': field_details_new.rstrip('\n ')})

        # Scrape Constructor Details
        constructor_dictionary_list = []

        for cons in constructor_detail:
            constructor_name = cons.xpath('.//h4/text()').extract_first()
            constructor_details = cons.xpath('.//div').extract_first()
            soup = BeautifulSoup(constructor_details, 'html.parser')
            constructor_details_new = soup.getText()
            constructor_dictionary_list.append(
                {'Constructor_name': constructor_name, 'Constructor_details': constructor_details_new.rstrip('\n ')})

            # Scrape Constructor Details
        constructor_dictionary_list = []

        for cons in constructor_detail:
            constructor_name = cons.xpath('.//h4/text()').extract_first()
            constructor_details = cons.xpath('.//div').extract_first()
            soup = BeautifulSoup(constructor_details, 'html.parser')
            constructor_details_new = soup.getText()
            constructor_dictionary_list.append(
                {'Constructor_name': constructor_name, 'Constructor_details': constructor_details_new.rstrip('\n ')})

            # Scrape Constructor Details
        method_dictionary_list = []

        for method in method_detail:
            method_name = method.xpath('.//h4/text()').extract_first()
            method_details = method.xpath('.//div').extract_first()
            soup = BeautifulSoup(method_details, 'html.parser')
            method_details_new = soup.getText()
            method_dictionary_list.append(
                {'Method_name': method_name, 'Method_details': method_details_new.rstrip('\n ')})

        url = response.url

        yield {'URL': url,
               'Class': class_name,
               'Description': description_list,
               'Constructor_Details': constructor_dictionary_list,
               'Field_Details': field_dictionary_list,
               'Method_Details': method_dictionary_list}

# deny_domains='google.com',allow='java'
