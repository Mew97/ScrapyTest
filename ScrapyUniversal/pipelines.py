# -*- coding: utf-8 -*-

import pymongo
from random import choice
from ScrapyUniversal.custom_settings import COLLECTION, ITEM


class ScrapyuniversalPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, download_path):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.download_path = download_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('ALICE_MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            download_path=crawler.settings.get('DOWNLOAD_PATH'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # key_items = dict(item)
        # for item0 in key_items["bus_list"]:
        #     self.db[COLLECTION].insert({"bus_num": key_items["bus_num"], "bus_list": item0})
        self.db[COLLECTION].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
