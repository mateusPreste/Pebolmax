import threading
import os

from sportsonline import SportsOnline
from cloudflare import CloudFlareHandler
from videoThreads import videoThread
from playertv import PlayerTV
from redecanais import RedeCanais
from embedflix import Embedflix

import subprocess
import time
class terminalThread(threading.Thread):
    def __init__(self, source, olink):
        threading.Thread.__init__(self)
        self.source = source
        self.olink = olink
        self.ip = None
    
    def selectSource(self, source, link) -> list[str]:
        link = link.replace(' ', '')
        if(source == 'embedflix'):
            handler = Embedflix(link)
            return handler.getLink()
        elif(source == 'v3.sportsonline.sx'):
            handler = SportsOnline(link)
            return handler.getLink()
        elif(source == 'youtube.com'):
            link = link.replace(' ', '').replace('\'', '')
            return [link, '']
        elif(source == 'cloudflarestream'):
            handler = CloudFlareHandler(link)
            return handler.getLink()
        elif(source == 'playertv'):
            handler = PlayerTV(link)
            return handler.getLink()
        elif(source == 'sinalpublico'):
            handler = RedeCanais(link)
            return handler.getLink()
        
        print('Essa fonte não é suportada')
        raise RuntimeError('This source is not supported')
    
    def poolLink(self):
        with open(self.thread.output.name, 'r') as r:
            for line in r:
                if('127.0.0.1' in line and self.ip == None):
                    self.ip = line.replace('[cli][info]  ', '')
                    subprocess.Popen(f'gridplayer {self.ip}', shell=True)
    
    def run(self):
        try:
            #print('Gathering from', self.source, self.olink)
            [videoUrl, originUrl] = self.selectSource(self.source, self.olink)
            #print('get video url', videoUrl, originUrl)
            self.thread = videoThread(videoUrl, originUrl)
            self.thread.start()
            
            while(self.ip == None):
                time.sleep(1)
                self.poolLink()
                
        except Exception:
            print('Fail')
        
