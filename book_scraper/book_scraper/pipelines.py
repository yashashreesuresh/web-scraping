# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class BookScraperPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'bookname': item.get('title')}) for x in item.get(self.images_urls_field, [])]


    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = request.meta["bookname"]
        return f'full/{image_name}.jpg'