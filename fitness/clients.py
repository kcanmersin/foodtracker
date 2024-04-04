# fitness/clients.py
import requests

class WgerBaseClient:
    BASE_URL = "https://wger.de/api/v2/"

    def __init__(self):
        pass

    def make_request(self, endpoint, params=None):
        """Make a GET request to a specific Wger API endpoint."""
        url = f"{self.BASE_URL}{endpoint}/"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
