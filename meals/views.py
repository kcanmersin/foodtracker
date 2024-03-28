# meals/views.py
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .services import FatSecretService

class NutritionInfoAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({'error': 'A query parameter is required.'}, status=400)
        
        service = FatSecretService()
        try:
            nutrition_info = service.get_nutrition_info(query)
            return Response(nutrition_info)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class CategoriesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        service = FatSecretService()
        try:
            categories = service.get_categories()
            return Response(categories)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class FoodsSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({'error': 'Query parameter is required'}, status=400)
        
        service = FatSecretService()
        try:
            search_results = service.search_foods(query)
            return Response(search_results)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class FoodDetailsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, food_id):
        service = FatSecretService()
        try:
            food_details = service.get_food_details(food_id)
            return Response(food_details)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
