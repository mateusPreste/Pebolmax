import requests

from seleniumwire.webdriver import Chrome, ChromeOptions
import time
from bs4 import BeautifulSoup
import re

import os    
def interpreter(line):
    command = os.system(f'cmd /c "{line}"')
    return command


def showVideo(endpoint, origin):
    print('endpoint', endpoint)
    print('origin', origin)
    
    cmd = f'streamlink \'{endpoint}\' best --http-header \'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0\' \
        --http-header \'Accept= */*\' \
        --http-header \'Accept-Language= en-US,en;q=0.5\' \
        --http-header \'Accept-Encoding= gzip, deflate, br\' \
        --http-header \'Origin= {origin}\' \
        --http-header \'Sec-Fetch-Dest= empty\' \
        --http-header \'Sec-Fetch-Mode= cors\' \
        --http-header \'Sec-Fetch-Site= cross-site\' \
        --http-header \'Referer= {origin}/\' \
        --http-header \'DNT= 1\' \
        --http-header \'Connection= keep-alive\' \
        --http-header \'Pragma= no-cache\' \
        --http-header \'Cache-Control= no-cache\' --player-passthrough \'https\' --player \'vlc\''
        
    if(origin==''):
        cmd = f'vlc \"$(yt-dlp --get-url --format best \'{endpoint}\')\"'

    print(cmd)

    if os.name == 'nt':
        interpreter(cmd.replace("\'", "\""))
    else:
        os.system(cmd)

blacktokens = ['function','src','https','setTimeout','document','width','height','position','player','if','var','hlsjsConfig','unmute','newplayer','stream','p2p','p2pml','fadeIn','logo','startMuted','true','videoStarted','play','false','btn','60','undefined','Player','Clappr','new','mute','fadeOut','typeof','engine','hlsjs','100','loader','isSupported','Engine','createLoaderClass','Infinity','parentId','ready','else','source','maxBufferLength','liveMaxLatencyDuration','events','WSUnmute','destroy','options','configure','none','display','css','offline','WSreloadStream','initClapprPlayer','onReady','onVolumeUpdate','onPause','1000','onPlay','errorPlaying','onError','watermarkLink','watermark','bestfit','stretching','autoPlay','playback','liveSyncDuration','allow','id','5000px','iframe','php','gen','popups','scripts','origin','same','sandbox','absolute','left','top','hidden','visibility','style','forms','serve','pro','adsilo','online','contentango','ad','alpS84jP25','1800000','getElementById','setInterval','window','fXHggLmTuE','CMAs8uhhKm','s5e83yzhMM','50000','body','append','PReDvl944m','redirect','tid','756113','info','mckensecuryr','WYbHISCtLV','uFkWgZKDzl','sGwNIyGLG5','N2JBJxP2ji','MrwGr89ffS','CX0BW0NjsB','HsP3nKe6J5','1080','1920','1024','768','1280','800','1366']

def getPage(url):
    session = requests.Session()
    page = session.get(url, timeout=2)
    return page.content

def getEmbed(url):
    #retriving only the domain to fill the authority header
    authority = url.split('https://')[1].split('/')[0]
    print('authority', authority)
    code = url.split('https://')[1].split('/')[-1]
    print('code', code)

    payload={}
    headers = {
    'authority': f'{authority}',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'hf1=1',
    'referer': 'https://v3.sportsonline.sx/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'iframe',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=2)

    return [code, authority, response.text]

def parseScript(content):
    l = re.findall(r"'(.*?)'", content) # the (.*?) is a non-greedy group that matches anything inside the apostrophes
    content = ''
    for ind, element in enumerate(l):
        if('|' in element and len(element) > 10):
            content += element+'|'
            #print(element)
    contentList = content.split('|')
    print(contentList, len(contentList))
    return [el for el in contentList if el not in blacktokens]


def getHtml(url):
    content = getPage(url)
    
    soup = BeautifulSoup(content, "html.parser")
    iframes = soup.find_all("iframe")
    
    contentList = []
    lcode = ''
    
    for iframe in iframes:
        nextLink = iframe['src']
        print('NextLink', nextLink)
        [code, authority, nextContent] = getEmbed(nextLink)
        lcode = code
        contentList = parseScript(nextContent)
        print('contentList', contentList)
    return [lcode, authority, contentList]
    
[lcode, authority, contentList] = getHtml('https://v3.sportsonline.sx/channels/hd/hd9.php')

contentList = contentList[:13]

print(contentList)

finalList = []
value = ''
number = ''
valueField = False
cdn = ''
for el in contentList:
    if(el == 'm3u8'):
        valueField = True
    elif(el.isnumeric()):
        valueField = False
        number = el
    if('cdn' in el):
        cdn = el
    
    if(el != 'm3u8' and valueField):
        value += '-'+el
        
value = value[1:]
print('value', value)
print('number', number)
print('code', lcode)
print('cdn', cdn)
first = ''

okTokens = [number, lcode, cdn,'net', '8443', 'hls', 'm3u8']

for el in value.split('-'):
    okTokens.append(el)

for el in contentList:
    if el not in okTokens and el != '' and (len(el) != 6 and el[0] !='a'):
        finalList.append(el)
        
print('finalList', finalList)
if(len(finalList) == 1):
    first = finalList[0]
    
url = f'{first}.{cdn}.net:8443/hls/{lcode}.m3u8?s={value}&e={number}'
    
showVideo(url, 'https://'+authority)
    

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