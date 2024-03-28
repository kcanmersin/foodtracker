from django.urls import path
from .views import NutritionInfoAPIView , MealListCreateAPIView , GetCategoriesAPIView , FoodsSearchAPIView,FoodDetailsAPIView

urlpatterns = [
    path('api/nutrition/', NutritionInfoAPIView.as_view(), name='nutrition-info'),
    path('meals/', MealListCreateAPIView.as_view(), name='meal-list-create'),
    path('categories/', GetCategoriesAPIView.as_view(), name='get-categories'),
    path('foods/search/', FoodsSearchAPIView.as_view(), name='foods_search'),
    path('foods/details/<int:food_id>/', FoodDetailsAPIView.as_view(), name='food_details'),
]
