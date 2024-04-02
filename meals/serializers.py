from rest_framework import serializers
from .models import Meal, MealItem

class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        #all fields
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    meal_items = MealItemSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = [
            'id', 'user', 'date', 'name', 'total_calories', 'total_protein_g', 
            'total_carbohydrates_g', 'total_fats_g', 'total_saturated_fat_g',
            'total_polyunsaturated_fat_g', 'total_monounsaturated_fat_g',
            'total_cholesterol_mg', 'total_sodium_mg', 'total_potassium_mg',
            'total_fiber_g', 'total_sugar_g', 'meal_items'
        ]
