#!/bin/bash

sudo add-apt-repository ppa:nilarimogard/webupd8 && sudo apt update &&
sudo apt install streamlink && sudo add-apt-repository ppa:mc3man/mpv-tests &&
sudo apt remove mpv && sudo apt autoremove && pip install -r requirements.txt
