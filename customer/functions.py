from django.http.request import HttpHeaders
import requests
from requests.auth import HTTPBasicAuth
import json
base_url = 'https://api.razorpay.com/v1/'


def send_request(path, auth={}, payload={}, header=None):
    header = {"Accept": "*/*",
              "Content-Type": "application/json"}
    try:
        response = requests.post(base_url+path, auth=HTTPBasicAuth(
            auth['username'], auth['password']), data=payload, verify=True, headers=header)
        response = json.loads(response.text)
        print(response)
    except Exception as e:
        print(e)
        response = {
            'error': True,
            'message': str(e)
        }
    return response
