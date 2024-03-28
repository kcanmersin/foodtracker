from django.db import models
from django.conf import settings

class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meals")
    date = models.DateField()
    name = models.CharField(max_length=255)  # Öğün adı, örneğin "Kahvaltı", "Öğle Yemeği" vs.

    def __str__(self):
        return f"{self.name} ({self.date}) - {self.user.username}"

class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="meal_items")
    food_name = models.CharField(max_length=255)  # Yemek adı
    quantity_g = models.PositiveIntegerField()  # Yemek miktarı (gram cinsinden)
    calories = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Kalori (API'den çekilecek)
    protein_g = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Protein (API'den çekilecek)
    carbohydrates_g = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Karbonhidrat (API'den çekilecek)
    fats_g = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Yağ (API'den çekilecek)

    def __str__(self):
        return f"{self.food_name} - {self.quantity_g}g"
