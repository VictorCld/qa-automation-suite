import uuid
import random


def make_pet(name: str = "Doggo", status: str = "available") -> dict:
    return {
        "id": random.randint(100000, 999999),
        "name": name,
        "status": status,
        "photoUrls": ["https://example.com/photo.jpg"],
        "category": {"id": 1, "name": "Dogs"},
        "tags": [{"id": 1, "name": "tag1"}],
    }


def make_user(username: str = None) -> dict:
    suffix = uuid.uuid4().hex[:8]
    _username = username or f"user_{suffix}"
    return {
        "id": random.randint(100000, 999999),
        "username": _username,
        "firstName": "Test",
        "lastName": "User",
        "email": f"{_username}@test.com",
        "password": "testpassword",
        "phone": "1234567890",
        "userStatus": 1,
    }


def make_order(pet_id: int) -> dict:
    return {
        "id": random.randint(1, 10),
        "petId": pet_id,
        "quantity": 1,
        "status": "placed",
        "complete": False,
    }
