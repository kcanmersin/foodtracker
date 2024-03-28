# views.py
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
import requests , os
from requests.auth import HTTPBasicAuth
from .models import Meal
from .serializers import MealSerializer
#import oauthsession
from requests_oauthlib import OAuth1Session
from datetime import timedelta
#import allowany
from rest_framework.permissions import AllowAny


# FatSecret API credentials
FATSECRET_CLIENT_ID = os.getenv('FATSECRET_CLIENT_ID')
FATSECRET_CLIENT_SECRET = os.getenv('FATSECRET_CLIENT_SECRET')
def get_access_token():
    token_url = "https://oauth.fatsecret.com/connect/token"
    payload = {"grant_type": "client_credentials"}
    try:
        response = requests.post(token_url, auth=HTTPBasicAuth(settings.FATSECRET_CLIENT_ID, settings.FATSECRET_CLIENT_SECRET), data=payload)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        print(f"Error obtaining access token: {e}")
        return None

def get_nutrition_info(access_token, query):
    api_url = "https://platform.fatsecret.com/rest/server.api"
    params = {
        "method": "foods.search",
        "format": "json",
        "search_expression": query
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching nutrition info: {e}")
        return {}

class NutritionInfoAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({'error': 'A query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = get_access_token()
        if not access_token:
            return Response({'error': 'Could not obtain access token.'}, status=status.HTTP_401_UNAUTHORIZED)

        nutrition_info = get_nutrition_info(access_token, query)
        if 'error' in nutrition_info:
            return Response({'error': 'Failed to fetch nutrition info.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(nutrition_info, status=status.HTTP_200_OK)

class MealListCreateAPIView(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Ensure to add URL patterns in urls.py to link these views
class GetCategoriesAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        access_token = get_access_token()
        if not access_token:
            return Response({'error': 'Could not obtain access token.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Define the API endpoint for getting categories
        api_url = "https://platform.fatsecret.com/rest/server.api"
        params = {
            "method": "food_categories.get.v2",  # Specify the correct API method for fetching categories
            "format": "json"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            categories = response.json()  # You might need to adjust this based on the actual response structure
            return Response(categories, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            print(f"Error fetching food categories: {e}")
            return Response({'error': 'Failed to fetch food categories.'}, status=status.HTTP_400_BAD_REQUEST)

class FoodsSearchAPIView(APIView):
    permission_classes =  [permissions.AllowAny]

    def get_access_token(self):
        token_url = "https://oauth.fatsecret.com/connect/token"
        auth = (settings.FATSECRET_CLIENT_ID, settings.FATSECRET_CLIENT_SECRET)
        data = {'grant_type': 'client_credentials'}
        response = requests.post(token_url, auth=auth, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        return None

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if not query:
            return Response({'error': 'Query parameter is required'}, status=400)

        access_token = self.get_access_token()
        if not access_token:
            return Response({'error': 'Failed to obtain access token'}, status=401)

        search_url = "https://platform.fatsecret.com/rest/server.api"
        params = {
            'method': 'foods.search',
            'search_expression': query,
            'format': 'json'
        }
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Failed to fetch data from FatSecret API'}, status=response.status_code)
class FoodsSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        if not query:
            return Response({'error': 'Query parameter is required'}, status=400)

        access_token = get_access_token()
        if not access_token:
            return Response({'error': 'Failed to obtain access token'}, status=401)

        search_url = "https://platform.fatsecret.com/rest/server.api"
        params = {
            'method': 'foods.search',
            'search_expression': query,
            'format': 'json'
        }
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Failed to fetch data from FatSecret API'}, status=response.status_code)

class FoodDetailsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, food_id):
        access_token = get_access_token()
        if not access_token:
            return Response({'error': 'Could not obtain access token.'}, status=401)

        # Construct the request to the FatSecret API
        api_url = "https://platform.fatsecret.com/rest/server.api"
        params = {
            "method": "food.get.v4",
            "food_id": food_id,
            "format": "json"
        }
        headers = {"Authorization": f"Bearer {access_token}"}

        # Make the request to the FatSecret API
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            # Successful response
            return Response(response.json())
        else:
            # Handle errors
            return Response({'error': 'Failed to fetch food details from FatSecret API'}, status=response.status_code)