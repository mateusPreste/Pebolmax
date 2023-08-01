import time
from seleniumwire.webdriver import Chrome, ChromeOptions

def getVideoSportsOnlineInfo(url):
    print('Obtendo as informações do video')
    chrome_options = ChromeOptions()
    
    chrome_options.add_argument('--headless')
    driver = Chrome(options=chrome_options)
    driver.get(url)
    r = driver.requests
    
    videoUrl, videoOrigin = '',''
    for request in driver.requests:
        if (request.response and "m3u8" in request.url):
            videoUrl = request.url
            videoOrigin = request.headers['Origin']
            
    if(videoOrigin == '' or videoUrl == ''):
        print('ERROR: Não foi possivel obter as informações sobre a transmissão.')
        
    return [videoUrl, videoOrigin]
            
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
    
if __name__ == '__main__':
    #url = "https://v3.sportsonline.sx/channels/hd/hd5.php"
    #[videoUrl, videoOrigin] = getVideoSportsOnlineInfo(url)
    videoUrl = 'https://www.youtube.com/embed/1bwSvt2IWtU'
    videoOrigin = ''
    showVideo(videoUrl, videoOrigin)
    
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