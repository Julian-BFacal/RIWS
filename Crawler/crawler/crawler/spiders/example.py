# -*- coding: utf-8 -*-
import scrapy
import json
import re
from crawler.items import Book
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class ExampleSpider(CrawlSpider):
    name = 'example'
    count=0;
    allowed_domains = ['casadellibro.com']
    start_urls = ['https://www.casadellibro.com/']

    custom_settings = {
                'CLOSESPIDER_ITEMCOUNT' : 20,
                'CLOSESPIDER_PAGECOUNT' : 300000,
                'DOWNLOAD_DELAY' : 0.5}

    rules = (
        Rule(
            LinkExtractor(
                allow="www.casadellibro.com/libro-"),
                callback='parse_item',
                follow=False
            ),
        Rule(
            LinkExtractor(
                allow="www.casadellibro.com/"),
                callback='',
                follow=True
            ),
        )

    def parse_item(self, response):
        book = Book()
        soup = BeautifulSoup(response.body, 'lxml')

        aux = []

        for element in soup.find_all("span",attrs={"class":"v-chip__content"}):
            aux.append(element.get_text().replace("\n","").replace("\t",""))
        book['tags']=aux
        book['name'] = soup.select('h1', class_='text-h4 mb-2')[0].text.strip().replace("\n","").replace("\t","")
        try:
            book['sinopsis']=soup.find_all("div",attrs={"class":"formated-text"})[0].get_text()
        except:
            book["sinopsis"]=None
        aux=soup.find('a', attrs={'class': 'text--darken-1 d-flex grey--text'})
        if aux is not None:
            book['author'] = aux["data-autor-link"]
        else:
            book['author'] = "ANÓNIMO"

        aux=soup.find('div', attrs={'class': 'swiper-img-container'}).find('img')
        if aux is not None:
            book['portada'] =aux['src']
        else:
            book['portada']=None

        book["pages"]=None
        book["editorial"]=None
        book["year"]=None
        book["language"]=None

        for element in soup.find_all('div', attrs={'class': 'caracteristicas mt-4 pt-4'}):
            value = element.get_text().split("\n")
            for tab in value:
                value = tab.split(":")
                if len(value) > 1:
                    value[0] = value[0].replace("\t", "")
                    value[1] = value[1].strip()
                    print(value)

                    if value[0] == "Nº de páginas":
                         book["pages"] = value[1]
                    if value[0] == "Editorial":
                         book["editorial"] = value[1]
                    if value[0] == "Año de edición":
                         book["year"] = value[1]
                    if value[0] == "Idioma":
                         book["language"] = value[1]

        self.count+=1
        print(str(self.count) + "  -->  Indexado o libro " + book["name"] + " de " + book['author'])

        yield book