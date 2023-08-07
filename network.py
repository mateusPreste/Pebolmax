import requests

class NetworkSession:
    def __init__(self, session=None):
        if(session == None):
            self.session = requests.Session()
        
    def request(self, method, url, headers, data, timeout=1000, retries=1):
        for chance in range(retries):
            try:
                return self.session.request(method, url, headers=headers, data=data, timeout=timeout)
            except TimeoutError:
                print(f'debug: timeout error - retrying... {chance}')
                continue
        raise RuntimeError("The content cannot be loaded.")