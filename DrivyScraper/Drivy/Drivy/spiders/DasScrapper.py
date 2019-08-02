import scrapy
from scrapy_splash import SplashRequest
import pymongo
import time
class MySpider(scrapy.Spider):
    name = "DasScrapper"
    start_urls = ["google.com"]
    
    myclient = pymongo.MongoClient("mongodb://root:admin123@localhost:27017/")
    mydb = myclient["admin"]
    mycol = mydb["new_collection"]

    def __init__(self, *args, **kwargs): 
      super(MySpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')] 

    def start_requests(self):
        """
        This function starts the first request and the first action to do when the script is called.
        So this calls the first url (the search url)
        """
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,args={"wait":3})
    def parse2(self, response): 
        """
        this function is called to parse data out of the cars' pages
        """     
        nom_prop =    response.css("#js_car_id > div.container > div:nth-child(1) > div.col-md-8.col-sm-7.col-xs-12.no-outer-gutter-xs > div:nth-child(8) > div > span > div:nth-child(2) > div.cobalt-text-titleTiny > span > span::text").get() 
        if (nom_prop == None):
            nom_prop = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[2]/div/span/div[2]/div[1]/span/span/text()').get()
        
        
        userProfile = response.xpath("//a[contains(@class,'car_owner_section')]").attrib['href']
        
        isDrivey= response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[1]/div/div/div[2]/div[1]/text()').get()
        if (isDrivey == None):
            isDrivey = False
        else :
            isDrivey = True

        isInstant = response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[2]/div/div[1]/div/text()').get()
        if (isInstant == None):
            isInstant = False
        else :
            isInstant = True
        
        numbrePlaces = int(response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/span/text()[3]').get().split(" ")[0])
        
        price = float(response.xpath('//*[@id="request_form"]/div[2]/div/div[1]/div[2]/span/text()').get().split("€")[0])

        carName = response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/h1/text()').get()

        year =  int(response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/span/text()[2]').get())

        adress = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/div/text()').get()
        if (adress == None):
            adress = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/div/text()').get()

        priaviMinimum = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[5]/div/div[2]/div[1]/div/div/div/text()').get() 
        if (priaviMinimum == None):
             priaviMinimum = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[3]/div/div[2]/div[1]/div[2]/div/div/text()').get() 
        if (priaviMinimum == None):
            priaviMinimum = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/text()').get()
        if (priaviMinimum == None):
            priaviMinimum = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[4]/div/div[2]/div[1]/div/div/div/text()').get()
        if (priaviMinimum == None):
            priaviMinimum = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[3]/div/div[2]/div/div/div/div/text()').get()
        if (priaviMinimum == None):
            priaviMinimum = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[4]/div/div[2]/div/div/div/div/text()').get()
        if (priaviMinimum == None):  
            priaviMinimum = "rien"
        

        motorType = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[5]/div[1]/div/div/div[2]/div[1]/div[1]/p/text()').get()
        if (motorType == None):
            motorType = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[4]/div[1]/div/div/div[2]/div[1]/div[1]/p/text()').get()
        if (motorType == None):
            motorType = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[6]/div[1]/div/div/div[2]/div[1]/div[1]/p/text()').get()
        
        counter = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[5]/div[1]/div/div/div[2]/div[1]/div[2]/p/text()').get()
        if (counter == None):
            counter = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[4]/div[1]/div/div/div[2]/div[1]/div[2]/p/text()').get()
        if (counter == None):
            counter = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[6]/div[1]/div/div/div[2]/div[1]/div[2]/p/text()').get()
        
        boite = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[5]/div[1]/div/div/div[2]/div[2]/div/p/text()').get()
        if (boite == None):
            boite =response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[4]/div[1]/div/div/div[2]/div[2]/div/p/text()').get()
        if (boite == None):
            boite =response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[6]/div[1]/div/div/div[2]/div[2]/div/p/text()').get()
        

        evaluationNumberP = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[3]/div/span/div[2]/div[2]/div/div[2]/div[1]/text()').get()
        if (evaluationNumberP == None):
            evaluationNumberP = response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[2]/div/span/div[2]/div[2]/div/div[2]/div[1]/text()').get()
            if (evaluationNumberP == None ):
                evaluationNumberP = 0
            else :
                evaluationNumberP = int (evaluationNumberP)
        else :
            evaluationNumberP = int(evaluationNumberP)
        
        evaluationNumber = response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/button/span/text()').get() 
        if (evaluationNumber == None):
            evaluationNumber = response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/button/span/text()').get()
            if (evaluationNumber == None ):
                evaluationNumber = 0
            else :
                evaluationNumber = int (evaluationNumber)
        else :
            evaluationNumber = int(evaluationNumber)
        
        rating = response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/button/meta[1]/@content').get() 
        if (rating == None):
            rating = response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/button/meta[1]/@content').get()
            if (rating == None):
                rating = 0
            else :
                rating = float(rating)
        else :
            rating = float(rating)

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
                'nombre_eval_proprio': evaluationNumberP ,
                'note_proprio': response.xpath('//*[@id="js_car_id"]/div[3]/div[1]/div[1]/div[3]/div/span/div[2]/div[2]/div/div[1]/text()').get() ,
                'profileUrl' : userProfile
        }
        #item = MyItem()
        #item['dic'] = mydict
        #yield scrapy.Request(result, callback=self.parse2)
        #x = self.mycol.insert_one(mydict)
        yield mydict
        
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
            argumentForNextPage=self.start_urls[0]+'&page='+str(thisPage+1)
            time.sleep(60)
            yield SplashRequest(url=argumentForNextPage, callback=self.parse,args={"wait":3})

