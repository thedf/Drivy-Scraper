import argparse
import os
from datetime import date
import datetime


CLI=argparse.ArgumentParser()

CLI.add_argument(
  "-places",  # name on the CLI - drop the `--` for positional/required parameters
  nargs="+",  # 0 or more values expected => creates a list
  help='<Required> places',
  default=[],  # default if nothing is provided
)
CLI.add_argument(
  "-init",  # name on the CLI - drop the `--` for positional/required parameters
  type=str,
  help='<Optional> inital date',
  default= str(date. today()+datetime.timedelta(days=1)),  # default if nothing is provided
)
CLI.add_argument(
  "-end",  # name on the CLI - drop the `--` for positional/required parameters
  type=str,
  help='<Optional> final date',
  default= str(date. today()+datetime.timedelta(days=2)),  # default if nothing is provided
)
CLI.add_argument(
  "-file",  # name on the CLI - drop the `--` for positional/required parameters
  type=str,
  help='<Optional> csv file ',
  default= "result",  # default if nothing is provided
)


if __name__ == "__main__":
   #Getting the argument from CLI
   args = CLI.parse_args()

   #For each place call the Scrapper
   for i in args.places :
      url = "https://www.drivy.com/search?address="+"+".join(i.split(" "))+"&address_source=poi&poi_id=685&latitude=48.7254&longitude=2.2596&city_display_name=&start_date="+args.init+"&start_time=09%3A00&end_date="+args.end+"&end_time=09%3A00&country_scope=FR&car_sharing=true&user_interacted_with_car_sharing=false"
      os.system("scrapy crawl DasScrapper -a start_url='"+url+"' -o "+args.file+".csv -t csv")