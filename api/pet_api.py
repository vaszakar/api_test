# api/pet_api.py

import requests
from config import BASE_URL

class PetAPI:
    """Class for methods working with the /pet endpoints."""
    def __init__(self):
        self.base_url = BASE_URL

    def create_pet(self, payload):
        """Method to create/update a pet (uses PUT)."""
        url = f"{self.base_url}/pet"
        response = requests.put(url, json=payload)
        return response

    def get_pet_by_id(self, pet_id):
        """Method to get pet data by its ID."""
        url = f"{self.base_url}/pet/{pet_id}"
        response = requests.get(url)
        return response

    def delete_pet(self, pet_id):
        """Method to delete a pet by its ID with authorization."""
        url = f"{self.base_url}/pet/{pet_id}"
        headers = {'api_key': 'special-key'}
        response = requests.delete(url, headers=headers)
        return response