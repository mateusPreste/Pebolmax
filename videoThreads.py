import threading
import os
import configparser

from subprocess import Popen, PIPE, STDOUT

import subprocess

import tempfile

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')
    
class videoThread (threading.Thread):
    def __init__(self, endpoint, origin):
        threading.Thread.__init__(self)
        self.endpoint = endpoint
        self.origin = origin

        self.config = configparser.ConfigParser()
        self.config.read('settings.conf')
        self.subprocess = None
        self.output = tempfile.NamedTemporaryFile()
        self.errout = tempfile.NamedTemporaryFile()
        self.ip = None
    
    def interpreter(self, line):
        command = os.system(f'cmd /c "{line}"')
        return command    
    
    def mode(self):
        address = self.config['proxy']['address']
        port = self.config['proxy']['port']
        mode = str(self.config['player']['playerMode'])

        self.proxy = ''
#        f'--http-proxy \"http://{address}:{port}\"'
        
        if(mode == 'playerpass'):
            myplayer = self.config['player']['mainPlayer']
            return f'{self.proxy} --player-passthrough \'https\' --player \'{myplayer}\''
        elif(mode == 'player'):
            myplayer = self.config['player']['mainPlayer']
            return f'{self.proxy} --hls-live-edge=1  --player {myplayer}'
        elif(mode == 'http'):
            return f'{self.proxy} --hls-live-edge=1 --stream-segment-threads 5 --player-external-http'
    
    def run(self):
        cmd = f'streamlink \'{self.endpoint}\' best --http-header \'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0\' \
            --http-header \'Accept= */*\' \
            --http-header \'Accept-Language= en-US,en;q=0.5\' \
            --http-header \'Accept-Encoding= gzip, deflate, br\' \
            --http-header \'Origin= {self.origin}\' \
            --http-header \'Sec-Fetch-Dest= empty\' \
            --http-header \'Sec-Fetch-Mode= cors\' \
            --http-header \'Sec-Fetch-Site= cross-site\' \
            --http-header \'Referer= {self.origin}/\' \
            --http-header \'DNT= 1\' \
            --http-header \'Connection= keep-alive\' \
            --http-header \'Pragma= no-cache\' \
            --http-header \'Cache-Control= no-cache\' {self.mode()}'
            
        if(self.origin==''):
            cmd = f'gridplayer \"$(yt-dlp --get-url --format best \'{self.endpoint}\')\"'

        #print(cmd)

        if os.name == 'nt':
            self.interpreter(cmd.replace("\'", "\"").replace('&', '^&'))
        else:
            #os.system(cmd)
            #print('cmd', cmd)
            
            self.subprocess = Popen(cmd, stdout=self.output, stderr=self.errout, shell=True)