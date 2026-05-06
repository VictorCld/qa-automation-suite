import os
import requests

_BASE = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")


class UserService:
    def __init__(self):
        self._url = f"{_BASE}/user"

    def create(self, payload: dict) -> requests.Response:
        return requests.post(self._url, json=payload)

    def get_by_username(self, username: str) -> requests.Response:
        return requests.get(f"{self._url}/{username}")

    def update(self, username: str, payload: dict) -> requests.Response:
        return requests.put(f"{self._url}/{username}", json=payload)

    def delete(self, username: str) -> requests.Response:
        return requests.delete(f"{self._url}/{username}")

    def login(self, username: str, password: str) -> requests.Response:
        return requests.get(
            f"{self._url}/login",
            params={"username": username, "password": password},
        )
