from base64 import encode
from typing import Optional
from fastapi import FastAPI,Request
from fastapi.params import Cookie
from pydantic import BaseModel
from selenium import webdriver
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#{"protocol":"http://","domain":"","method":"GET","encode":"UTF-8","header":{"key":"Content-Type","value":"","optional":[]},"arg":"","cookie":"","proxy":{"ip":"","port":""}}

class Header(BaseModel):
    key: str
    value: str
    optional: Optional[list] = None

class Proxy(BaseModel):
    ip: str
    port: str

class Item(BaseModel):
    protocol: str
    domain: str
    method: str
    encode: str
    header: Header
    arg: Optional[str] = None
    jsonarg: Optional[str] = None
    cookie: Optional[str] = None
    proxy: Optional[Proxy] = None
    
@app.post('/api/http')
def handle_http(item:Item):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1420,1080')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    url = item.protocol + item.domain
    if(item.arg!=None):
        url+='?' + item.arg

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    entries = driver.execute_script("return window.performance.getEntries()")
    for entry in entries:
        for  key in list(entry.keys()):
            if(key not in {'requestStart','responseEnd','name'}):
                entry.pop(key)
    return entries
