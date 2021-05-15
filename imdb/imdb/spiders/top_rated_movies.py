import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TopRatedMoviesSpider(CrawlSpider):
    name = 'top_rated_movies'
    allowed_domains = ['www.imdb.com']
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url = "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating",
            headers = {"User-Agent": self.user_agent}
            )

    # Needn't specify @href in the xpath expression (specify only till 'a' element)
    # First rule extracts all the movie links and makes a call to each movie link (Each produced link will be used to generate a Request object and the response is sent to callback)
    # Second rules helps in pagination, needn't specify callback as the First rule is executed as soon as we navigate to next page
    rules = (
        Rule(LinkExtractor(restrict_xpaths = "//h3[@class='lister-item-header']/a"), callback = "parse_item", follow = True, process_request = "set_user_agent"),
        Rule(LinkExtractor(restrict_xpaths = "(//a[@class='lister-page-next next-page'])[2]"), follow = True, process_request = "set_user_agent")
    )

    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "title": response.xpath("(//h1)[1]/text()").get().strip(),
            "rating": response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            "release-date": response.xpath("//a[@title='See more release dates']/text()").get(),
            "genre": response.xpath("(//div[@class='subtext']/a/text())[1]").get(),
            "duration": response.xpath("normalize-space(//div[@class='subtext']/time/text())").get(),
            "movie-url": response.xpath("//a[@class='tracked-offsite-link buybox__link']/@href").get()
        }
    