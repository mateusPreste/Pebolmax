
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
if __name__ == '__main__':
    chrome_options = ChromeOptions()
    driver = Chrome(options=chrome_options)
    driver.get("https://v3.sportsonline.sx/channels/pt/sporttv1.php")
    r = driver.requests
    for request in driver.requests:
        if (request.response and "m3u8" in request.url):
            print(
                request.url,
                request.response.status_code,
                request.headers
            )
    