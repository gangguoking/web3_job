# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 爬取到的数据写入到redis数据库
import redis
from scrapy import Item


class Web3JobPipeline:
    def process_item(self, item, spider):
        return item


class Web3CareerRedisPipeline(object):

    # 打开数据库
    def open_spider(self, spider):
        db_host = spider.settings.get('REDIS_HOST', 'localhost')
        db_port = spider.settings.get('REDIS_PORT', 6379)
        db_index = spider.settings.get('REDIS_DB_INDEX', 0)
        self.db_conn = redis.StrictRedis(host=db_host, port=db_port, db=db_index)
        self.item_i = 0

    # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.connection_pool.disconnect()

    # 处理数据
    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    # 插入数据
    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)

        self.item_i += 1
        self.db_conn.hset(item['fromSource'], item['jobId'], json.dumps(item))
