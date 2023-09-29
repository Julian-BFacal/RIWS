# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ExampleSpider(CrawlSpider):
    name = 'example'
    allowed_domains = ['casadellibro.com']
    start_urls = ['https://www.casadellibro.com/']

    custom_settings = {
                'CLOSESPIDER_ITEMCOUNT' : 5,
                'CLOSESPIDER_PAGECOUNT' : 100,
                'DOWNLOAD_DELAY' : 0}

    rules = (
    	Rule(
            LinkExtractor(
                allow="casadellibro.com/libro-"),
                callback='parse_item',
                follow=False
            ),
        Rule(
            LinkExtractor(
                allow=""),
                callback='',
                follow=True
            ),
        )

    def parse_item(self, response):
        page = response.url
        print(page+"......................................................... ")
