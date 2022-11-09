import requests
import json
from django.conf import settings


def verify_id(nin):
    url = "https://api.verified.africa/sfx-verify/v3/id-service/"

    headers = {
        'Content-type': 'application/json', 
        "userid" : settings.USER_ID,
        "apiKey": settings.API_KEY
    } 

    body = {
        "searchParameter": nin, # "02730846093"
        "verificationType": "NIN-SEARCH"
    }
    response = requests.post(url,  headers=headers, data=json.dumps(body))

    data = response.json()
    return data

# print(verify_id("02730846093"))