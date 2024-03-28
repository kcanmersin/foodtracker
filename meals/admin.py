from django.contrib import admin
from .models import Meal, MealItem

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'user']
    list_filter = ['date', 'user']

@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'quantity_g', 'meal']
    list_filter = ['meal']
