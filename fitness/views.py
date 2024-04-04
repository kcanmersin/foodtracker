# fitness/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import WgerService
import requests
from rest_framework.permissions import AllowAny
class ExerciseListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        service = WgerService()
        exercises = service.get_exercises()
        return Response(exercises)

# Add more views as needed.
