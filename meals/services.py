# services.py
from .clients import FatSecretBaseClient
# request 
import requests
class FatSecretService:
    def __init__(self):
        self.client = FatSecretBaseClient()
    def get_access_token(self):
        return self.client.get_access_token()
    def get_nutrition_info(self, query):
        access_token = self.get_access_token()
        if not access_token:
            raise Exception("Could not obtain access token.")

        params = {
            "method": "foods.search",
            "format": "json",
            "search_expression": query
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.client.BASE_URL, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch nutrition info.")
        return response.json()

    def get_categories(self):
        access_token = self.get_access_token()
        if not access_token:
            raise Exception("Could not obtain access token.")

        params = {
            "method": "food_categories.get.v2",
            "format": "json"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.client.BASE_URL, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch categories.")
        return response.json()

    def search_foods(self, query):
        access_token = self.get_access_token()
        if not access_token:
            raise Exception("Could not obtain access token.")

        params = {
            "method": "foods.search",
            "format": "json",
            "search_expression": query
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.client.BASE_URL, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Failed to search foods.")
        return response.json()

    def get_food_details(self, food_id):
        access_token = self.get_access_token()
        if not access_token:
            raise Exception("Could not obtain access token.")

        params = {
            "method": "food.get.v4",
            "food_id": food_id,
            "format": "json"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.client.BASE_URL, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch food details.")
        return response.json()

    # Implement other methods as needed, following the same pattern
