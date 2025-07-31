# tests/test_pet.py

import pytest
import random
from api.pet_api import PetAPI

pet_api = PetAPI()


@pytest.fixture
def created_pet_data():
    """
    Фікстура, яка створює тваринку, а потім намагається її видалити.
    """
    # --- SETUP ---
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

    # --- TEARDOWN ---
    # Цей код виконається ПІСЛЯ тесту
    print(f"\nПрибирання: спроба видалити тваринку {created_pet_json.get('id')}")
    pet_api.delete_pet(created_pet_json.get('id'))


def test_create_pet():
    """Тест для перевірки успішного створення тваринки."""
    payload = {
        "id": random.randint(100000, 999999),
        "name": "MySuperPet",
        "status": "available"
    }
    response = pet_api.create_pet(payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['name'] == payload['name']

@pytest.mark.skip(reason="Skipping get_by_id due to API instability")
def test_get_pet_by_id(created_pet_data):
    """Тест, що використовує фікстуру для перевірки отримання."""
    pet_id = created_pet_data.get('id')
    get_response = pet_api.get_pet_by_id(pet_id)
    assert get_response.status_code == 200
    response_data = get_response.json()
    assert response_data.get('id') == pet_id

@pytest.mark.skip(reason="Skipping due to API instability")
def test_delete_pet():
    """
    Автономний тест на видалення, який не залежить від фікстури.
    """
    # 1. Створюємо тваринку спеціально для цього тесту
    unique_id = random.randint(100000, 999999)
    payload = {
        "id": unique_id,
        "name": f"PetForDelete_{unique_id}",
        "status": "available"
    }
    create_response = pet_api.create_pet(payload)
    assert create_response.status_code == 200
    pet_id = create_response.json().get('id')

    # 2. Видаляємо її
    delete_response = pet_api.delete_pet(pet_id)
    assert delete_response.status_code == 200

    # 3. Перевіряємо, що вона дійсно видалена
    get_response_after_delete = pet_api.get_pet_by_id(pet_id)
    assert get_response_after_delete.status_code == 404


@pytest.mark.parametrize("invalid_id", [99999999, "abc"], ids=["non_existent", "string"])
def test_get_pet_with_invalid_id_returns_404(invalid_id):
    """Негативний тест з невалідними ID."""
    get_response = pet_api.get_pet_by_id(invalid_id)
    assert get_response.status_code == 404