import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QuotesSpider(CrawlSpider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print("proxy: ", response.meta.get('proxy'))
        print("server ip: ", response.ip_address)
