from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from spiders.DasScrapper import MySpider
from scrapy.utils.project import get_project_settings
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
    process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
   })
    process.crawl(spider)
    process.start()


