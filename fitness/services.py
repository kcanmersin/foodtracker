# fitness/services.py
from .clients import WgerBaseClient

class WgerService:
    def __init__(self):
        self.client = WgerBaseClient()

    def get_exercises(self):
        """Retrieve a list of exercises."""
        return self.client.make_request('exercise', params={'language': 2, 'status': 2})  # English and Approved

    def get_exercise_info(self, exercise_id):
        """Retrieve detailed information about a specific exercise."""
        return self.client.make_request(f'exerciseinfo/{exercise_id}')

    def search_exercises(self, search_term):
        """Search for exercises by term."""
        return self.client.make_request('exercise/search', params={'term': search_term})

    # Add more methods for other endpoints you're interested in.
