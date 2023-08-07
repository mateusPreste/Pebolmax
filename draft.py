import PyChromeDevTools
import time


chrome = PyChromeDevTools.ChromeInterface()
chrome.Network.enable()
chrome.Page.enable()

chrome.Page.navigate(url="https://sinalpublico.com/player3/ch.php?canal=espn4")
event,messages=chrome.wait_event("Page.frameStoppedLoading", timeout=60)


for m in messages:
    print(m)
    if "method" in m and m["method"] == "Network.responseReceived":
        try:
            url=m["params"]["response"]["url"]
            print (url)
        except:
            pass
        
value = chrome.wait_event("Network.responseReceived", timeout=60)
reqid = value[0]['params']['requestId']
print("reqid: ", reqid)
responses = chrome.Network.getResponseBody(requestId=reqid)


#for reponse in responses:
    #print(response)
        
value = chrome.wait_event("DOMDebugger.getEventListeners", timeout=5)

#document = chrome.DOM.getDocument(depth=-1)
#print(document)

#devtools idenifiers
#https://cdn.jsdelivr.net/npm/console-ban@4.1.0/dist/console-ban.min.js
#https://link.encrypted-encrypted-encrypted-encrypted-encrypted-encrypted.link/player3/devtools-detector.js