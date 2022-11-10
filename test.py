import requests
import json

headers = {
    'Content-type': 'application/json'
} 

body =  {"nin": "22330019181"}

response = requests.post(url="http://127.0.0.1:8000/api/v1/auth/verify", data=body)
print(response)