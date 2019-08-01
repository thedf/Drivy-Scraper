import scrapy
from scrapy_splash import SplashRequest
import time
class MySpider(scrapy.Spider):
    name = "DasScrapper"
    lien="https://www.drivy.com/search?address=Gare+de+Massy+-+Palaiseau&address_source=poi&poi_id=685&latitude=48.7254&longitude=2.2596&city_display_name=&start_date=2019-08-03&start_time=09%3A00&end_date=2019-08-04&end_time=09%3A00&country_scope=FR&car_sharing=true&user_interacted_with_car_sharing=false"
    start_urls = [lien]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,args={"wait":3})
    def parse2(self, response):        
        yield {
                "nom_voiture" : response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/h1/text()').get() ,
                'tarif' : response.xpath('//*[@id="request_form"]/div[2]/div/div[1]/div[2]/span/text()').get() ,
                'drivy_open	': response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[1]/div/div/div[2]/div[1]/text()').get() ,
                'reservation_instantanee	': response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[2]/div/div[1]/div/text()').get() ,
                'nombre_place':  response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/span/text()[3]').get() ,
                'annees_voiture':  response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/span/text()[2]').get() ,
                'nombre_eval':  response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/button/span/text()').get() ,
                'note': 	 response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/button/meta[1]/@content').get() ,
                'url_annonce':  response.url,
                'adresse_proximitee':  response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/div/text()').get() ,
                'preavi_minimum': 	 response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[5]/div/div[2]/div[1]/div/div/div/text()').get() ,
                'moteur':  response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[5]/div[1]/div/div/div[2]/div[1]/div[1]/p/text()').get() ,
                'compteur':  response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[5]/div[1]/div/div/div[2]/div[1]/div[2]/p/text()').get() ,
                'boite': 	 response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[5]/div[1]/div/div/div[2]/div[2]/div/p/text()').get() ,
                'nom_propriétaire':  response.css("#js_car_id > div.container > div:nth-child(1) > div.col-md-8.col-sm-7.col-xs-12.no-outer-gutter-xs > div:nth-child(8) > div > span > div:nth-child(2) > div.cobalt-text-titleTiny > span > span::text").get() ,
                'Nom 2':  response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[2]/div/span/div[2]/div[1]/span/span/text()').get(),
                'nombre_eval_proprio':  response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[3]/div/span/div[2]/div[2]/div/div[2]/div[1]/text()').get() ,
                'note_proprio': response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[3]/div/span/div[2]/div[2]/div/div[1]/text()').get() ,
        }
    def parse(self, response):
        content = response.xpath('//*[@id="js_picks"]/div[6]/div/div[2]/div[3]/div/div[2]/div[2]')
        pages=response.xpath('//*[@id="js_search_paginator"]/div/text()').get()
        pageSplit=pages.split(' ')
        numPages=int(pageSplit[3])
        thisPage=int(pageSplit[1])
        picks=content.css("div.pick_result")
        result=""
        for pick in picks :
            result="https://www.drivy.com"+pick.css("a").attrib['href']
            time.sleep(2)
            yield scrapy.Request(result, callback=self.parse2)
            #yield SplashRequest(url=result, callback=self.parse2,args={"wait":3})
        if (thisPage != numPages):
            argumentForNextPage=self.lien+'&page='+str(thisPage+1)
            time.sleep(60)
            yield SplashRequest(url=argumentForNextPage, callback=self.parse,args={"wait":3})

