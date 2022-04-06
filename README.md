# Pebolmax

## __

### [installing dependencies]
- python 
- streamlink - cli utility for pipe video streams
- mpv - supported video player 

#### [ubuntu]
Installing dependencies manually

Installing streamlink
 $ sudo add-apt-repository ppa:nilarimogard/webupd8 && sudo apt update && sudo apt install streamlink

Installing mpv
 $ sudo add-apt-repository ppa:mc3man/mpv-tests && sudo apt remove mpv && sudo apt autoremove
 
Installing python dependencies:
 $ pip install -r requirements.txt
 
 or
 
 $ ./install.sh

#### [arch]

### [how to use]

Run 
  $ python run.py

### [changelog]
v1.0 - only supports futemax live games and mpv player
