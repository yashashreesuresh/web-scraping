import scrapy


class ScotchSpider(scrapy.Spider):
    name = 'scotch'
    allowed_domains = ['www.whiskyshop.com']
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    def start_requests(self):
        yield scrapy.Request(url = "https://www.whiskyshop.com/scotch-whisky/",
            callback = self.parse,
            headers = self.header
            )

    def parse(self, response):
        whiskies = response.xpath("//li[@class='item product product-item']")
        for whisky in whiskies:
            name = whisky.xpath(".//a[@class='product-item-link']/text()").get()
            final_price = whisky.xpath(".//span[@data-price-type='finalPrice']/span[@class='price']/text()").extract_first(default="Sold Out")
            yield {
                "name": name,
                "price": final_price
            }

        next_page = response.xpath("(//a[@class='action  next'])[2]/@href").get()

        if next_page:
            yield response.follow(next_page, 
                callback = self.parse,
                headers = self.header
                )