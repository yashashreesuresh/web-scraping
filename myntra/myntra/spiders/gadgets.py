import scrapy
from scrapy_selenium import SeleniumRequest


class GadgetsSpider(scrapy.Spider):
    name = 'gadgets'
    allowed_domains = ['www.myntra.com']
    start_urls = ['https://www.myntra.com/gadgets/']

    def __init__(self):
        yield SeleniumRequest(url='https://duckduckgo.com', screenshot=True, callback=self.parse)

    def parse(self, response):
        img = response.meta['screenshot']

        with open("screenshot1.png", "wb") as img_file:
            img_file.write(img)

