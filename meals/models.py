from django.db import models
from django.conf import settings

class Meal(models.Model):
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name="meals", null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=255)
    # Toplam besin değerleri
    total_calories = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_protein_g = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_carbohydrates_g = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_fats_g = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_saturated_fat_g = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    total_polyunsaturated_fat_g = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    total_monounsaturated_fat_g = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    total_cholesterol_mg = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    total_sodium_mg = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    total_potassium_mg = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    total_fiber_g = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    total_sugar_g = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.name} - {self.user.username}"

class MealItem(models.Model):


    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="meal_items")
    food_name = models.CharField(max_length=255)
    q_type = models.CharField(max_length=10,  default='g')  # Miktar türü: gram, ons veya adet
    quantity = models.DecimalField(max_digits=6, decimal_places=2)  # Miktar

    # Besin değerleri
    calories = models.DecimalField(max_digits=6, decimal_places=2)
    protein_g = models.DecimalField(max_digits=6, decimal_places=2)
    carbohydrates_g = models.DecimalField(max_digits=6, decimal_places=2)
    fats_g = models.DecimalField(max_digits=6, decimal_places=2)
    saturated_fat_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    polyunsaturated_fat_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    monounsaturated_fat_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    cholesterol_mg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    sodium_mg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    potassium_mg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fiber_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    sugar_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    vitamin_a_mg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    vitamin_c_mg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    calcium_mg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    iron_mg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.food_name} - {self.quantity}{self.get_type_display()}"


