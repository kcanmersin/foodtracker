from decimal import Decimal
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Meal, MealItem
from .serializers import MealSerializer, MealItemSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .services import FatSecretService

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

            meal.save()

            return Response(MealItemSerializer(meal_item).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=400)

class MealItemDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, meal_id, mealitem_id):
        meal_item = get_object_or_404(MealItem, id=mealitem_id, meal_id=meal_id)
        
        # Silinecek MealItem'ın besin değerlerini al
        calories = meal_item.calories
        protein_g = meal_item.protein_g
        carbohydrates_g = meal_item.carbohydrates_g
        fats_g = meal_item.fats_g
        # Diğer besin değerleri de benzer şekilde alınabilir

        # MealItem'ı sil
        meal_item.delete()

        # İlgili Meal modelinde toplam besin değerlerini güncelle
        Meal.objects.filter(id=meal_id).update(
            total_calories=F('total_calories') - calories,
            total_protein_g=F('total_protein_g') - protein_g,
            total_carbohydrates_g=F('total_carbohydrates_g') - carbohydrates_g,
            total_fats_g=F('total_fats_g') - fats_g,
            # Diğer besin değerleri de benzer şekilde güncellenir
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
class MealItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MealItem.objects.all()
    serializer_class = MealItemSerializer
    permission_classes = [AllowAny]

