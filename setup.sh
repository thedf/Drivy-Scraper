curl -O https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
bash Anaconda3-5.0.1-Linux-x86_64.sh
source ~/.bashrc
conda create --name Scrap python=3
source activate Scrap
conda install -c conda-forge scrapy
pip install scrapy-fake-useragent
pip install scrapy_splash
pip install pymongo
pip install argparse
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
sudo docker pull scrapinghub/splash
sudo docker run -p 8050:8050 scrapinghub/splash
