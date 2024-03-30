from rest_framework import serializers
from .models import Meal, MealItem

class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = [
            'id', 'meal', 'food_name', 'quantity_g', 'quantity_oz', 'quantity_number',
            'calories', 'protein_g', 'carbohydrates_g', 'fats_g', 'saturated_fat_g',
            'polyunsaturated_fat_g', 'monounsaturated_fat_g', 'cholesterol_mg',
            'sodium_mg', 'potassium_mg', 'fiber_g', 'sugar_g', 'vitamin_a_mg',
            'vitamin_c_mg', 'calcium_mg', 'iron_mg'
        ]

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
