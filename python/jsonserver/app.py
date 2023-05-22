from fastapi import FastAPI 
from fastapi.encoders import jsonable_encoder
import requests
import json

app = FastAPI()

base_url = 'http://192.168.1.12:5000/users'

@app.get(path='/')
async def healthCheck():
    return "OK"

@app.get(path='/users')
async def getUsers():
    response = requests.get(base_url)
    return response.json()

@app.post(path='/users')
async def postUsers(id:str, name:str):
    data = dict(id=id, name=name)
    response = requests.post(base_url, json=data)
    return response.json()

@app.get(path='/getdata')
async def getData(id=None, name=None):
    if (id is None) and (name is None):
        return "id, name을 입력하세요."
    else:
        if id is None:
            params = '?name=' + name
        elif name is None:
            params = '?id=' + id
        else:
            params = '?id=' + id
            params += '&name=' + name
    url = base_url + params
    response = requests.get(url)
    return response.json()

@app.get(path='/users/{id}')
async def users_data(id=None):
    if id is None:
        return "id를 입력하세요."
    else:
        data = dict(id=id)
    response = requests.get(base_url, data)
    return response.json()

@app.put(path='/put/{id}')
async def putData(id:str, name:str):
    url = base_url + '/' + str(id)
    data = dict(id=id, name=name)
    response = requests.put(url, json=data)
    return response.json()

@app.patch(path='/patch/{id}')
async def putData(id:str, name:str):
    url = base_url + '/' + str(id)
    data = dict(name=name)
    response = requests.patch(url, json=data)
    return response.json()

@app.delete(path='/delete/{id}')
async def putData(id:str):
    url = base_url + '/' + str(id)
    data = dict(id=id)
    response = requests.delete(url, json=data)
    response = requests.get(base_url)
    return response.json()
