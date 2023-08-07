import requests

from seleniumwire.webdriver import Chrome, ChromeOptions
import time
from bs4 import BeautifulSoup
import re
import js2py
from network import NetworkSession

class PlayerTV():
    def __init__(self, url):
        self.url = url.replace(' ', '')
        self.session = NetworkSession()
    
    def getPage(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Alt-Used': 'playertv.net',
            'Connection': 'keep-alive',
            'Referer': 'https://multicanais.cl/',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        
        
        response = self.session.request("GET", url, headers=headers, data={}, timeout=5)
        return response.content

    def parseScript(self, content):
        soup = BeautifulSoup(content, "html.parser")
        scripts = soup.find_all("script")
        
        links = []
        
        for sc in scripts:
            if('jwplayer' in sc.text):
                pattern = r"\'(.*?)\'"
                matches = re.findall(pattern, sc.text)
                for match in matches:
                    if('http' in match):
                        links.append(match)
                        
        return links[0]
    
    def getLink(self) -> list[str]:
        content = self.getPage(self.url)
        link = self.parseScript(content)

        return [link, 'https://playertv.net/']

#https://dut9w58y58wfh5xm.cdnministry.net:8443/hls/61i6q3jvgok.m3u8?s=_gsfR9UBm9mVaPO7_wEFTw&e=1691022967
#    import time
#rom seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
#if __name__ == '__main__':
#    chrome_options = ChromeOptions()
#    
##    #chrome_options.headless = True
#    driver = Chrome(options=chrome_options)
#    driver.get("https://v3.sportsonline.sx/channels/pt/sporttv1.php")
#    r = driver.requests
#    for request in driver.requests:
#        if (request.response and "m3u8" in request.url):
#            print(
#                request.url,
#                request.response.status_code,
#                request.headers
#            )
#    time.sleep(10)