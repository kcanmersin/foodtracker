# meals/urls.py
from django.urls import path
from .externalAPIviews import FoodBrandsAPIView, FoodSubCategoriesAPIView, FoodsSearchV3APIView, NutritionInfoAPIView, CategoriesAPIView, FoodsSearchAPIView, FoodDetailsAPIView
from . import views  # import the views module from the current package
from .views import MealListCreateAPIView, MealDetailAPIView, MealItemListCreateAPIView ,MealItemDetailAPIView
from . import externalAPIviews
from rest_framework.views import APIView

urlpatterns = [
    path('nutrition/', NutritionInfoAPIView.as_view(), name='nutrition-info'),
    path('categories/', CategoriesAPIView.as_view(), name='categories'),
    path('foods/search/', FoodsSearchAPIView.as_view(), name='foods-search'),
    path('food/details/<int:food_id>/', FoodDetailsAPIView.as_view(), name='food-details'),
      path('categories/subcategories/<int:food_category_id>/', FoodSubCategoriesAPIView.as_view(), name='food-sub-categories'),

        path('foods/search/v3/', FoodsSearchV3APIView.as_view(), name='foods-search-v3'),

      path('food_brands/', FoodBrandsAPIView.as_view(), name='food_brands'),


    path('meals/', MealListCreateAPIView.as_view(), name='meal-list-create'),
    path('meals/<int:pk>/', MealDetailAPIView.as_view(), name='meal-detail'),
    # path('meals/<int:meal_id>/items/quantity/<float:quantity>/multiplier/<float:quantity>', MealItemListCreateAPIView.as_view(), name='mealitem-list-create'),
      path('meals/<int:meal_id>/items/type/<str:type>/multiplier/<str:multiplier>/', MealItemListCreateAPIView.as_view(), name='mealitem-list-create'),

    path('mealitems/<int:pk>/', MealItemDetailAPIView.as_view(), name='mealitem-detail'),



]
