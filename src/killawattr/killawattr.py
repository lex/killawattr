import requests
from requests.auth import HTTPBasicAuth


class Killawattr:
    def __init__(self, api_url, username, password):
        self.api_url = api_url
        self.username = username
        self.password = password

    def fetch_data(self, filename):
        auth = HTTPBasicAuth(self.username, self.password)
        headers = {'Content-type': 'application/json'}
        response = requests.get(
            f'{self.api_url}/{filename}', auth=auth, headers=headers)

        if response.status_code != 200:
            return None

        return response.json()
