from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from spiders.DasScrapper import MySpider
import sys, getopt


def getArgs(argv):
   try:
      opts, args = getopt.getopt(argv,"hu:",["Url="])
   except getopt.GetoptError:
      print ('python run.py -u <Url>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('python run.py -mg <mongodb://user:pwd@ip:port/> -db <Database> -c <Collection> -u <Url>')
         sys.exit()
      elif opt in ("-u", "--Url"):
         url = arg
   return url

if __name__ == "__main__":
    url=getArgs(sys.argv[1:])
    spider = MySpider(domain=url)
    crawler = Crawler()
    crawler.crawl(spider)
    crawler.start()
    reactor.run() # the script will block here


