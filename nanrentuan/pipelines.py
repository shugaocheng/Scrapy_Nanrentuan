# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
import codecs
import json

class NanrentuanEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('nanrentuan.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self):
        self.file.close()

class NanrentuanPipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url,meta={'item':item,'index':item['image_urls'].index(image_url)})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        index = request.meta['index']
        image_name = item['image_name'][index]+'.'+request.url.split('/')[-1].split('.')[-1]
        filename = u'full/{0}/{1}'.format(item['name'],image_name)
        return filename

    # def item_completed(self,results,item,info):
    #     image_paths = [x['path'] for ok,x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     item['image_paths'] = image_paths
    #     return item