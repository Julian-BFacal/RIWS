# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from elasticsearch import Elasticsearch, helpers
import json
name_completion = []
class CrawlerPipeline(object):
    listItems = []


    def process_item(self, item, spider):
        self.listItems.append(item)
        return item

    def close_spider(self, spider):
        global name_completion
        es = Elasticsearch(['http://localhost:9200'], http_auth=('elastic', 'nA88Kiu2ok-4M+G7*Dif'))

        mappings = {
        "properties": {
            "name": {
                "type": "text", 
                "index": True, 
                "analyzer": "name_analyzer",
                "fields": {
                    "suggest": {
                        "type": "search_as_you_type"
                    },
                    "keyword": {
                        "type": "keyword",
                        "normalizer": "my_normalizer",
                    }
                }
            },
            "author": {
                "type": "text",
                "analyzer": "name_analyzer",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "normalizer": "my_normalizer",
                    }
                }
            },
            "editorial": {"type": "text"},
            "year": {"type": "integer"},
            "pages": {"type": "integer"},
            "language": {"type": "keyword"},
            "tags": {"type": "text","fielddata":True,"analyzer": "tags_analyzer"},
            "sinopsis": {"type": "text", "index": False},
            "portada": {"type": "text", "index": False},
            "name_completion": {"type": "completion"}
            }
        }

        settings = {
            "analysis": {
                "analyzer": {
                    "tags_analyzer": {
                        "type": "custom",
                        "tokenizer": "my_tokenizer",
                        "filter": [ "uppercase", "asciifolding" ]
                    },
                    "name_analyzer": {
                        "type": "custom",
                        "tokenizer": "name_toke",
                        "filter": [ "uppercase", "asciifolding" ]
                    }
                }, 
                "normalizer": {
                    "my_normalizer": {
                      "type": "custom",
                      "filter": ["lowercase", "asciifolding"]
                    }
                } ,
                "tokenizer": {
                    "my_tokenizer": {
                        "type": "pattern",
                        "pattern": ","
                    },
                    "name_toke": {
                        "type": "pattern",
                        "pattern": " "
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
                    "name_completion": node["name"],
                    }
            }
            for node in self.listItems
        ]
        helpers.bulk(es, bulk_data)
        es.indices.refresh(index="book")
        es.cat.count(index="book", format="json")
