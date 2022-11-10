import requests
import json

headers = {
    'Content-type': 'application/json'
} 

body =  {"nin": "22330019181"}

response = requests.get(url="https://cella-api.herokuapp.com/api/v1/auth/hello", data=body)
print(response)