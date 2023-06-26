import scrapy



class Bayut_spiderSpider(scrapy.Spider):
    name = "bayut_spider"
    allowed_domains = ["bayut.com"]
    start_urls = ["https://www.bayut.com/to-rent/property/dubai/"]

    def parse(self, response):
        apartments = response.css('article.ca2f5674')

        for apartment in apartments:
            yield{
                'url' : apartment.css('._4041eb80 a').attrib['href'],
            }

        next_page = response.css('[title="Next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.bayut.com' + next_page
            yield response.follow(next_page_url,callback=self.parse)
