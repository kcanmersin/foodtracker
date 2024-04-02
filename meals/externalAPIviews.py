# meals/views.py
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .services import FatSecretService
from rest_framework.views import APIView

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
class FoodSubCategoriesAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, food_category_id):
        try:
            service = FatSecretService()
            sub_categories = service.get_food_sub_categories(food_category_id)
            return Response(sub_categories)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class FoodsSearchV3APIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        search_expression = request.query_params.get('search_expression', '')
        page_number = request.query_params.get('page_number', 0)
        max_results = request.query_params.get('max_results', 20)
        include_sub_categories = request.query_params.get('include_sub_categories', 'true').lower() == 'true'
        include_food_images = request.query_params.get('include_food_images', 'true').lower() == 'true'
        include_food_attributes = request.query_params.get('include_food_attributes', 'false').lower() == 'true'
        flag_default_serving = request.query_params.get('flag_default_serving', 'false').lower() == 'true'

        service = FatSecretService()
        try:
            search_results = service.search_foods_v3(search_expression, page_number, max_results, include_sub_categories, include_food_images, include_food_attributes, flag_default_serving)
            return Response(search_results)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class FoodBrandsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        starts_with = request.query_params.get('starts_with', '*')
        brand_type = request.query_params.get('brand_type', 'manufacturer')
        
        service = FatSecretService()
        try:
            brands = service.get_all_food_brands(starts_with=starts_with, brand_type=brand_type)
            return Response(brands)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
