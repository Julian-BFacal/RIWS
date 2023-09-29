# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ExampleSpider(CrawlSpider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    custom_settings = {
                'CLOSESPIDER_ITEMCOUNT' : 10,
                'DOWNLOAD_DELAY' : 0.5}

    rules = (
        Rule(
            LinkExtractor(
                allow=""),
                callback='parse_item',
                follow=True
            ),
        )


    def parse_item(self, response):
        page = response.url
        print(page)
