#!/bin/bash

sudo add-apt-repository ppa:nilarimogard/webupd8 && sudo apt update &&
sudo apt -y install streamlink && sudo add-apt-repository ppa:mc3man/mpv-tests &&
sudo apt -y install mpv && pip install -r requirements.txt
