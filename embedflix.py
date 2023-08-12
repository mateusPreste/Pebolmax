import requests

from seleniumwire.webdriver import Chrome, ChromeOptions
import time
from bs4 import BeautifulSoup
import re
import json
from network import NetworkSession

class Embedflix():
    def __init__(self, url):
        self.url = url.replace(' ', '')
        self.session = NetworkSession()
    
    def match_string(self, string, text):
        return re.search(string, text).group(0).split(' = ')[-1]
    
    def getPage(self, url):
        link = url.replace(" ", "")
        url = link

        payload = {}
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Alt-Used': 'embedflix.net',
        'Connection': 'keep-alive',
        'Referer': 'https://multicanais.cl/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=1000)

        #print(response.text)
        #line = match_string('let video_id =', response.text)
        videoId = self.match_string('let video_id =([^;]+)', response.text)
        action = self.match_string('action      : ([^,]+)', response.text)
        action = action.split(' ')[-1].replace('\'','')
        ip_address = requests.get('https://api.ipify.org').text
        
        #print('videoId', videoId, 'action', action)
        
        url = "https://embedflix.net/api"

        payload = f'action={action}&client_ip={ip_address}&video_id={videoId}'
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://embedflix.net',
        'DNT': '1',
        'Alt-Used': 'embedflix.net',
        'Connection': 'keep-alive',
        'Referer': f'{link}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=1000)
        jsonResponse = json.loads(response.text)
        return jsonResponse

    def parseScript(self, content):
        url = content['data']['video_url'] + '?wmsAuthSign=' + content['data']['url_signature']
        return url
    
    def getLink(self) -> list[str]:
        content = self.getPage(self.url)
        link = self.parseScript(content)

        return [link, 'https://embedflix.net']