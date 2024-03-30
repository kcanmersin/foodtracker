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




    def get_food_details(self, food_id):
        access_token = self.get_access_token()
        if not access_token:
            return {"error": "Could not obtain access token."}

        params = {
            "method": "food.get.v4",
            "food_id": food_id,
            "format": "json"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.client.BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception("Failed to fetch food details.")

        data = response.json()
        
        # Bu kısımda açıklamaların başlangıcında belirli ifadeler olup olmadığını kontrol etmek için bir liste belirliyoruz
        allowed_start_words = ["1 medium", "1 small", "1 oz", "100 g"]

        if 'food' in data and 'servings' in data['food'] and 'serving' in data['food']['servings']:
            data['food']['servings']['serving'] = [
                serving for serving in data['food']['servings']['serving']
                if any(serving['serving_description'].startswith(word) for word in allowed_start_words)
            ]

        return data

    def get_food_sub_categories(self, food_category_id):
        access_token = self.get_access_token()
        if not access_token:
            raise Exception("Could not obtain access token.")

        params = {
            "method": "food_sub_categories.get.v2",
            "food_category_id": food_category_id,
            "format": "json"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.client.BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception("Failed to fetch food sub categories.")

        return response.json()
    def get_all_food_brands(self, starts_with="*", brand_type="manufacturer"):
        access_token = self.get_access_token()
        if not access_token:
            raise Exception("Could not obtain access token.")
        
        params = {
            "method": "food_brands.get.v2",
            "starts_with": starts_with,
            "brand_type": brand_type,
            "format": "json"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.client.BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception("Failed to fetch food brands.")

        return response.json()
    def search_foods_v3(self, search_expression, page_number=0, max_results=20, include_sub_categories=False, include_food_images=False, include_food_attributes=False, flag_default_serving=False):
        access_token = self.get_access_token()
        if not access_token:
            raise Exception("Could not obtain access token.")

        params = {
            "method": "foods.search.v3",  # The method is specified here as a parameter, not in the URL
            "search_expression": search_expression,
            "page_number": str(page_number),
            "max_results": str(max_results),
            "include_sub_categories": str(include_sub_categories).lower(),
            "include_food_images": str(include_food_images).lower(),
            "include_food_attributes": str(include_food_attributes).lower(),
            "flag_default_serving": str(flag_default_serving).lower(),
            "format": "json"
        }
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(self.client.BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception("Failed to search foods with v3 API. Error: " + response.text)

        return response.json()
    def search_foods(self, query):
        access_token = self.get_access_token()
        if not access_token:
            return {"error": "Could not obtain access token."}

        params = {
            'method': 'foods.search',
            'search_expression': query,
            'format': 'json'
        }
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.client.BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception("Failed to fetch data from FatSecret API")

        # Parse the JSON response
        data = response.json()

        # Filter out 'Brand' food types
        if 'foods' in data and 'food' in data['foods']:
            data['foods']['food'] = [food for food in data['foods']['food'] if food.get('food_type') != 'Brand']

        return data