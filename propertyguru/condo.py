from logging import debug
from selenium import webdriver
from selenium_stealth import stealth
import time
from shutil import which
from lxml import html
import pandas as pd
from stem.util.log import get_logger
from toripchanger import TorIpChanger
from stem import Signal
from stem.control import Controller


all_listings = []
all_property_details = []


def rotate_ip():
    logger = get_logger()
    logger.propagate = False
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='mytor')
        controller.signal(Signal.NEWNYM)
    time.sleep(1)


def get_condominium_details(url):
    rotate_ip()

    property_details = {}
    driver.get(url)
    response = html.fromstring(driver.page_source)

    property_details['URL'] = url

    rental_price = response.xpath("//div[@class='price-overview-row rentals']/div/span/span/text()")
    if rental_price:
        property_details['Rental Price Range'] = f'{rental_price[0]} {rental_price[1]} ~ {rental_price[2]} {rental_price[3]}' 
    else:
        property_details['Rental Price Range'] = "Not available"

    property_details['Address'] = response.xpath("//span[@itemprop='streetAddress']/text()")[0]

    property_details['Rating'] = response.xpath("(//p[@class='rating-text']/span/text())[1]")[0].strip()

    detail_label = response.xpath("//th[@class='label-block']/text()")
    detail_value = response.xpath("//td[@class='value-block']/text()")
    
    for label, value in zip(detail_label, detail_value):
        property_details[label] = value

    property_details['Geocodes - Latitude'] = response.xpath("//div[@id='map-canvas']/@data-latitude")[0]
    property_details['Geocodes - Longitude'] = response.xpath("//div[@id='map-canvas']/@data-longitude")[0]
    
    facilities = response.xpath("//li[@itemprop='amenityFeature']/span/text()")
    property_details['Facilities & Amenities'] = ", ".join(facilities)

    similar_interests = response.xpath("//div[@class='widget-links-body']")
    for item in similar_interests:
        label = item.xpath("./text()")[0].strip()
        if not label:
            values = item.xpath("./ul/li/a/text()")
            values = [" ".join(v.split()) for v in values]
            property_details["Similar Condominiums"] = ", ".join(values)
        else:
            values = item.xpath("./ul/li/a/span/text()")
            property_details[label] = ", ".join(values)
        
    print(property_details)
    all_property_details.append(property_details)


def get_listings(url):
    rotate_ip()

    driver.get(url)
    response = html.fromstring(driver.page_source)

    listings = response.xpath("//div[@class='gallery-container']/a[@class='nav-link']/@href")
    listings = [f'https://www.propertyguru.com.my{listing}' for listing in listings]
    all_listings.extend(listings)

    for listing in listings:
        get_condominium_details(listing)

    next_page = response.xpath("//li[@class='pagination-next']/a/@href")
    if next_page:
        next_page_url = f'https://www.propertyguru.com.my{next_page[0]}'
        get_listings(driver, next_page_url)
        print(next_page_url)


if __name__ == "__main__":
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        options.add_argument("--headless")
        options.add_argument('--proxy-server=http://127.0.0.1:8118')

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        global driver
        driver = webdriver.Chrome(options=options, executable_path=which("./chromedriver"))

        stealth(driver,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        url = "https://www.propertyguru.com.my/condo/search-condo-project"
        get_listings(url)

    except Exception as e:
        print("Encountered following exception: ", e)

    finally:
        driver.quit()
        listings_data = pd.DataFrame(all_property_details)
        listings_data.to_excel('condo_listings_data.xlsx')