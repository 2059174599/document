# -*- coding: utf-8 -*-

# Define your item pipelines here
import scrapy
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import json
import codecs
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class LagouPipeline(ImagesPipeline):
#     # def process_item(self, item, spider):
#     #     # item = request.meta['item']
#     #     # # return item
#     #     # print(item)
#     #     return item
#     def get_media_requests(self, item, info):
#     	item = request.meta['item']
#     	print(item)
class LagouPipeline(object):

    # 初始化时指定要操作的文件
    def __init__(self):
        self.file = codecs.open('questions.json', 'w', encoding='utf-8')

    # 存储数据，将 Item 实例作为 json 数据写入到文件中
    def process_item(self, item, spider):
        item = request.meta['item']
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item
    # 处理结束后关闭 文件 IO 流
    def close_spider(self, spider):
        self.file.close()