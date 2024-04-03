import datetime
from decimal import Decimal
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Meal, MealItem
from .serializers import MealSerializer, MealItemSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .services import FatSecretService
#import f
from django.db.models import F
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


from decimal import Decimal, InvalidOperation

class MealItemCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, meal_id, food_id, q_type, multiplier):
        meal = get_object_or_404(Meal, id=meal_id)
        service = FatSecretService()

        try:
            # `multiplier`'ı Decimal'e çevir
            multiplier = Decimal(multiplier)
            # Gıda detaylarını servisten al
            food_details = service.get_food_details(food_id)
            print(food_details)
            # Gıda detaylarından ilgili serving bilgisini bul
            serving_found = False
            for serving in food_details['food']['servings']['serving']:
                if serving['measurement_description'].lower().startswith(q_type.lower()):
                    serving_found = True
                    break
            
            if not serving_found:
                return Response({'error': f"{q_type} serving type not found for this food."}, status=404)

            def calculate_value(key):
                try:
                    return Decimal(serving.get(key, 0)) * multiplier
                except InvalidOperation:
                    return Decimal(0)

            # MealItem oluşturma
            meal_item = MealItem.objects.create(
                meal=meal,
                food_name=food_details['food']['food_name'],
                q_type=q_type,
                quantity=multiplier,
                calories=calculate_value('calories'),
                protein_g=calculate_value('protein'),
                carbohydrates_g=calculate_value('carbohydrate'),
                fats_g=calculate_value('fat'),
                saturated_fat_g=calculate_value('saturated_fat'),
                polyunsaturated_fat_g=calculate_value('polyunsaturated_fat'),
                monounsaturated_fat_g=calculate_value('monounsaturated_fat'),
                cholesterol_mg=calculate_value('cholesterol'),
                sodium_mg=calculate_value('sodium'),
                potassium_mg=calculate_value('potassium'),
                fiber_g=calculate_value('fiber'),
                sugar_g=calculate_value('sugar'),
                vitamin_a_mg=calculate_value('vitamin_a'),
                vitamin_c_mg=calculate_value('vitamin_c'),
                calcium_mg=calculate_value('calcium'),
                iron_mg=calculate_value('iron'),
            )
            # Update Meal nutritional totals
            meal.total_calories = F('total_calories') + meal_item.calories
            meal.total_protein_g = F('total_protein_g') + meal_item.protein_g
            meal.total_carbohydrates_g = F('total_carbohydrates_g') + meal_item.carbohydrates_g
            meal.total_fats_g = F('total_fats_g') + meal_item.fats_g
            meal.total_saturated_fat_g = F('total_saturated_fat_g') + (meal_item.saturated_fat_g or 0)
            meal.total_polyunsaturated_fat_g = F('total_polyunsaturated_fat_g') + (meal_item.polyunsaturated_fat_g or 0)
            meal.total_monounsaturated_fat_g = F('total_monounsaturated_fat_g') + (meal_item.monounsaturated_fat_g or 0)
            meal.total_cholesterol_mg = F('total_cholesterol_mg') + (meal_item.cholesterol_mg or 0)
            meal.total_sodium_mg = F('total_sodium_mg') + (meal_item.sodium_mg or 0)
            meal.total_potassium_mg = F('total_potassium_mg') + (meal_item.potassium_mg or 0)
            meal.total_fiber_g = F('total_fiber_g') + (meal_item.fiber_g or 0)
            meal.total_sugar_g = F('total_sugar_g') + (meal_item.sugar_g or 0)
            meal.total_vitamin_a_mg = F('total_vitamin_a_mg') + (meal_item.vitamin_a_mg or 0)
            meal.total_vitamin_c_mg = F('total_vitamin_c_mg') + (meal_item.vitamin_c_mg or 0)
            meal.total_calcium_mg = F('total_calcium_mg') + (meal_item.calcium_mg or 0)
            meal.total_iron_mg = F('total_iron_mg') + (meal_item.iron_mg or 0)

            meal.save(update_fields=[
                'total_calories', 'total_protein_g', 'total_carbohydrates_g', 'total_fats_g',
                'total_saturated_fat_g', 'total_polyunsaturated_fat_g', 'total_monounsaturated_fat_g',
                'total_cholesterol_mg', 'total_sodium_mg', 'total_potassium_mg', 'total_fiber_g',
                'total_sugar_g', 'total_vitamin_a_mg', 'total_vitamin_c_mg', 'total_calcium_mg',
                'total_iron_mg'
            ])

            meal.save()

            return Response(MealItemSerializer(meal_item).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=400)
