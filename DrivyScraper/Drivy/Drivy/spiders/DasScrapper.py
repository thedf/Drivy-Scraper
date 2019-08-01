import scrapy
from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):
    name = "DasScrapper"
    lien="https://www.drivy.com/search?address=Gare+de+Massy+-+Palaiseau&address_source=poi&poi_id=685&latitude=48.7254&longitude=2.2596&city_display_name=&start_date=2019-08-03&start_time=09%3A00&end_date=2019-08-04&end_time=09%3A00&country_scope=FR&car_sharing=true&user_interacted_with_car_sharing=false"
    start_urls = [lien]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,args={"wait":3})
    def parse2(self, response):
        yield {'halo':'yo'}
    def parse(self, response):
        content = response.xpath('//*[@id="js_picks"]/div[6]/div/div[2]/div[3]/div/div[2]/div[2]')
        pages=response.xpath('//*[@id="js_search_paginator"]/div/text()').get()
        yield {"page":pages}
        """
        numPages=int(pages.split('sur')[1])
        picks=content.css("div.pick_result")
        result=""
        for pick in picks :
            result="https://www.drivy.com/"+pick.css("a").attrib['href']
            scrapy.Request(result, callback=self.parse2)
        for i in range(1,numPages):
            argumentForNextPage=self.lien+'&page='+str(i+1)
            yield scrapy.Request(argumentForNextPage, callback=self.parse)
        """