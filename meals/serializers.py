# serializers.py
from rest_framework import serializers
from .models import Meal, MealItem


class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = ['id', 'food_name', 'quantity_g', 'calories', 'protein_g', 'carbohydrates_g', 'fats_g', 'saturated_fat_g', 'fiber_g', 'sugar_g', 'sodium_mg', 'cholesterol_mg', 'potassium_mg']

class MealSerializer(serializers.ModelSerializer):
    meal_items = MealItemSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'date', 'name', 'meal_items', 'user']