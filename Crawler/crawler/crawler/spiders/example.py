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
        )

    def parse_item(self, response):
        book = Book()
        soup = BeautifulSoup(response.body, 'lxml')
        book['name'] = soup.select('h1', class_='text-h4 mb-2')[0].text.strip()
        book["author"] = soup.find('a', attrs={'class': 'text--darken-1 d-flex grey--text'})["data-autor-link"]
        for element in soup.find_all('div', attrs={'class': 'row text-body-2 py-1 no-gutters'}):
            value = element.get_text().split(":")
            if value[0] == "Nº de páginas":
                 book["pages"] = value[1]
            if value[0] == "Editorial":
                 book["editorial"] = value[1]
            if value[0] == "Año de edición":
                 book["year"] = value[1]
            if value[0] == "Idioma":
                 book["language"] = value[1]
        yield book

