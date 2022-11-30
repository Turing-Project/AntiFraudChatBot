import requests

def request(url, headers=None):
    if not headers:
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
    return requests.get(url, headers=headers).content