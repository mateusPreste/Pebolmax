import requests

url = "https://link.encrypted-encrypted-encrypted-encrypted-encrypted-encrypted.link/player3/ch.php?canal=c0hEOUROL2NVRkViRWpoRXhrNXEvQXJFbmRSL0R6Q3hiVTZ6TzBIU3A0QmRyRmszblM0WnNKUStEOUQxVE4zYmRnbGRJNVFiYm1vWEdFbW1USUZjY2c4L1FLTGVFZ2ladVN1QVRsNXY2bmZBdnQyQnVpOXh5R3JOK2p1QmJVbG8yR0I2MjR6bDlPZTVTQ1I1T1FjcGM3Q1VQVHB3YW55aUUrRmlJbmZ1Q1VxRnovWUFPT3FYc1ZOZnBvZCtqT289"

payload={}
headers = {
  'authority': 'link.encrypted-encrypted-encrypted-encrypted-encrypted-encrypted.link',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'cookie': '__dtsu=4C30169100106511A0D2FE613C6F6426; _cc_id=57fda6a8c78b2732d54816e07bea9e0; panoramaId=f2ecdd080efa152391d43857848c16d5393833c1b0693f5745d9f7cdbea6ae7e; panoramaIdType=panoIndiv; panoramaId_expiry=1691702346193; cf_clearance=ZXCkbgOENl5O0urFNq7gy2m9sh3zOyorr_KhvN7cs.g-1691103256-0-1-3566bd96.2579fc7.236096cd-0.2.1691103256',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'cross-site',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
print(response.content)
print(response.status_code)
print(response.headers)
