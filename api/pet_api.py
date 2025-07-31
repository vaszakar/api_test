# api/pet_api.py

import requests
from config import BASE_URL

class PetAPI:
    """Клас для методів, що працюють з ендпоінтами /pet."""
    def __init__(self):
        self.base_url = BASE_URL

    def create_pet(self, payload):
        """Метод для створення/оновлення тваринки (використовує PUT)."""
        url = f"{self.base_url}/pet"
        response = requests.put(url, json=payload)
        return response

    def get_pet_by_id(self, pet_id):
        """Метод для отримання даних тваринки за її ID."""
        url = f"{self.base_url}/pet/{pet_id}"
        response = requests.get(url)
        return response

    def delete_pet(self, pet_id):
        """Метод для видалення тваринки за її ID з авторизацією."""
        url = f"{self.base_url}/pet/{pet_id}"
        headers = {'api_key': 'special-key'}
        response = requests.delete(url, headers=headers)
        return response