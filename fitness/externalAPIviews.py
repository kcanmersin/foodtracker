# fitness/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import WgerService

class ExerciseListView(APIView):
    def get(self, request):
        service = WgerService()
        exercises = service.get_exercises()
        return Response(exercises)

# Add more views as needed.
