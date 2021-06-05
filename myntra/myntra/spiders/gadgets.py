from os import wait
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest


class GadgetsSpider(scrapy.Spider):
    name = 'gadgets'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.myntra.com/gadgets/",
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']

        # Checking user-agent
        print(response.request.headers)

        response_object = Selector(text=driver.page_source)
        items = response_object.xpath("//div[@class='product-productMetaInfo']")

        for item in items:
            # Check if the product has disount
            if item.xpath("(.//span[@class='product-discountedPrice']/text())[2]"):
                yield {
                    "Product": item.xpath(".//h4[@class='product-product']/text()").get(),
                    "Brand": item.xpath(".//h3[@class='product-brand']/text()").get(),
                    "Discounted Price": item.xpath("(.//span[@class='product-discountedPrice']/text())[2]").get(),
                    "Original Price": item.xpath("(.//span[@class='product-strike']/text())[2]").get()
                }
            else:
                yield {
                    "Product": item.xpath(".//h4[@class='product-product']/text()").get(),
                    "Brand": item.xpath(".//h3[@class='product-brand']/text()").get(),
                    "Discounted Price": "No Discount",
                    "Original Price": item.xpath("(.//div[@class='product-price']/span/text())[2]").get()
                }

        # Scrape items from next page if it exists
        next_page = response_object.xpath("//li[@class='pagination-next']/a")
        if next_page:
            yield SeleniumRequest(
                url=next_page.xpath(".//@href").get(),
                wait_time=3,
                callback=self.parse
            )
