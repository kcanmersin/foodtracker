# fitness/urls.py
from django.urls import path
from . import views
from .externalAPIviews import  ExerciseSearchView
#corrected the import statement



urlpatterns = [
    path('exercises/', views.ExerciseListView.as_view(), name='exercise-list'),
 path('exercises/search/', ExerciseSearchView.as_view(), name='exercise-search'),
    
   
    # Add more URL patterns for other views.
]
