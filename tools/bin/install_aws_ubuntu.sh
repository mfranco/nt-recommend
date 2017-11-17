#!/bin/bash
sudo apt-get install python3-matplotlib -y
sudo apt-get install python3-pip -y
sudo apt-get install git build-essential htop g++ gcc vim libssl-dev libffi-dev python3-dev  -y
sudo python3 -m nltk.downloader all
sudo pip3 install -r ~/src/nt-recommend/tools/requirements/base.txt
