# -*- coding: utf-8 -*-
import scrapy
from crawler.items import Book
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class ExampleSpider(CrawlSpider):
    name = 'example'
    allowed_domains = ['casadellibro.com']
    start_urls = ['https://www.casadellibro.com/libro-la-chica-del-verano-novela/9788448038977/14166923/']

    custom_settings = {
                'CLOSESPIDER_ITEMCOUNT' : 10,
                'DOWNLOAD_DELAY' : 0.5}

    rules = (
        Rule(
            LinkExtractor(
                allow="www.casadellibro.com/libro-"),
                callback='parse_item',
                follow=False
            ),
        )


    def parse_item(self, response):
        book = Book()
        soup = BeautifulSoup(response.body, 'lxml')
        book['name'] = soup.select('h1', class_='text-h4 mb-2')[0].text.strip()
        yield book
