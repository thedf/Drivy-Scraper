from scrapy.crawler import CrawlerProcess
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
    process = CrawlerProcess()
    process.crawl(MySpider,domain=url)
    process.start()


