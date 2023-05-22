from fastapi import FastAPI 
from pydantic.main import BaseModel
import requests
import json

class HelloWorldRequest(BaseModel):
    id : str
    name : int

app = FastAPI()

base_url = 'http://192.168.1.12:5000/users'

def getUrlData(url):
    response = requests.get(url)
    contents = response.text
    data = json.loads(contents)
    return data

@app.get(path='/')
async def healthCheck():
    return "OK"

@app.get(path='/getdata')
async def getData():
    url = base_url

    return getUrlData(url)

@app.get(path='/getquery')
async def getQuery(id=None, name=None):
    if (id is None) and (name is None):
        return "id, name을 입력하세요."
    else:
        if id is None:
            print("id null")
            params = '?name=' + name
        elif name is None:
            print("name null")
            params = '?id=' + id
        else:
            print("id and name not null")
            params = '?id=' + id
            params += '&name=' + name
    url = base_url + params

    return getUrlData(url)
