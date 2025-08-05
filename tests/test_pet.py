# tests/test_pet.py

import pytest
import random
import json
import os
from api.pet_api import PetAPI
from jsonschema import validate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pet_api = PetAPI()

def load_pet_data():
    """Helper function to load test data from a JSON file."""
    path = os.path.join(BASE_DIR, 'test_data', 'pet_data.json')
    with open(path, 'r') as f:
        return json.load(f)


def test_get_pet_response_conforms_to_schema(created_pet_data):
    """Test that the GET /pet/{id} response conforms to the JSON schema."""
    # Arrange
    path = os.path.join(BASE_DIR, 'test_data', 'pet_schema.json')
    with open(path, 'r') as f:
        schema = json.load(f)
    pet_id = created_pet_data.get('id')
    # Act
    get_response = pet_api.get_pet_by_id(pet_id)
    assert get_response.status_code == 200
    response_data = get_response.json()
    # Assert
    validate(instance=response_data, schema=schema)


@pytest.fixture
def created_pet_data():
    """Fixture to create a pet and then delete it afterwards."""
    # SETUP
    unique_id = random.randint(100000, 999999)
    payload = {
        "id": unique_id,
        "name": f"SuperPet_{unique_id}",
        "status": "available"
    }
    create_response = pet_api.create_pet(payload)
    assert create_response.status_code == 200
    created_pet_json = create_response.json()

    yield created_pet_json

    # TEARDOWN
    pet_id_to_delete = created_pet_json.get('id')
    if pet_id_to_delete:
        print(f"\nTeardown: deleting pet {pet_id_to_delete}")
        pet_api.delete_pet(pet_id_to_delete)


@pytest.mark.parametrize("payload", load_pet_data())
def test_create_pets_from_data(payload):
    """Data-driven test that uses data from pet_data.json."""
    # Arrange
    payload['id'] = random.randint(100000, 999999)

    # Act
    response = pet_api.create_pet(payload)

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['name'] == payload['name']
    assert response_data['status'] == payload['status']

@pytest.mark.skip(reason="Skipping due to API instability")
def test_get_pet_by_id(created_pet_data):
    """Test using the fixture to verify pet retrieval by ID."""
    pet_id = created_pet_data.get('id')
    get_response = pet_api.get_pet_by_id(pet_id)
    assert get_response.status_code == 200
    response_data = get_response.json()
    assert response_data.get('id') == pet_id

@pytest.mark.skip(reason="DELETE endpoint is unstable on the public API")
def test_delete_pet():
    """Autonomous test for the deletion functionality."""
    # 1. Arrange
    unique_id = random.randint(100000, 999999)
    payload = {
        "id": unique_id,
        "name": f"PetForDelete_{unique_id}",
        "status": "available"
    }
    create_response = pet_api.create_pet(payload)
    assert create_response.status_code == 200
    pet_id = create_response.json().get('id')

    # 2. Act
    delete_response = pet_api.delete_pet(pet_id)
    assert delete_response.status_code == 200

    # 3. Assert
    get_response_after_delete = pet_api.get_pet_by_id(pet_id)
    assert get_response_after_delete.status_code == 404


@pytest.mark.parametrize("invalid_id", [99999999, "abc"], ids=["non_existent", "string"])
def test_get_pet_with_invalid_id_returns_404(invalid_id):
    """Negative test to verify error handling for invalid IDs."""
    get_response = pet_api.get_pet_by_id(invalid_id)
    assert get_response.status_code == 404
