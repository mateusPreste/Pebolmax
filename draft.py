import PyChromeDevTools
import time

import subprocess
import psutil

from videoThreads import videoThread
import json

from bs4 import BeautifulSoup
import re
import os

#devnull = open('/dev/null', 'w')

#SW_HIDE = 0
#info = subprocess.STARTUPINFO()
#info.dwFlags = subprocess.STARTF_USESHOWWINDOW
#info.wShowWindow = SW_HIDE

url = 'https://sinalpublico.com/player3/ch.php?canal=espn4'

p = subprocess.Popen(f'chromium --remote-debugging-port=9222 --remote-allow-origins=* --window-position=0,0 --window-size=0,0 --disable-session-crashed-bubble {url}', shell=True)

if os.name != 'nt':
    time.sleep(1)
    
chrome = PyChromeDevTools.ChromeInterface()

chrome.Network.enable()
chrome.Page.enable()

#chrome.Page.navigate(url="https://sinalpublico.com/player3/ch.php?canal=espn4")
#event,messages=chrome.wait_event("Page.frameStoppedLoading", timeout=60)
#
#
#for m in messages:
#    #print(m)
#    if "method" in m and m["method"] == "Network.responseReceived":
#        try:
#            url=m["params"]["response"]["url"]
#     #       print (url)
#        except:
#            pass
        
#value = chrome.wait_event("Network.responseReceived", timeout=60)
#print('finished')
#reqid = value[0]['params']['requestId']
#print("reqid: ", reqid)
#responses = chrome.Network.getResponseBody(requestId=reqid)


#for reponse in responses:
    #print(response)
        
#value = chrome.wait_event("DOMDebugger.getEventListeners", timeout=5)
time.sleep(1)

file_js = "onSubmit()"
chrome.Runtime.evaluate(expression=file_js)

message=chrome.wait_message()
reqid = message['params']['requestId']

data = chrome.wait_event("Network.requestWillBeSent",timeout=60)
responses = chrome.Network.getResponseBody(requestId=reqid)
#js = json.loads(responses)
print()

body = ''
streamLinks = []
for r in responses:
    if(type(r) == dict):
        js = json.dumps(r)
        js = json.loads(js)
        body = js['result']['body']
    #print(type(r))
    #print(r)
    
soup = BeautifulSoup(body, 'html.parser')
scripts = soup.find_all('script')
for script in scripts:
    code = script.get_text()
    if('player.src' in code):
        
        pattern = r"\"(.*?)\""
        matches = re.findall(pattern, code)
        streamLinks = [match for match in matches if 'm3u8' in match]

pid = p.pid
parent = psutil.Process(pid)
for child in parent.children(recursive=True):  # or parent.children() for recursive=False
    child.kill()
parent.kill()

terminal = videoThread(streamLinks[0], 'https://link.encrypted-encrypted-encrypted-encrypted-encrypted-encrypted.link')
terminal.start()

#document = chrome.DOM.getDocument(depth=-1)
#print(document)

#devtools idenifiers
#https://cdn.jsdelivr.net/npm/console-ban@4.1.0/dist/console-ban.min.js
#https://link.encrypted-encrypted-encrypted-encrypted-encrypted-encrypted.link/player3/devtools-detector.js

#Request interception
#    await Network.Enable();
#    await Network.enableRequestInterception({enabled: true});
#    Network.requestIntercepted((params) => {
#      let continueParams = {interceptionId: params.InterceptionId};
#      if (params.request.url.endsWith('.jpg')) {
#        // Pretend the .jpg IP address was unreachable.
#        continueParams.errorReason = 'AddressUnreachable';
#      } else if (params.hasOwnProperty('redirectStatusCode') &&
#                 params.redirectStatusCode == 302) {
#        // Pretend the server sent a 404 instead of a 302.
#        continueParams.rawResponse =
#            btoa("HTTP/1.1 404 Not Found\r\n\r\n");
#      } else {
#        // Allow the request to continue as normal.
#      }
#      Network.continueInterceptedRequest(continueParams);
#    });
#
#    Page.navigate({url: 'http://some-website.tld/'})