import requests


def request(method: str, url: str, body: dict={}):
    if method.lower() == "get":
        return requests.post(url)
    elif method.lower() == "post":
        return requests.post(url, body)
    elif method.lower() == "head":
        return requests.head(url, body)