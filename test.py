import requests
import re
from bs4 import BeautifulSoup
from videoThreads import videoThread
import json

url = "https://www.playstream.site/p/embed.html?id=1076286"

idValue = int(url.split('?')[-1].replace('id=', ''))

payload={}
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

response = requests.request("GET", url, headers=headers, data=payload, timeout=1000)

content = response.text

print(content)

soup = BeautifulSoup(content, "html.parser")
scripts = soup.find_all('script')

links = []

for sc in scripts:
    if('EMBED' in sc.text):
        pattern = r"\'(.*?)\'"
        matches = re.findall(pattern, sc.text)
        for match in matches:
            if('http' in match):
                links.append(match)

print(links)

response1 = requests.request('GET', links[0], headers=headers, data=payload, timeout=1000)

jsonResponse = json.loads(response1.text)

print('json', jsonResponse)

internalLink = ''

for el in jsonResponse:
  if(el['embed'] == idValue):
    print(el['link'])
    internalLink = el['link']
    
print('internalLink', internalLink)

internalLink = 'https://voodc.com/embed/85899a889c8b8499879983c6c2c2cac0c2d5b8dc.html'

response1 = requests.request('GET', internalLink, headers=headers, data=payload, timeout=1000)

#vodc

soup = BeautifulSoup(response1.text, "html.parser")
div = soup.find_all('script')
divRemoved = soup.find_all('h4')


if(len(divRemoved) > 0):
  print('liveEnded')
  exit()

print(response1.text)

finalLink = 'https:'+div[0]['src']

print('finalLink', finalLink)

response1 = requests.request('GET', finalLink, headers=headers, data=payload, timeout=1000)

code = response1.text

#print(code)

pattern = r"var\s+([a-zA-Z_$][\w$]*)(\s*=\s*[^,;]+)?"
matches = re.findall(pattern, code)
#print('MATCHES', matches)

#videoInstance = videoThread(links[0], 'https://playertv.net/')
#videoInstance.start()