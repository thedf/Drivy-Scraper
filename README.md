# Scrap


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Latest Anaconda
Docker
```
for ubuntu installing anaconda is like the following

```
curl -O https://repo.continuum.io/archive/Anaconda3-2019.07-Linux-x86_64.sh
bash Anaconda3-2019.07-Linux-x86_64.sh
source ~/.bashrc
```
more on this url
https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-16-04

for ubuntu installing docker is like the following

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
```
more in this url
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04

### Installing

A step by step series of examples that tell you how to get a development env running

First you should create an anaconda env

```
conda create --name Scrap python=3
```
and then activate the env

```
source activate Scrap
```
or 
```
conda activate Scrap
```

then install scrapy 

```
conda install -c conda-forge scrapy
```

the install few packages in need 

```
pip install scrapy-fake-useragent
pip install scrapy_splash
pip install pymongo
pip install argparse
```

## Running the docker

In order for the Splash to work :
Open a new shell into the server (a terminal locally) and run 

```
sudo docker pull scrapinghub/splash
sudo docker run -p 8050:8050 scrapinghub/splash --max-timeout 3600
```
and then close the terminal/shell

To get the code 

```
git clone https://github.com/SEOUTE/Scrap.git
```

### Running the code
To run the code get in the folder you excuted the git command from
```
cd Scrap/DrivyScraper/Drivy/Drivy/
```
and then activate the env

```
source activate Scrap
```
or 
```
conda activate Scrap
```
and run the script 
```
python run.py -places "Gare de Massy - Palaiseau" "Paris"
```
if the script isn't excutable try 
```
chmod +x run.py
```
### To change MongoDB Database

go to Scrap/DrivyScraper/Drivy/Drivy/spiders/DasScrapper.py
and change the line :
```
#MongoDB Credentials
myclient = pymongo.MongoClient("mongodb://root:admin123@localhost:27017/")
mydb = myclient["admin"]
mycol = mydb["new_collection"]
```
### To change Proxy user
if you ever change the user from the proxy :
go to Scrap/DrivyScraper/Drivy/Drivy/spiders/DasScrapper.py line 236
```
request.meta['proxy'] = "e49ba384b4e94d04bef21798f0bdc5e4:@proxy.crawlera.com:8010"
```

"e49ba384b4e94d04bef21798f0bdc5e4" is the API from Crawlera

go to  Scrap/DrivyScraper/Drivy/Drivy/scripts/crawlera.lua and
Scrap/DrivyScraper/Drivy/Drivy/scripts/crawleraCar.lua line 4
and change :
```
local user = "e49ba384b4e94d04bef21798f0bdc5e4"
```
