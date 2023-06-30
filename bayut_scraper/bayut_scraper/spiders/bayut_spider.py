import scrapy
from bayut_scraper.items import BayutItem



class Bayut_spiderSpider(scrapy.Spider):
    name = "bayut_spider"
    allowed_domains = ["bayut.com"]
    start_urls = ["https://www.bayut.com/to-rent/property/dubai/"]

    def parse(self, response):
        apartments = response.css('article.ca2f5674')

        for apartment in apartments:
            relative_url = apartment.css('._4041eb80 a ::attr(href)').get()
            property_url = 'https://www.bayut.com' + relative_url
            yield response.follow(property_url,callback=self.parse_property_page)



        next_page = response.css('[title="Next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.bayut.com' + next_page
            yield response.follow(next_page_url,callback=self.parse)

    

    def parse_property_page(self ,response):
        bayut_item=BayutItem()

        
           
        bayut_item['property_id'] = response.css('._033281ab  [aria-label="Reference"]::text').get(),
        bayut_item['purpose'] = response.css('._033281ab  [aria-label="Purpose"]::text').get(),
        bayut_item['type'] = response.css('._033281ab  [aria-label="Type"]::text').get(),
        bayut_item['added_on']= response.css('._033281ab  [aria-label="Reactivated date"]::text').get(),
        bayut_item['furnishing']=  response.css('._033281ab  [aria-label="Furnishing"]::text').get(),
        bayut_item['price']=  {
            'currency' : response.css('.c4fc20ba .e63a6bfb::text').get(),
            'amount' : response.css('.c4fc20ba ._105b8a67::text').get(),
        },
        bayut_item['location' ]=  response.css('._1f0f1758 ::text').get(),
        bayut_item['bed_bath_size']=  {
            'bedrooms' : response.css('[aria-label="Beds"] .fc2d1086::text').get(),
            'bathrooms' : response.css('[aria-label="Baths"] .fc2d1086::text').get(),
            'size' : response.css('.fc2d1086 span::text').get(),
        },
        bayut_item['agent_name' ]=  response.css('._63b62ff2 .f730f8e6::text').get(),
        bayut_item['img_url' ]=  response.css('[aria-label="Property image"] .bea951ad').attrib['src'],
        bayut_item['description' ]=  response.css('._96aa05ec ._2a806e1e ::text').getall(),


        
        yield bayut_item
            
        