def safe_subtract(current_value, subtract_value):
    current = current_value if current_value is not None else Decimal('0.00')
    subtract = subtract_value if subtract_value is not None else Decimal('0.00')
    result = current - subtract
    return max(result, Decimal('0.00'))
class MealItemDeleteAPIView(APIView):

    permission_classes = [AllowAny]

    def delete(self, request, meal_id, mealitem_id):
        meal_item = get_object_or_404(MealItem, id=mealitem_id, meal_id=meal_id)
        meal = get_object_or_404(Meal, id=meal_id)
        
        meal.total_calories = safe_subtract(meal.total_calories, meal_item.calories)
        meal.total_protein_g = safe_subtract(meal.total_protein_g, meal_item.protein_g)
        meal.total_carbohydrates_g = safe_subtract(meal.total_carbohydrates_g, meal_item.carbohydrates_g)
        meal.total_fats_g = safe_subtract(meal.total_fats_g, meal_item.fats_g)
        meal.total_saturated_fat_g = safe_subtract(meal.total_saturated_fat_g, meal_item.saturated_fat_g)
        meal.total_polyunsaturated_fat_g = safe_subtract(meal.total_polyunsaturated_fat_g, meal_item.polyunsaturated_fat_g)
        meal.total_monounsaturated_fat_g = safe_subtract(meal.total_monounsaturated_fat_g, meal_item.monounsaturated_fat_g)
        meal.total_cholesterol_mg = safe_subtract(meal.total_cholesterol_mg, meal_item.cholesterol_mg)
        meal.total_sodium_mg = safe_subtract(meal.total_sodium_mg, meal_item.sodium_mg)
        meal.total_potassium_mg = safe_subtract(meal.total_potassium_mg, meal_item.potassium_mg)
        meal.total_fiber_g = safe_subtract(meal.total_fiber_g, meal_item.fiber_g)
        meal.total_sugar_g = safe_subtract(meal.total_sugar_g, meal_item.sugar_g)
        meal.total_vitamin_a_mg = safe_subtract(meal.total_vitamin_a_mg, meal_item.vitamin_a_mg)
        meal.total_vitamin_c_mg = safe_subtract(meal.total_vitamin_c_mg, meal_item.vitamin_c_mg)
        meal.total_calcium_mg = safe_subtract(meal.total_calcium_mg, meal_item.calcium_mg)
        meal.total_iron_mg = safe_subtract(meal.total_iron_mg, meal_item.iron_mg)

        meal.save()

        meal_item.delete()

        return Response({'message': 'Meal item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
class MealItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MealItem.objects.all()
    serializer_class = MealItemSerializer
    permission_classes = [AllowAny]


class UserMealsByDateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id, year, month, day):
        date = datetime.date(year, month, day)
        meals = Meal.objects.filter(user_id=user_id, date=date)
        # Correctly instantiate the serializer with `instance=meals` and `many=True`
        serializer = MealSerializer(instance=meals, many=True)
        return Response(serializer.data)

class UserMealsByMonthAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id, year, month):
        meals = Meal.objects.filter(user_id=user_id, date__year=year, date__month=month)
        serializer = MealSerializer(instance=meals, many=True)
        return Response(serializer.data)
