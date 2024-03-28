# meals/urls.py
from django.urls import path
from .views import NutritionInfoAPIView, CategoriesAPIView, FoodsSearchAPIView, FoodDetailsAPIView

urlpatterns = [
    path('nutrition/', NutritionInfoAPIView.as_view(), name='nutrition-info'),
    path('categories/', CategoriesAPIView.as_view(), name='categories'),
    path('foods/search/', FoodsSearchAPIView.as_view(), name='foods-search'),
    path('food/details/<int:food_id>/', FoodDetailsAPIView.as_view(), name='food-details'),
]
