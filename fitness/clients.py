import requests

class WgerBaseClient:
    def __init__(self):
        self.base_url = "https://wger.de/api/v2"
        self.headers = {"accept": "application/json"}  # Add additional headers if necessary, e.g., Authentication

    def make_request(self, endpoint, params=None):
        full_url = f"{self.base_url}/{endpoint}"
        response = requests.get(full_url, headers=self.headers, params=params)
        response.raise_for_status()  # This will raise an error for non-2xx responses
        return response.json()
