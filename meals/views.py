# views.py
from rest_framework import generics
from .models import Meal, MealItem
from .serializers import MealSerializer, MealItemSerializer
import requests
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
class MealListCreateAPIView(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

class MealDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealItemListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = MealItem.objects.all()
    serializer_class = MealItemSerializer

    def perform_create(self, serializer):
        serializer.save(meal_id=self.kwargs.get('meal_id'))

class MealItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = MealItem.objects.all()
    serializer_class = MealItemSerializer
