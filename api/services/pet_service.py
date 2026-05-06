import os
import requests

_BASE = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")


class PetService:
    def __init__(self):
        self._url = f"{_BASE}/pet"

    def create(self, payload: dict) -> requests.Response:
        return requests.post(self._url, json=payload)

    def get_by_id(self, pet_id: int) -> requests.Response:
        return requests.get(f"{self._url}/{pet_id}")

    def update(self, payload: dict) -> requests.Response:
        return requests.put(self._url, json=payload)

    def delete(self, pet_id: int) -> requests.Response:
        return requests.delete(f"{self._url}/{pet_id}")

    def find_by_status(self, status: str) -> requests.Response:
        return requests.get(f"{self._url}/findByStatus", params={"status": status})
