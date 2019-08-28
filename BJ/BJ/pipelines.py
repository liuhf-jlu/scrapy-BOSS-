# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import time
import pymongo
from scrapy import Item


class BjPipeline(object):
    def process_item(self, item, spider):
        return item


class ImportToJson(object):
    # 创建json文件
    def __init__(self):
        # 构建json文件的名称，bosszhipin_日期.json
        jsonName = 'bosszhipin_' + str(time.strftime("%Y%m%d", time.localtime())) + '.json'
        self.f = open(jsonName, 'w')

    # 打开爬虫时执行的动作
    def open_spider(self, spider):
        pass

    # 主管道
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(content)
        return item

    # 爬虫关闭时执行的动作
    def close_spider(self, spider):
        self.f.close()


class ImportToMongo(object):
    # 读取MongoDB中的MONGO_DB_URI
    # 读取MongoDB中的MONGO_DB_NAME
    @classmethod
    def from_crawler(cls,crawler):
        cls.DB_URI=crawler.settings.get('MONGO_DB_URI')
        cls.DB_NAME=crawler.settings.get('MONGO_DB_NAME')
        return cls()

    def __init__(self):
        pass

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.DB_URI)
        self.db=self.client[self.DB_NAME]

    def process_item(self,item,spider):
        db_name=spider.name+'_'+str(time.strftime("%Y%m%d",time.localtime()))
        collection=self.db[db_name]
        post=dict(item) if isinstance(item,Item) else item
        collection.insert_one(post)
        return item

    def close_spider(self,spider):
        self.client.close()

