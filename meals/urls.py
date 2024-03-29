# meals/urls.py
from django.urls import path
from .externalAPIviews import FoodSubCategoriesAPIView, FoodsSearchV3APIView, NutritionInfoAPIView, CategoriesAPIView, FoodsSearchAPIView, FoodDetailsAPIView
from . import views 
from . import externalAPIviews
from rest_framework.views import APIView

urlpatterns = [
    path('nutrition/', NutritionInfoAPIView.as_view(), name='nutrition-info'),
    path('categories/', CategoriesAPIView.as_view(), name='categories'),
    path('foods/search/', FoodsSearchAPIView.as_view(), name='foods-search'),
    path('food/details/<int:food_id>/', FoodDetailsAPIView.as_view(), name='food-details'),
      path('food-sub-categories/<int:food_category_id>/', FoodSubCategoriesAPIView.as_view(), name='food-sub-categories'),

        path('foods/search/v3/', FoodsSearchV3APIView.as_view(), name='foods-search-v3'),





    path('meals/', views.MealListCreateAPIView.as_view(), name='meal-list-create'),
    path('meals/<int:pk>/', views.MealDetailAPIView.as_view(), name='meal-detail'),
    path('meals/<int:meal_id>/items/', views.MealItemListCreateAPIView.as_view(), name='mealitem-list-create'),
    path('mealitems/<int:pk>/', views.MealItemDetailAPIView.as_view(), name='mealitem-detail'),

]
