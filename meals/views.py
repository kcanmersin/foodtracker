from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Meal, MealItem
from .serializers import MealSerializer, MealItemSerializer
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
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [AllowAny]


class MealItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = MealItem.objects.all()
    serializer_class = MealItemSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        meal_id = self.kwargs.get('meal_id')
        quantity = self.kwargs.get('type')
        multiplier = self.kwargs.get('multiplier')
        
        try:
            quantity = float(quantity)
            multiplier = float(multiplier)
        except ValueError:
            # Handle the case where conversion to float fails
            raise ValueError("Type and multiplier must be convertible to float")

        # Calculate the total quantity based on the quantity and multiplier
        total_quantity = quantity * multiplier

        # Now you can use total_quantity as needed, for example:
        # You might want to modify the serializer.save() call to pass additional data
        serializer.save(meal_id=meal_id, quantity=total_quantity)

class MealItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MealItem.objects.all()
    serializer_class = MealItemSerializer
    permission_classes = [AllowAny]

