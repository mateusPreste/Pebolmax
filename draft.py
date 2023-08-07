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