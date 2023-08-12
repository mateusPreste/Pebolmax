import requests
from bs4 import BeautifulSoup
import json

import subprocess

from sportsonline import SportsOnline
from cloudflare import CloudFlareHandler
from videoThreads import videoThread
from playertv import PlayerTV
from redecanais import RedeCanais
from embedflix import Embedflix

import time
import os

from terminalThread import terminalThread

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

def interactive():
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
    return [optionList, optionNumber]

def main():
    while(True):
        [optionList, optionNumber] = interactive()
        
        if(optionNumber == '-1'):
            for source, olink in optionList:
                if(source != "UNSUPPORTED"):
                    thread = terminalThread(source, olink)
                    thread.start()           
        else:
            source, olink = optionList[int(optionNumber)]
            thread = terminalThread(source, olink)
            thread.start()
            
        subprocess.Popen(f'gridplayer', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
main()