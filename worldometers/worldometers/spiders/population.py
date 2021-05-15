import scrapy


class PopulationSpider(scrapy.Spider):
    name = 'population'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            relative_url = country.xpath(".//@href").get()

            # yield {
            #     "name": name,
            #     "link": relative_url
            # }

            # scrapy.Request requires absolute url to make a request
            # absolute_url = "https://www.worldometers.info/" + relative_url
            # yield scrapy.Request(absolute_url, callback = self.parse_country, meta = {"country_name": name})
            
            # response.follow makes a request with relative url as well unlike scrapy.Request
            # sending the meta data to be accessed in callback function
            yield response.follow(relative_url, callback = self.parse_country, meta = {"country_name": name})

    def parse_country(self, response):
        country = response.meta.get("country_name")
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                "country": country,
                "year": year,
                "population": population,
                "user-agent": response.request.headers.get('User-Agent').decode('utf-8')
            }