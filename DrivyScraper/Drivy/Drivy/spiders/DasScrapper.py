import scrapy
from scrapy_splash import SplashRequest
from .. import items
import pymongo
import pkgutil


class MySpider(scrapy.Spider):
    """
    This is the spider that crawls the pages
    """
    #Initial naming and declarations will change by the init function
    name = "DasScrapper"
    start_urls = ["google.com"]
    
    #MongoDB Credentials
    myclient = pymongo.MongoClient("mongodb://root:admin123@localhost:27017/")
    mydb = myclient["admin"]
    mycol = mydb["new_collection"]
    
    def __init__(self, *args, **kwargs): 
        """
        Initialse the class : Getting the Lua Scripts for the proxy and the urls
    
        Args:
        start_url : list of urls
        Returns:
        self.start_urls     : the urls that gets crawled (the first url)
        self.LUA_SOURCE     : this the lua script for the proxy for search pages (needs 15 secs for JS to load)
        self.LUA_SOURCE_CAR : this the lua script for the proxy for search pages (only needs 1 sec for JS to load)
        """
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
    
        Args:
        start_url : list of urls
        Returns:
        Requests     : calls Splash Requests to parse the search url
        """
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parseSearchPage,
                        endpoint='execute',
                        args={
                            'lua_source': self.LUA_SOURCE,
                            'timeout': 3600
                        },
                        # tell Splash to cache the lua script, to avoid sending it for every request
                        cache_args=['lua_source']
                    )

    def parseSearchPage(self, response):
        """
        This is the parse function for the search url request.This looks for the number of pages and requests parse function for all 
        the pages .Also scraping car pages urls and calls the parse function for the Car pages.
    
        Args:
        response     : response from the Initial url call
        Returns:
        Requests     : calls Splash Requests to parse all the other pages and car pages
        """
        content = response.xpath('//*[@id="js_picks"]/div[6]/div/div[2]/div[3]/div/div[2]/div[2]')
        pages=response.xpath('//*[@id="js_search_paginator"]/div/text()').get()
        pageSplit=pages.split(' ')
        
        #Parsing the the page number of the page being crawled and how many pages there are in this search
        numPages=int(pageSplit[3])
        thisPage=int(pageSplit[1])
        
        #Getting urls of cars' pages 
        picks=content.css("div.pick_result")
        result=""
        for pick in picks :
            result="https://www.drivy.com"+pick.css("a").attrib['href']
            
            #Calling request for every Car page
            yield SplashRequest(url=result, callback=self.parseCarPages,
                        endpoint='execute',
                        args={
                            'lua_source': self.LUA_SOURCE_CAR,
                            'timeout': 3600
                        },
                        # tell Splash to cache the lua script, to avoid sending it for every request
                        cache_args=['lua_source']
                    )

        #If this isn't the last page call a request for the next page
        if (thisPage != numPages):
            argumentForNextPage=self.start_urls[0]+'&page='+str(thisPage+1)

            yield SplashRequest(url=argumentForNextPage, callback=self.parseSearchPage,
                        endpoint='execute',
                        args={
                            'lua_source': self.LUA_SOURCE,
                            'timeout': 3600
                        },
                        # tell Splash to cache the lua script, to avoid sending it for every request
                        cache_args=['lua_source']
                    )
                    
        #yield {"content":response.body.decode("utf-8")}

    def parseCarPages(self, response): 
        """
        this function is called to parse data out of the cars' pages and call the user page request to complete the required infos.
    
        Args:
        response     : response from the Car page request
        Returns:
        Requests     : calls Requests to parse user infos
        myDict       : Dictionary containing all infos that can be parsed from Car page
        """

        #Getting the name of the owner 
        nom_prop = response.xpath('//span[@class="link_no_style js_drk_lnk"]/text()').get()

        #Getting the url for the user page to call the request 
        userProfile = response.xpath('//a[@class="car_owner_section"]/@href').get()
            
        #Check if the Drivy Open is True or not
        isDrivey= response.xpath('//div[@class="car_open_section__icon"]').get()
        if (isDrivey == None):
            isDrivey = False
        else :
            isDrivey = True

        #Check if the reservation is instant
        isInstant = response.xpath('//div[@class="cobalt-Pill__Icon"]').get()
        if (isInstant == None):
            isInstant = False
        else :
            isInstant = True
        
        """
        The number of places can be in two tags of the HTML (this happens for most of the info) due to lacking of 
        some infos in some of the car pages so the html tags slightly shift. But the code can handle all the changes.
        """
        numbrePlaces = response.xpath('//span[@class="car_info_header__attributes"]/text()[3]').get()
        if (numbrePlaces == None):
            numbrePlaces = response.xpath('//*[@id="js_car_id"]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/div/span/text()[3]').get()
        else :
            numbrePlaces = int(numbrePlaces.split(" ")[0])
        
        #Getting the price from the 2 possible tags
        price = response.xpath('//div[@class="cobalt-text-titleLarge js_price_value"]/text()').get()
        if (price == None):
            price = float(response.xpath('//div[@class="js_default_price"]/span/text()').get().split("€")[0])
        else :
            price = float(price.split("€")[0])

        #Getting the name of the car 
        carName = response.xpath('//h1[@class="car_info_header__title js_car_name"]/text()').get()

        #Getting the year of the car
        year =  int(response.xpath('//span[@class="car_info_header__attributes"]/text()[2]').get())

        #Getting the address of the car's owner
        adress = response.xpath('//div[@itemprop="address"]/div/text()').get()

        """
        For the Préavis minimum there exists a bloc that can be sometimes empty so we will return "rien"
        Or the Préavis minimum if it exists it can be one of the 3 options Ergo this process to find it
        """
        priaviMinimumList = response.xpath('//div[@class="car_owner_restrictions__restriction"]')
        priaviMinimum = None
        for divPriavi in priaviMinimumList :
            if (divPriavi == None):
                pass
            elif ("Préavis" in divPriavi.get()):
                priaviMinimum = divPriavi.xpath('./div/div/text()').get()
        if (priaviMinimum == None):  
            priaviMinimum = "rien"
        
        #Getting the motor type of the car
        motorType = response.xpath('//div[@class="car_technical_features__features_group"][1]/div[1]/p/text()').get()

        #Getting the counter number of the car
        counter = response.xpath('//div[@class="car_technical_features__features_group"][1]/div[2]/p/text()').get()

        #Getting the type of the switching mechanism of the car
        boite = response.xpath('//div[@class="car_technical_features__features_group"][2]/div/p/text()').get()
        
        #Getting how many evaluations the car has (Not the User ,the user's is scrapped later)
        evaluationNumber = response.xpath('//span[@class="car_card__ratings_count"]/text()').get() 
        if (evaluationNumber == None):
            evaluationNumber = 0
        else :
            evaluationNumber = int(evaluationNumber)
        
        #Getting the rating out of 5 of the car (Not the User ,the user's is scrapped later)
        rating = response.xpath('//button[@class="unstyled car_card__ratings car_card__ratings--clickable js_car_card__ratings"]/meta[1]/@content').get() 
        if (rating == None):
            rating = 0.0
        else :
            rating = float(rating)
        
        #Getting all the accessories of the car
        accessories = response.xpath('//div[@class="car_show_options__option_content"]/text()').extract()

        #Froming the dictionary of the infos scrapped from car's page
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
        
        #This item manoeuver is to pass the dictionary to the user's page as an argument so we can add other parameters
        item = items.DrivyItem()
        item['mydict'] = mydict

        #Forming and calling the request, This request doesn't need to be SplashRequest because we don't need any JS to load
        request = scrapy.Request("https://www.drivy.com"+userProfile, callback=self.parseUserPage,dont_filter = True)
        request.meta['proxy'] = "e49ba384b4e94d04bef21798f0bdc5e4:@proxy.crawlera.com:8010"
        request.meta['item'] = item
        yield request 
        

    def parseUserPage(self, response):
        """
        this function is called to parse data out of the users' pages to complete myDict and upload myDict to MongoDB.
    
        Args:
        response     : response from the user page
        Returns:
        success      : sends a sucess json with url to confirm that the data has been parsed successfully
        """

        #Loading the dictionary from the car's request
        item = response.meta['item']
        mydict = item['mydict'] 

        #Getting the date of Creation of the account of the user
        #Some users don't show their date so the value "00/00/0000" is passed instead
        dateCreation = response.xpath('//div[@class="cobalt-Card user_card cobalt-mb"]/div[3]/div/text()').get()
        if (dateCreation == None ):
            dateCreation = "00/00/0000"
        else :
            dateCreation = dateCreation.split(' ')[3].strip()

        #Getting how many cars the user rented 
        #Some users don't show their rental numbers so the value 0 is assumed and passed instead
        rentalsNumber = response.xpath('//div[@class="cobalt-Card user_card cobalt-mb"]/div[2]/div/div[1]/div[1]/text()[2]').get()
        if (rentalsNumber == None):
            rentalsNumber = 0
        else :
            rentalsNumber = int(rentalsNumber)
        
        #Getting the rating of the user 
        #Some users don't show their rating so the value 0.0 is assumed and passed instead
        ratingProp = response.xpath('//div[@class="col-sm-4 col-xs-12 no-outer-gutter-xs"]/div/div[2]/div/div[2]/div[1]/span[1]/text()').get()
        if (ratingProp == None):
            ratingProp = 0.0
        else :
            ratingProp = float(ratingProp)
        
        #Getting the evaluation Number of the user 
        #Some users don't show their evaluation Number so the value 0 is assumed and passed instead

        evaluationNumberP =response.xpath('//div[@class="col-sm-4 col-xs-12 no-outer-gutter-xs"]/div/div[2]/div/div[2]/div[2]/text()').get()
        if (evaluationNumberP == None):
            evaluationNumberP = 0
        elif ("Une évaluation" in evaluationNumberP.strip() ):
            evaluationNumberP = 1
        else :
            evaluationNumberP = int(evaluationNumberP.split(' ')[0].strip())
         
        #Loading the infos parssed from user's page to the dictionary
        mydict['nombre_location_proprio'] = rentalsNumber
        mydict['date_debut_loc_proprio']  = dateCreation
        mydict['note_proprio']  = ratingProp
        mydict['nombre_eval_proprio']  = evaluationNumberP

        #Dumping the Dictionary in the MongoDB 
        x = self.mycol.insert_one(mydict)

        #Printing a sucess json into output for Logging (this isn't sent to the DB)
        yield {"sucess" : mydict['url_annonce']}
