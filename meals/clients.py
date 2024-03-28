# clients.py
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

class FatSecretBaseClient:
    BASE_URL = "https://platform.fatsecret.com/rest/server.api"
    TOKEN_URL = "https://oauth.fatsecret.com/connect/token"

    def __init__(self):
        self.client_id = settings.FATSECRET_CLIENT_ID
        self.client_secret = settings.FATSECRET_CLIENT_SECRET

    def get_access_token(self):
        payload = {"grant_type": "client_credentials"}
        try:
            response = requests.post(self.TOKEN_URL, auth=HTTPBasicAuth(self.client_id, self.client_secret), data=payload)
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.RequestException as e:
            raise Exception(f"Error obtaining access token: {e}")
