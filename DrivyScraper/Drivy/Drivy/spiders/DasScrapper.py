import scrapy
from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):
    name = "DasScrapper"

    start_urls = ["https://www.drivy.com/search?address=Gare+de+Massy+-+Palaiseau&address_source=poi&poi_id=685&latitude=48.7254&longitude=2.2596&city_display_name=&start_date=2019-08-03&start_time=09%3A00&end_date=2019-08-04&end_time=09%3A00&country_scope=FR&car_sharing=true&user_interacted_with_car_sharing=false"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,args={"wait":3})

    def parse(self, response):
        content = response.xpath('//*[@id="js_picks"]/div[6]/div/div[2]/div[3]/div/div[2]/div[2]')
        picks=content.css("div.pick_result")
        result=""
        for pick in picks :
            result+=pick.css("a").get()
        yield {'article': ''.join(result)}