import sys
import os

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
   os.system("scrapy crawl DasScrapper --a start_url='"+url+"'")


