import requests
import json
from django.conf import settings


def verify_id(nin):
    url = "https://api.verified.africa/sfx-verify/v3/id-service/"

    headers = {
        'Content-type': 'application/json', 
        "userid" : '1667948304746',
        "apiKey": 'DTHswgJl1K3roPN5FeVp'
    } 

    body = {
        "searchParameter": nin, # "02730846093"
        "verificationType": "NIN-SEARCH"
    }
    response = requests.post(url,  headers=headers, data=json.dumps(body))

    data = response.json()
    return data
    