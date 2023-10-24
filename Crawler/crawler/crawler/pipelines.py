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
        self.listItems.append(item)
        return item

    def close_spider(self, spider):

        es = Elasticsearch('http://localhost:9200')

        mappings = {
        "properties": {
            "name": {"type": "text", "index": True},
            "author": {"type": "text"},
            "editorial": {"type": "text"},
            "year": {"type": "integer"},
            "pages": {"type": "integer"},
            "language": {"type": "text"},
            "tags": {"type": "text", "analyzer": "tags_analyzer"},
            "sinopsis": {"type": "text", "index": False},
            "portada": {"type": "text", "index": False},
            }
        }

        settings = {
            "analysis": {
                "analyzer": {
                    "tags_analyzer": {
                        "type": "custom",
                        "tokenizer": "my_tokenizer",
                        "filter": [ "lowercase" ]
                    }
                }, 
                "tokenizer": {
                    "my_tokenizer": {
                        "type": "pattern",
                        "pattern": ","
                    }
                }
            }
        }
        if not es.indices.exists(index="book"):
            es.indices.create(index="book", mappings=mappings, settings=settings)
        bulk_data = [
            {
                "_index": "book",
                "_source": {   
                    "name": node["name"],
                    "author": node["author"],
                    "editorial": node["editorial"],
                    "tags": node["tags"],
                    "year": node["year"],
                    "pages": node["pages"],
                    "language": node["language"],
                    "sinopsis": node["sinopsis"],
                    "portada": node["portada"],
                    }
            }
            for node in self.listItems
        ]
        helpers.bulk(es, bulk_data)
        es.indices.refresh(index="book")
        es.cat.count(index="book", format="json")
