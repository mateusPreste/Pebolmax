import requests
from bs4 import BeautifulSoup
import json

from sportsonline import SportsOnline
from cloudflare import CloudFlareHandler
from videoThreads import videoThread
from playertv import PlayerTV
from redecanais import RedeCanais
from embedflix import Embedflix

import time

supported_sources = ['embedflix', 'v3.sportsonline.sx', 'youtube.com', 'cloudflarestream', 'playertv', 'sinalpublico']

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

def selectSource(session, source, link) -> list[str]:
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
        optionLink = option['data-url'].replace(' ', '')
        optionName = getSourceName(optionLink)
        #print(optionName, optionLink)
        if(verifysource(optionLink)):
            optionList.append([optionName, optionLink])
        else:
            optionList.append([optionName, optionLink])
    return optionList

def main():
    session = requests.Session()
    linkList = getTodayGames(session, "https://multicanais.cl/")
    
    print('Jogos de hoje')
    for ind, value in enumerate(linkList):
        title, link = value
        print(f'|{ind}| {title}')
        
        
    result = input("\nInsira o numero do jogo: ")
    
    title, link = linkList[int(result)]
    print(title)
    optionList = getGameOptions(session, title, link)
    
    for idx, option in enumerate(optionList):
        print(f'[ {idx} ]',option)
    print(f'[-1 ] [ exibir todas simultaneamente ]')
    
    optionNumber = input('Escolha uma opção: ')
    
    streamlist = []
    
    if(optionNumber == '-1'):
        for source, olink in optionList:
            if(source != "UNSUPPORTED"):
                try:
                    [videoUrl, originUrl] = selectSource(session, source, olink)
                    streamlist.append([videoUrl, originUrl])
                except Exception:
                    print('Fail')
                
    else:
        source, olink = optionList[int(optionNumber)]
        [videoUrl, originUrl] = selectSource(session, source, olink)
        streamlist.append([videoUrl, originUrl])
    
    threads = []
    for videoUrl, originUrl in streamlist:
        thread = videoThread(videoUrl, originUrl)
        thread.start()
        threads.append(thread)
        
    while(True):
        time.sleep(1)
        for thread in threads:
            out = thread.subprocess.stdout.readline()
            print(type(out))
            print('output', out)
    
main()