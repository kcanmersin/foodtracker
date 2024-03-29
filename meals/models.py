from django.db import models
from django.conf import settings

class Meal(models.Model):
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name="meals", null=True, blank=True)

    #use useraccount
    #user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name="meals")
    date = models.DateField()
    name = models.CharField(max_length=255)  # Meal name, e.g., "Breakfast", "Lunch", etc.

    def __str__(self):
        return f"{self.name} ({self.date}) - {self.user.username}"

class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="meal_items")
    food_name = models.CharField(max_length=255)  
    quantity_g = models.PositiveIntegerField()  
    calories = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  
    protein_g = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True) 
    carbohydrates_g = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  
    fats_g = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  
    saturated_fat_g = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  
    fiber_g = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True) 
    sugar_g = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True) 
    sodium_mg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  
    cholesterol_mg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  
    potassium_mg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True) 

    def __str__(self):
        return f"{self.food_name} - {self.quantity_g}g"
