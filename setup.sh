sudo apt install docker.io
sudo docker pull scrapinghub/splash
sudo docker run -p 8050:8050 scrapinghub/splash
pip install scrapy-fake-useragent