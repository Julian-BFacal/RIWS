# -*- coding: utf-8 -*-
import scrapy
import json
from crawler.items import Book
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
from scrapy.http.response.html import HtmlResponse

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
                allow="www.casadellibro.com/libro-la-chica-del-verano-novela/9788448038977/14166923"),
                callback='parse_item',
                follow=False
            ),
        )

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_item, args={'wait': 0.5})

    """
    def parse(self,response):
        ht = HtmlResponse(url=response.url, body=response.body, encoding="utf-8", request=response.request)
    """

    def _requests_to_follow(self,response):
        if not isinstance(response, HtmlResponse):
            response = HtmlResponse(url=response.url, status=response.status, header = response.headers,
                body = response.body, flags = response.flags, encoding = "utf-8", request = response.request,
                certificate = response.certificate, ip_address= response.ip_address)
        return super()._requests_to_follow(response)


    def parse_item(self, response):
        book = Book()
        soup = BeautifulSoup(response.body, 'lxml')
        
        print(soup.find_all('div', attrs={'class': 'text-h4 font-weight-bold'}))
        """
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
        """

