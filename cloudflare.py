import requests
from bs4 import BeautifulSoup

class CloudFlareHandler():
    def __init__(self, url):
        self.url = url
    
    def getLink(self):
        content = requests.get(self.url).content
        soup = BeautifulSoup(content, "html.parser")
        scripts = soup.find_all('stream')
        domain = self.url.split('https://')[1].split('/')[0]
        videoId = scripts[0]['src']
        url = f'https://{domain}/'+videoId+'/manifest/video.mpd'
        return [url, f'https://{domain}/']
