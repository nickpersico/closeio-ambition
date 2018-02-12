import json
import urllib
import requests


def upload_data_to_ambition(endpoint, payload, auth_token):

    response = requests.post(
        endpoint,
        headers = {
            'Authorization': 'Token {0}'.format(auth_token),
            'Content-Type': 'application/json',
        },
        data=payload
    )

    return response.json
