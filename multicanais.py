import requests
from bs4 import BeautifulSoup
import json

from seleniumwire.webdriver import Chrome, ChromeOptions
from sportsonline import SportsOnline
from cloudflare import CloudFlareHandler
from videoThreads import videoThread
from playertv import PlayerTV

supported_sources = ['embedflix', 'v3.sportsonline.sx', 'youtube.com', 'cloudflarestream', 'playertv']

def verifysource(source):
    for s in supported_sources:
        if s in source:
            return True
    return False

def getSourceName(link):
    for s in supported_sources:
        if s in link:
            return s
    return "UNSUPPORTED"

def selectSource(session, source, link):
    link = link.replace(' ', '')
    if(source == 'embedflix'):
        return getEmbedflix(session, link)
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
    elif(source == 'UNSUPPORTED'):
        print('Essa fonte não é suportada')
        exit(0)

def getTodayGames(session, url):
    get_page = session.get(url)
    
    soup = BeautifulSoup(get_page.content, 'html.parser')
    gamesSection = soup.find_all("div", id="vlog-module-0-1")
    eachGame = gamesSection[0].find_all("article")
    
    gamesLinks = []
    for game in eachGame:
        div = game.find("div", class_="entry-image")
        link = div.find('a')['href']
        title = div.find('a')['title']
        title = title.replace("Assistir ", "").replace('ao vivo','').replace('online','').replace('grátis','')
        #print(title, link)
        gamesLinks.append([title, link])
        #print()
    return gamesLinks
    #get content from xpath 

def getGameOptions(session, title, link):
    get_page = session.get(link)
    soup = BeautifulSoup(get_page.content, 'html.parser')
    options = soup.find_all("div", class_="options_iframe")
    eachOption = options[0].find_all("a")
    optionList = []
    for option in eachOption:
        optionLink = option['data-url']
        optionName = getSourceName(optionLink)
        #print(optionName, optionLink)
        if(verifysource(optionLink)):
            optionList.append([optionName, optionLink])
        else:
            optionList.append([optionName, optionLink])
    return optionList

import re

def match_string(string, text):
    return re.search(string, text).group(0).split(' = ')[-1]

        
def getEmbedflix(session, link):
    link = link.replace(" ", "")
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
    videoId = match_string('let video_id =([^;]+)', response.text)
    action = match_string('action      : ([^,]+)', response.text)
    action = action.split(' ')[-1].replace('\'','')
    ip_address = requests.get('https://api.ipify.org').text
    
    print('videoId', videoId, 'action', action)
    
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
    print(jsonResponse)
    url = jsonResponse['data']['video_url'] + '?wmsAuthSign=' + jsonResponse['data']['url_signature']
    #print(url)
    return [url, 'https://embedflix.net']
    
import os    
def interpreter(line):
    command = os.system(f'cmd /c "{line}"')
    return command


def showVideo(endpoint, origin):
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
        interpreter(cmd.replace("\'", "\"").replace('&', '^&'))
    else:
        os.system(cmd)
    

def main():
    session = requests.Session()
    linkList = getTodayGames(session, "https://multicanais.cl/")
    
    print('Jogos de hoje')
    for ind, value in enumerate(linkList):
        title, link = value
        print(f'|{ind}| {title}')
        
    result = input("Insira o numero do jogo: ")
    
    title, link = linkList[int(result)]
    print(title)
    optionList = getGameOptions(session, title, link)
    
    for option in optionList:
        print(option)
    
    optionNumber = input('Escolha uma opção: ')
    
    streamlist = []
    
    if(optionNumber == '-1'):
        for source, olink in optionList:
            if(source != "UNSUPPORTED"):
                [videoUrl, originUrl] = selectSource(session, source, olink)
                streamlist.append([videoUrl, originUrl])
    else:
        source, olink = optionList[int(optionNumber)]
        [videoUrl, originUrl] = selectSource(session, source, olink)
        streamlist.append([videoUrl, originUrl])
    
    for videoUrl, originUrl in streamlist:
        thread = videoThread(videoUrl, originUrl)
        thread.start()
    
main()