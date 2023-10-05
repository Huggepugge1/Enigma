import requests
import threading
import time
import math

from . import std_functions
from .std_functions import log, output


class RequestThread(threading.Thread):
    def __init__(self, method: str, url: str, request_body: dict={}, files: dict={}, request_cookies: dict={}, proxies: dict={}):
        super().__init__()
        self.method = method
        self.url = url
        self.request_body    = request_body
        self.files           = files
        self.request_cookies = request_cookies
        self.proxies         = proxies
        
        self.response = None
        
        self.apparent_encoding      = None
        self.content                = None
        self.cookies                = None
        self.elapsed                = None
        self.encoding               = None
        self.headers                = None
        self.history                = None
        self.is_permanent_redirect  = None
        self.is_redirect            = None
        self.links                  = None
        self.next                   = None
        self.ok                     = None
        self.reason                 = None
        self.request                = None
        self.status_code            = None
        self.text                   = None

    
    def __repr__(self):
        return f"RequestThread<{self.name}>"


    def run(self):
        """
        Send request to webserver
        Arguments:
            method (str): method of request (GET, POST, HEAD currently supported)
            url (str): url
            body (dict): body of request
            cookies (dict): specific cookies to send
            n (int): expected number of requests
        """
        try:
            if self.method.lower() == "get":
                self.response = requests.get(self.url, cookies=self.request_cookies, proxies=self.proxies)
            elif self.method.lower() == "post":
                self.response = requests.post(self.url, self.request_body, files=self.files, cookies=self.request_cookies, proxies=self.proxies)
            elif self.method.lower() == "head":
                self.response = requests.head(self.url, cookies=self.request_cookies, proxies=self.proxies)
            else:
                output(f"{self.method} is not yet a supported method")
                self.response = None
                return
                
            self.apparent_encoding      = self.response.apparent_encoding      
            self.content                = self.response.content                
            self.cookies                = self.response.cookies                
            self.elapsed                = self.response.elapsed                
            self.encoding               = self.response.encoding               
            self.headers                = self.response.headers                
            self.history                = self.response.history                
            self.is_permanent_redirect  = self.response.is_permanent_redirect  
            self.is_redirect            = self.response.is_redirect            
            self.links                  = self.response.links                  
            self.next                   = self.response.next                   
            self.ok                     = self.response.ok                     
            self.reason                 = self.response.reason                 
            self.request                = self.response.request                
            self.status_code            = self.response.status_code            
            self.text                   = self.response.text                   
        
        except requests.exceptions.ConnectionError:
            self.response = None
            log(f"Connection error on {self.name}")


class MultiRequestHandler(threading.Thread):
    def __init__(self, timeout: int=0, batch_size: int=10):
        super().__init__()
        self.queue = []
        self.timeout = timeout
        self.batch_size = batch_size
        self.pos = 0

    
    def __repr__(self):
        return f"MultiRequestHandler<{', '.join((thread.text if thread.text else 'None' for thread in self.queue))}>"


    def __len__(self):
        return len(self.queue)

    
    def __add__(self, request: RequestThread):
        self.queue.append(request)
        return self


    def __radd__(self, request: RequestThread):
        return self.__add__(request)


    def __iadd__(self, request: RequestThread):
        self.queue.append(request)
        return self


    def __getitem__(self, key):
        return self.queue[key]


    def __setitem__(self, key, value):
        self.queue[key] = value
        return self


    def __iter__(self):
        self.pos = 0
        return self


    def __next__(self):
        if self.pos < len(self):
            item = self.queue[self.pos]
            self.pos += 1
            return item
        else:
            raise StopIteration


    def batches(self):
        return [
                self[batch * self.batch_size:min(len(self), (batch + 1) * self.batch_size)]
                for batch in range(math.ceil(len(self) / self.batch_size))
               ]


    def run(self):
        for batch in self.batches():    
            for thread in batch:
                thread.start()
                time.sleep(self.timeout)

            for thread in batch:
                thread.join()


def request(method: str, url: str, body: dict={}, files: dict={}, cookies: dict={}, proxies: dict={}):
    """
    Send request to webserver (runs in seperate thread for speed in case of multiple requests are needed)
    Arguments:
        method (str): method of request (GET, POST, HEAD currently supported)
        url (str): url
        body (dict): body of request
        files (dict): files to send
        cookies (dict): specific cookies to send
        n (int): expected number of requests
    """
    thread = RequestThread(method, url, request_body=body, files=files, request_cookies=cookies, proxies=proxies)
    return thread

