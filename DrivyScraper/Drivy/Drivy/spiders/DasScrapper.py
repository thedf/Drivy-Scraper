import scrapy
from scrapy_splash import SplashRequest
from .. import items
import pymongo
import time
import random
import pkgutil
from w3lib.http import basic_auth_header
class MySpider(scrapy.Spider):
    name = "DasScrapper"
    start_urls = ["google.com"]
    
    myclient = pymongo.MongoClient("mongodb://root:admin123@localhost:27017/")
    mydb = myclient["admin"]
    mycol = mydb["new_collection"]
    
    def __init__(self, *args, **kwargs): 
      super(MySpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')] 
      self.LUA_SOURCE = pkgutil.get_data(
            'Drivy', 'scripts/crawlera.lua'
        ).decode('utf-8')
      self.LUA_SOURCE_CAR = pkgutil.get_data(
            'Drivy', 'scripts/crawleraCar.lua'
        ).decode('utf-8')

    def start_requests(self):
        """
        This function starts the first request and the first action to do when the script is called.
        So this calls the first url (the search url)
        """
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,
                        endpoint='execute',
                        args={
                            'lua_source': self.LUA_SOURCE,
                            'timeout': 3600
                        },
                        # tell Splash to cache the lua script, to avoid sending it for every request
                        cache_args=['lua_source']
                    )

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
            yield SplashRequest(url=result, callback=self.parse2,
                        endpoint='execute',
                        args={
                            'lua_source': self.LUA_SOURCE_CAR,
                            'timeout': 3600
                        },
                        # tell Splash to cache the lua script, to avoid sending it for every request
                        cache_args=['lua_source']
                    )
        if (thisPage != numPages):
            argumentForNextPage=self.start_urls[0]+'&page='+str(thisPage+1)

            yield SplashRequest(url=argumentForNextPage, callback=self.parse,
                        endpoint='execute',
                        args={
                            'lua_source': self.LUA_SOURCE,
                            'timeout': 3600
                        },
                        # tell Splash to cache the lua script, to avoid sending it for every request
                        cache_args=['lua_source']
                    )
                    
        #yield {"content":response.body.decode("utf-8")}
    def parse2(self, response): 
        """
        this function is called to parse data out of the cars' pages
        """     
        nom_prop = response.xpath('//span[@class="link_no_style js_drk_lnk"]/text()').get()
        if (nom_prop == None):
            yield {"content":response.body.decode("utf-8")}

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
        
        price = response.xpath('//div[@class="cobalt-text-titleLarge js_price_value"]/text()').get()
        if (price == None):
            price = float(response.xpath('//div[@class="js_default_price"]/span/text()').get().split("€")[0])
            
        else :
            price = float(price.split("€")[0])

        carName = response.xpath('//h1[@class="car_info_header__title js_car_name"]/text()').get()

        year =  int(response.xpath('//span[@class="car_info_header__attributes"]/text()[2]').get())

        adress = response.xpath('//div[@itemprop="address"]/div/text()').get()

        priaviMinimumList = response.xpath('//div[@class="car_owner_restrictions__restriction"]')
        priaviMinimum = None
        for divPriavi in priaviMinimumList :
            if (divPriavi == None):
                pass
            elif ("Préavis" in divPriavi):
                priaviMinimum = divPriavi.xpath('./div/div/text()').get()
        if (priaviMinimum == None):  
            priaviMinimum = "rien"
            
        motorType = response.xpath('//div[@class="car_technical_features__features_group"][1]/div[1]/p/text()').get()

        counter = response.xpath('//div[@class="car_technical_features__features_group"][1]/div[2]/p/text()').get()

        boite = response.xpath('//div[@class="car_technical_features__features_group"][2]/div/p/text()').get()

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
                'preavi_minimum': 	priaviMinimum.strip() ,
                'moteur': motorType  ,
                'compteur':  counter ,
                'boite': 	 boite ,
                'nom_propriétaire': nom_prop,
                'options_accessoires': accessories
        }
        
        item = items.DrivyItem()
        item['mydict'] = mydict
        request = scrapy.Request("https://www.drivy.com"+userProfile, callback=self.parse3,dont_filter = True)
        request.meta['proxy'] = "e49ba384b4e94d04bef21798f0bdc5e4:@proxy.crawlera.com:8010"
        request.meta['item'] = item
        yield request 
        #yield mydict
        

    def parse3(self, response):
        item = response.meta['item']
        mydict = item['mydict'] 
        dateCreation = response.xpath('//div[@class="cobalt-Card user_card cobalt-mb"]/div[3]/div/text()').get()
        if (dateCreation == None ):
            dateCreation = "00/00/00"
        else :
            dateCreation = dateCreation.split(' ')[3].strip()

        rentalsNumber = response.xpath('//div[@class="cobalt-Card user_card cobalt-mb"]/div[2]/div/div[1]/div[1]/text()[2]').get()
        if (rentalsNumber == None):
            rentalsNumber = 0
        else :
            rentalsNumber = int(rentalsNumber)
        
        ratingProp = response.xpath('//div[@class="col-sm-4 col-xs-12 no-outer-gutter-xs"]/div/div[2]/div/div[2]/div[1]/span[1]/text()').get()
        if (ratingProp == None):
            ratingProp = 0.0
        else :
            ratingProp = float(ratingProp)
            
        evaluationNumberP =response.xpath('//div[@class="col-sm-4 col-xs-12 no-outer-gutter-xs"]/div/div[2]/div/div[2]/div[2]/text()').get()
        if (evaluationNumberP == None):
            evaluationNumberP = 0
        elif ("Une évaluation" in evaluationNumberP.strip() ):
            evaluationNumberP = 1
        else :
            evaluationNumberP = int(evaluationNumberP.split(' ')[0].strip())
         

        mydict['nombre_location_proprio'] = rentalsNumber
        mydict['date_debut_loc_proprio']  = dateCreation
        mydict['note_proprio']  = ratingProp
        mydict['nombre_eval_proprio']  = evaluationNumberP
        x = self.mycol.insert_one(mydict)
        #yield {"sucess" : mydict['url_annonce']}
        yield mydict
