# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from elasticsearch import Elasticsearch, helpers
import json

class CrawlerPipeline(object):
    listItems = []

    def process_item(self, item, spider):
        self.listItems.append(json.dumps(dict(item)))
        return item

    def close_spider(self, spider):

        es = Elasticsearch('http://localhost:9200')

        actions = [
            {
                "_index": "book",
                "_source": node
            }
            for node in self.listItems
        ]
        #print(actions)

        helpers.bulk(es, actions)
