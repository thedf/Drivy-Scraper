from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
from spiders.DasScrapper import MySpider
import sys, getopt


def getArgs(argv):
   try:
      opts, args = getopt.getopt(argv,"hmg:db:c:u:",["mongoDB=","Database=","Collection=","Url="])
   except getopt.GetoptError:
      print ('python run.py -mg <mongodb://user:pwd@ip:port/> -db <Database> -c <Collection> -u <Url>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('python run.py -mg <mongodb://user:pwd@ip:port/> -db <Database> -c <Collection> -u <Url>')
         sys.exit()
      elif opt in ("-mg", "--mongoDB"):
         usmongodber = arg
      elif opt in ("-db", "--Database"):
         database = arg
      elif opt in ("-c", "--Collection"):
         collection = arg
      elif opt in ("-u", "--Url"):
         url = arg
   return url,mongodb,database,collection


if __name__ == "__main__":
    url,mongodb,database,collection=getArgs(sys.argv[1:])
    spider = MySpider(domain=url,mongodb=mongodb,db=database,collection=collection)
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run() # the script will block here


