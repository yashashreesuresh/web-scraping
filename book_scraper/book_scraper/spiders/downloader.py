import scrapy
from book_scraper.items import BookScraperItem


class DownloaderSpider(scrapy.Spider):
    name = 'downloader'
    allowed_domains = ['books.toscrape.com/']
    start_urls = ['http://books.toscrape.com/']
    url = 'http://books.toscrape.com/'

    def parse(self, response):
        books = response.xpath("//article[@class='product_pod']")
        for book in books:

            """
            We can just use yield directly if we don't want to rename downloaded image names
            NOTE: The image to be downloaded needs to be provided through a list `image_urls`  
            yield {
                "title": book.xpath(".//a/@title").get(),
                "price": book.xpath(".//p[@class='price_color']/text()").get(),
                "image_urls": [self.url + book.xpath(".//img/@src").get()]
            }
            """
            
            item = BookScraperItem()
            item["title"] = book.xpath(".//a/@title").get()
            item["price"] = book.xpath(".//p[@class='price_color']/text()").get()
            item["image_urls"] = [self.url + book.xpath(".//img/@src").get()]   # converting the relative url to absolute url
            yield item
            
