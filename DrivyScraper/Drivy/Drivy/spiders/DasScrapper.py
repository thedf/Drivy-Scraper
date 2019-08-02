import scrapy
from scrapy_splash import SplashRequest
from .. import items
import pymongo
import time
import random
class MySpider(scrapy.Spider):
    name = "DasScrapper"
    start_urls = ["google.com"]
    
    myclient = pymongo.MongoClient("mongodb://root:admin123@localhost:27017/")
    mydb = myclient["admin"]
    mycol = mydb["new_collection"]
    host = "http://olympic.usefixie.com:80"
    username="fixie"
    password = "jFkCP1vhrJtUnfT"
    def __init__(self, *args, **kwargs): 
      super(MySpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')] 

    def start_requests(self):
        """
        This function starts the first request and the first action to do when the script is called.
        So this calls the first url (the search url)
        """
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,args={"wait":3},meta={'proxy':self.host},headers={"Proxy-Authorization" : basic_auth_header(self.username,self.password)})

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
            time.sleep(5)
            #yield scrapy.Request(result, callback=self.parse2)
            yield SplashRequest(url=result, callback=self.parse2,args={"wait":3})
        if (thisPage != numPages):
            argumentForNextPage=self.start_urls[0]+'&page='+str(thisPage+1)
            #time.sleep(10)
            yield SplashRequest(url=argumentForNextPage, callback=self.parse,args={"wait":3})

    def parse2(self, response): 
        """
        this function is called to parse data out of the cars' pages
        """     
        nom_prop = response.xpath('//span[@class="link_no_style js_drk_lnk"]/text()').get()
        
        userProfile = response.xpath('//a[@class="car_owner_section"]/@href').get()
            
        
        isDrivey= response.xpath('//div[@class="car_open_section__icon"]').get()
        if (isDrivey == None):
            isDrivey = False
        else :
            isDrivey = True

        isInstant = response.xpath('//div[@class="cobalt-Pill__Icon"]').get()
        if (isInstant == None):
            isInstant = False
        else :
            isInstant = True
        
        numbrePlaces = response.xpath('//span[@class="car_info_header__attributes"]/text()[3]').get()
        if (numbrePlaces == None):
            numbrePlaces = response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/span/text()[3]').get()
        else :
            numbrePlaces = int(numbrePlaces.split(" ")[0])
        
        price = float(response.xpath('//div[@class="cobalt-text-titleLarge js_price_value"]/text()').get().split("€")[0])

        carName = response.xpath('//h1[@class="car_info_header__title js_car_name"]/text()').get()

        year =  int(response.xpath('//span[@class="car_info_header__attributes"]/text()[2]').get())

        adress = response.xpath('//div[@itemprop="address"]/div/text()').get()

        priaviMinimum = response.xpath('//div[@class="car_owner_restrictions__restriction"]/div/div/text()').get() 
        if (priaviMinimum == None):
             priaviMinimum = response.xpath('//div[@class="car_owner_restrictions__restriction"][2]/div/div/text()').get() 
        if (priaviMinimum == None):
             priaviMinimum = response.xpath('//div[@class="car_owner_restrictions__restriction"][1]/div/div/text()').get() 
        if (priaviMinimum == None):
             priaviMinimum = response.xpath('//div[@class="car_owner_restrictions__restriction"][3]/div/div/text()').get() 
        if (priaviMinimum == None):  
            priaviMinimum = "rien"
        

        motorType = response.xpath('//div[@class="car_technical_features__features_group"][1]/div[1]/p/text()').get()

        counter = response.xpath('//div[@class="car_technical_features__features_group"][1]/div[2]/p/text()').get()

        boite = response.xpath('//div[@class="car_technical_features__features_group"][2]/div/p/text()').get()

        """
        evaluationNumberP = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[3]/div/span/div[2]/div[2]/div/div[2]/div[1]/text()').get()
        if (evaluationNumberP == None):
            evaluationNumberP = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[2]/div/span/div[2]/div[2]/div/div[2]/div[1]/text()').get()
            if (evaluationNumberP == None ):
                evaluationNumberP = 0
            else :
                evaluationNumberP = int (evaluationNumberP)
        else :
            evaluationNumberP = int(evaluationNumberP)
        """

        evaluationNumber = response.xpath('//span[@class="car_card__ratings_count"]/text()').get() 
        if (evaluationNumber == None):
            evaluationNumber = 0
        else :
            evaluationNumber = int(evaluationNumber)
        
        rating = response.xpath('//button[@class="unstyled car_card__ratings car_card__ratings--clickable js_car_card__ratings"]/meta[1]/@content').get() 
        if (rating == None):
            rating = 0.0
        else :
            rating = float(rating)

        accessories = response.xpath('//div[@class="car_show_options__option_content"]/text()').extract()
        mydict = {
                "nom_voiture" : carName ,
                'tarif' : price ,
                'drivy_open': isDrivey,
                'reservation_instantanee': isInstant ,
                'nombre_place':  numbrePlaces ,
                'annees_voiture': year ,
                'nombre_eval':  evaluationNumber ,
                'note': rating ,
                'url_annonce':  response.url,
                'adresse_proximitee': adress ,
                'preavi_minimum': 	priaviMinimum ,
                'moteur': motorType  ,
                'compteur':  counter ,
                'boite': 	 boite ,
                'nom_propriétaire': nom_prop,
                'profile' : userProfile,
                'options_accessoires': accessories
        }
        
        item = items.DrivyItem()
        item['mydict'] = mydict
        request = scrapy.Request("https://www.drivy.com"+userProfile, callback=self.parse3,dont_filter = True)
        request.meta['item'] = item
        yield request 
        #x = self.mycol.insert_one(mydict)
        #yield mydict
        

    def parse3(self, response):
        item = response.meta['item']
        mydict = item['mydict'] 
        yield mydict
