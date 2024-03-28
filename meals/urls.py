from django.urls import path
from .views import NutritionInfoAPIView , MealListCreateAPIView , GetCategoriesAPIView

urlpatterns = [
    path('api/nutrition/', NutritionInfoAPIView.as_view(), name='nutrition-info'),
    path('meals/', MealListCreateAPIView.as_view(), name='meal-list-create'),
    path('categories/', GetCategoriesAPIView.as_view(), name='get-categories'),
]
