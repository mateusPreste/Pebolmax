#!/bin/bash

sudo add-apt-repository -y ppa:nilarimogard/webupd8  &&
sudo apt -y install streamlink && sudo add-apt-repository -y ppa:mc3man/mpv-tests &&
sudo apt-get install python3-gi gir1.2-wnck-3.0 &&
sudo apt -y install mpv && pip install -r requirements.txt
