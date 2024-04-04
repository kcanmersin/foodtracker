# fitness/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('exercises/', views.ExerciseListView.as_view(), name='exercise-list'),
    # Add more URL patterns for other views.
]
