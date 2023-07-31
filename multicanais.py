import requests
from bs4 import BeautifulSoup
import json

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
        optionName = option.text
        optionLink = option['data-url']
        #print(optionName, optionLink)
        if('embedflix' in optionLink):
            optionList.append([optionName, optionLink])
        else:
            optionList.append([optionName+' INDISPONIVEL', optionLink])
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
    print('videoId', videoId)
    
    url = "https://embedflix.net/api"

    payload = f'action=getPlayer&client_ip=187.46.89.113&video_id={videoId}'
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
    url = jsonResponse['data']['video_url'] + '?wmsAuthSign=' + jsonResponse['data']['url_signature']
    print(url)
    showVideo(url, 'https://embedflix.net')
    
import os    
def interpreter(line):
    command = os.system(f'cmd /c "{line}"')
    return command


def showVideo(endpoint, origin):
    cmd = f'streamlink \'{endpoint}\' best --http-header \'User-Agent= Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0\' \
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

    print(cmd)

    if os.name == 'nt':
        interpreter(cmd.replace("\'", "\""))
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
    

    
    name, olink = optionList[0]
    print(optionList)
    getEmbedflix(session, olink)
    
main()