import requests

from seleniumwire.webdriver import Chrome, ChromeOptions
import time
from bs4 import BeautifulSoup
import re
import js2py

class SportsOnline():
    def __init__(self, url):
        self.url = url
    
    def getPage(self, url):
        session = requests.Session()
        page = session.get(url, timeout=2)
        return page.content

    def getEmbed(self, url):
        #retriving only the domain to fill the authority header
        authority = url.split('https://')[1].split('/')[0]
        code = url.split('https://')[1].split('/')[-1]

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

        return [authority, response.text]

    def parseScript(self, content) -> str:
        soup = BeautifulSoup(content, "html.parser")
        scripts = soup.find_all('script')
        
        playerScript = ''
        
        for sc in scripts:
            if('eval' in sc.text and 'player' in sc.text):
                playerScript = sc.text
                
        playerScript = playerScript.replace('</script>', '').replace('<script>', '').replace('eval(', '')[:-2]
        playerScript = playerScript.replace('function(p,a,c,k,e,d)', 'result = function ex(p,a,c,k,e,d)')
        # Use js2py to execute the JavaScript code
        context = js2py.EvalJs()
        result = context.execute(playerScript)
        
        pattern = r"\"(.*?)\""
        matches = re.findall(pattern, context.result)
        matches = [cont for cont in matches if 'https' in cont]
        return matches[0]
    
    def getLink(self) -> list[str]:
        content = self.getPage(self.url)
    
        soup = BeautifulSoup(content, "html.parser")
        iframes = soup.find_all("iframe")
        
        videoUrl = ''
        authority = ''
        
        for iframe in iframes:
            nextLink = iframe['src']
            [authority, nextContent] = self.getEmbed(nextLink)
            videoUrl = self.parseScript(nextContent)
        return [videoUrl, 'https://'+authority]

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