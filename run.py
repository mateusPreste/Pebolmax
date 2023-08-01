import requests
from bs4 import BeautifulSoup as bs
import os

def getOptions(linksList, index):
  link1 = linksList[index][0]
  URL1 = link1
    
  r1 = requests.get(url = URL1)

  # extracting data in json format
  data1 = r1.text

  soup1 = bs(data1, features='lxml')
  mydivs1 = soup1.find("div", {"class": "options_iframe"})
  links = mydivs1.find_all("a")

  sourceList = []
  for el in links:
    sourceLink = el['data-url']
    #print(sourceLink)
    sourceList.append([sourceLink, el.string])
  return sourceList

import re

def returnEndpointList(sourceList):
  #print('sourceList', sourceList)
  endPointList = []
  for el in sourceList:
  #  print('>>>>>>>>>>>>>>>.', el)
    url2 = el

    r2 = requests.get(url = url2)

    # extracting data in json format
    data2 = r2.content.decode('utf-8')

    soup2 = bs(data2, features='lxml')
    script = soup2.find_all("script", {})

    counter = 0
    for el in script:
      #print(counter, 'Clappr' in el.get_text())
      stringText = el.get_text()
      #print(el.text)
      if('Clappr' in stringText):
        #print(el)
        m = re.findall('source: \"(.*?)\"', str(el))
        if(m):
          #print(m[0])
          endPointList.append(m[0])

      if('x_id_analise' in stringText):
        endpoint = returnLink(el.text)
        #print(endpoint)
        if(endpoint != None):
          endPointList.append(endpoint)
      counter += 1
    
  return endPointList

import json
import re

def returnLink(code):
  try:
    #print(code)

    hd = re.findall('\(function\([^\)]*\)\{var [^\=]*\=function\([^\)]*\)\{while\(--[^\)]*\)\{[^\[]*\[\'push\'\]\([^\[]*\[\'shift\'\]\(\)\);\}\};[^\(]*\(\+\+[^\)]*\);\}\(([^\,]*),([^\)]*)\)\);', code)

    #print('hd', hd)

    cnt = {}
  
    cntT = f'x={hd[0][1]};'

    #print('cntT', cntT)
    exec(cntT, cnt)
    #print('cnt', cnt['x'])

    #code = code.replace('\'', '')

    #regex to find lists
    ts = re.findall("var ([^=]*)=\[([^\]]*)\];", code)

    #regex to find functions
    functions = re.findall('var ([^=]*)=function\(([^\)]*)\)\{([^\}]*)\}', code, re.DOTALL | re.MULTILINE)

    #extract content from the main list
    lista = ts[0][1].split(',')
    #print('lista', lista)
    listaL = list(map(lambda x: x.encode('latin1', 'ignore').decode('unicode_escape', 'ignore').encode('latin1', 'ignore').decode('utf-8','ignore'), lista))

    #print("*", ts[0][0], listaL, '\n') 


    def outter(data, i):
      def write(isLE):
        #print('write', isLE)
        counter = isLE % len(data)
        for el in range(counter):
          x = data.pop(0)
          data.append(x)
      write(++i);
      return data

    outter(listaL, cnt['x'])

    #print(listaL)

    findFunction = None


    for func in functions:
        varName, variables, definition = func
        
        variables = variables.split(",")
        if(len(variables) == 2):
          findFunction = varName
          a, b = variables
          c = definition.replace(a, 'var1').replace(b, 'var2').replace('var ', '').replace(';', ';\n\t')
          c = c[:-3]+'[1:-1]'
          #print('cc', c)
          
          #defining function in runtime
          pr = f'{ts[0][0]} = {listaL}\ndef fun(var1):\n\tvar1=int(var1, 16)\n\t{c}'

          #printing main list on runtime
          #print(pr)

          #print func (variables) {content}
          #print(varName, variables,"\n", c)
          funcL = {}
          exec(pr, funcL)
          #print(funcL['fun']('0x12'))

          #shows a string being returned from list
          #print('fun', fun('0x12'))
        
    if(findFunction != None):
      strings = re.findall(f'=({findFunction}[^,;]*)', code, re.DOTALL | re.MULTILINE)
      for st in strings:
          text = ''
          #st = list(map(lambda x: x, st))
          cmd2 = f'{pr}\ntext = '+st.replace(f'{findFunction}', 'fun').encode('latin1', 'ignore').decode('unicode_escape', 'ignore').encode('latin1', 'ignore').decode('utf-8', 'ignore')

          saveV = {}
          #print('cm2', cmd2)
          try:
            exec(cmd2, saveV)
            #print(r'm3u8' in saveV['text'], saveV['text'])
            if(r'm3u8' in saveV['text']):
              return saveV['text']
          except Exception: 
            pass
          
  except Exception:
    pass
    #exc_type, exc_obj, exc_tb = sys.exc_info()
    #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #print(exc_type, fname, exc_tb.tb_lineno)



import os    
def interpreter(line):
    command = os.system(f'cmd /c "{line}"')
    return command





def genEvents():
  URL = "https://futemax.app/"
    
  r = requests.get(url = URL)

  # extracting data in json format
  data = r.text


  soup = bs(data, features='lxml')
  #widget-home
  mydivs = soup.find("div", {"class": "widget-home"})
  links = mydivs.find_all("div", {'class': 'item-wd'})
  #result = [x['data-name-en'] for x in soup('span') if x.has_attr('data-name-en')]

  linksList = []

  for el in links:
    lk = el.a['href']
    desc = el.a.span.text
    linksList.append([lk, desc])
    #print(lk)
    #print(desc)
    #print()

  return linksList


def main():
  linksList = genEvents()

  print('-- Esses são os jogos ao vivo do pebolmax: --')

  for ind, link in enumerate(linksList):
    showText = re.sub(r'Assistir|ao vivo|online', '', link[1])
    print(f'|{ind}|{showText}')

  print()

  gameChoosed = int(input('Insira o Numero do jogo: '))

  options = getOptions(linksList, gameChoosed)

  print('\n')
  print('-- Opções de transmissão: --')
  for ind, opt in enumerate(options):
    showText = opt[1]
    print("|", ind, "|", showText, opt[0])

  linkOptions = [el[0] for el in options]

  optionChoosed = int(input('Insira o Numero da opção: '))

  print()

  endpoints = returnEndpointList([linkOptions[optionChoosed]])
  print('endpoints', endpoints)
  endpoint = endpoints[0]
  

  cmd = f'streamlink \'{endpoint}\' best --http-header \'User-Agent= Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0\' \
                 --http-header \'Accept= */*\' \
                 --http-header \'Accept-Language= en-US,en;q=0.5\' \
                 --http-header \'Accept-Encoding= gzip, deflate, br\' \
                 --http-header \'Origin= https://futemax.app\' \
                 --http-header \'Sec-Fetch-Dest= empty\' \
                 --http-header \'Sec-Fetch-Mode= cors\' \
                 --http-header \'Sec-Fetch-Site= cross-site\' \
                 --http-header \'Referer= https://futemax.app/\' \
                 --http-header \'DNT= 1\' \
                 --http-header \'Connection= keep-alive\' \
                 --http-header \'Pragma= no-cache\' \
                 --http-header \'Cache-Control= no-cache\' --player-passthrough \'https\' --player \'vlc\''

  print(cmd)

  if os.name == 'nt':
    interpreter(cmd.replace("\'", "\""))
  else:
    os.system(cmd)
  

main()
