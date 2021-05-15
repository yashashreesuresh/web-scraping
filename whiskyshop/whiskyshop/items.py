# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def remove_currency(value):
    return value.replace("£", "").strip()

class WhiskyshopItem(scrapy.Item):
    name = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        input_processor = MapCompose(remove_currency),
        output_processor = TakeFirst()
    )
