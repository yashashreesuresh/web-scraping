import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys


class ExampleSpider(scrapy.Spider):
    name = 'example'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        img = response.meta['screenshot']
        with open('screenshot1.png', 'wb') as f:
            f.write(img)

        driver = response.meta['driver']

        search_input = driver.find_element_by_id("search_form_input_homepage")
        search_input.send_keys("Hello World!")
        search_input.send_keys(Keys.ENTER)

        # To take full page screenshot, find the longest element in the page
        longest_element = driver.find_element_by_xpath("//body[@class='body--serp']")
        driver.set_window_size(1920, longest_element.size["height"])
        driver.save_screenshot("screenshot2.png")

        response_object = Selector(text=driver.page_source)
        links = response_object.xpath("//div[@class='result__extras__url']/a/@href")
        for link in links:
            yield {
                "url": link.get()
            }

    
