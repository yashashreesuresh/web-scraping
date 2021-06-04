import scrapy
import time
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class CoinSeleniumSpider(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/currencies/dogecoin/historical-data/']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)

        # set the window size to max to enable all the html contents to be retrieved
        driver.set_window_size(1920, 1080)

        driver.get('https://coinmarketcap.com/currencies/dogecoin/historical-data/')

        # wait for the html to load
        time.sleep(3)

        self.data = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.data)
        for row in resp.xpath("//table[@class='cmc-table table___1p4Jy ']/tbody/tr"):
            yield {
                "Date": row.xpath(".//td[1]/text()").get(),
                "Open price": row.xpath(".//td[2]/text()").get(),
                "Close price": row.xpath(".//td[5]/text()").get(),
                "Volume": row.xpath(".//td[6]/text()").get(),
                "Market Cap": row.xpath(".//td[7]/text()").get()
            }
