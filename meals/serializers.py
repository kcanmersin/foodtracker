# serializers.py
from rest_framework import serializers
from .models import Meal, MealItem

class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    meal_items = MealItemSerializer(many=True)

    class Meta:
        model = Meal
        fields = ['id', 'user', 'date', 'name', 'meal_items']
        read_only_fields = ['user']

    def create(self, validated_data):
        meal_items_data = validated_data.pop('meal_items')
        meal = Meal.objects.create(**validated_data)
        for meal_item_data in meal_items_data:
            MealItem.objects.create(meal=meal, **meal_item_data)
        return meal
