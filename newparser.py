import PyChromeDevTools
import time

import subprocess
import psutil

from videoThreads import videoThread
import json

from bs4 import BeautifulSoup
import re
import os
import requests

if os.name != 'nt':
    import gi                         #Import gi pageage
    gi.require_version('Wnck','3.0')
    from gi.repository import Wnck
    
class NewParser():
    def __init__(self, url, host='127.0.0.1', port=9122):
        self.url = url.replace(' ', '')
        self.windowoptions = '--window-position=0,0 --window-size=0,0'
        self.chrome = None
        self.host, self.port = host, port
        
    def minimize(self):
        if os.name == 'nt':
            pass
        elif os.name == 'posix':
            screen=Wnck.Screen.get_default()  #Get screen information
            screen.force_update()             #Update screen object
            windows=screen.get_windows()      #Get all windows in task bar. The first 2 elements I believe relate to the OS GUI interface itself and the task bar. All other elements are the open windows in the task bar in that order.
            for w in windows:                 #Go through each window one by one.
                if 'Chromium' in w.get_name(): #Get name of window and check if it includes 'Chromium'
                    w.minimize()     
    
    def getPage(self):
        for trynum in range(50):
            try:      
                self.chrome = PyChromeDevTools.ChromeInterface(host=self.host, port=self.port)
            except requests.exceptions.ConnectionError:
                #print(f'ConnectionError - retrying... {trynum}')
                time.sleep(0.05)
                continue
        print('connected')

            
        if(self.chrome == None):
            raise Exception('ConnectionError: Could not connect to Chromium')

        self.minimize()

        self.chrome.Network.enable()
        self.chrome.Page.enable()
        #self.chrome.Page.setAdBlockingEnabled()


        #self.chrome.Fetch.enable(patterns=['*'])
        #print('enabled')
        start_time=time.time()
        self.chrome.Page.navigate(url=self.url)
        
        event,messages=self.chrome.wait_event("Page.frameStoppedLoading", timeout=60)
        event,messages=self.chrome.wait_event("Page.frameStoppedLoading", timeout=60)
        
        value = self.chrome.wait_event("Network.responseReceived", timeout=60)
        self.chrome.wait_event("Page.loadEventFired", timeout=60)
        end_time=time.time()
        #print ("Page Loading Time:", end_time-start_time)
        
        file_js = "onSubmit()"
        aa = self.chrome.Runtime.evaluate(expression=file_js)
        #print('onSubmit action:', aa)

        message=self.chrome.wait_message()
        reqid = message['params']['requestId']

        data = self.chrome.wait_event("Network.requestWillBeSent",timeout=60)
        responses = self.chrome.Network.getResponseBody(requestId=reqid)
        
        return responses

    def parseScript(self, content):
        body = ''
        streamLinks = []
        for r in content:
            if(type(r) == dict):
                js = json.loads(json.dumps(r))
                body = js['result']['body']
            
        soup = BeautifulSoup(body, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            code = script.get_text()
            if('player.src' in code):
                pattern = r"\"(.*?)\""
                matches = re.findall(pattern, code)
                streamLinks = [match for match in matches if 'm3u8' in match]
                
                
        #time.sleep(450)
        self.chrome.Page.close()
        
        return streamLinks[0]
    
    def getLink(self) -> list[str]:
        self.p = subprocess.Popen(f'chromium --remote-debugging-port={self.port} --remote-allow-origins=* {self.windowoptions} --disable-session-crashed-bubble', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True)      
    
        content = self.getPage()
        link = self.parseScript(content)

        return [link, 'https://link.encrypted-encrypted-encrypted-encrypted-encrypted-encrypted.link']