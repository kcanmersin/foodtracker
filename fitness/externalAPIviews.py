# fitness/views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import WgerService
#import allowany
from rest_framework.permissions import AllowAny
#import status
from rest_framework import status

class ExerciseListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        service = WgerService()
        exercises = service.get_exercises()
        return Response(exercises)


class ExerciseSearchView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        language = request.query_params.get('language', 'en')
        term = request.query_params.get('term', '')

        if not term:
            return Response({"error": "The 'term' query parameter is required."}, status=400)

        service = WgerService()
        search_results = service.search_exercises(language, term)
        return Response(search_results)