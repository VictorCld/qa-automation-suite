import os
import requests

_BASE = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")


class StoreService:
    def __init__(self):
        self._url = f"{_BASE}/store"

    def get_inventory(self) -> requests.Response:
        return requests.get(f"{self._url}/inventory")

    def create_order(self, payload: dict) -> requests.Response:
        return requests.post(f"{self._url}/order", json=payload)

    def get_order(self, order_id: int) -> requests.Response:
        return requests.get(f"{self._url}/order/{order_id}")

    def delete_order(self, order_id: int) -> requests.Response:
        return requests.delete(f"{self._url}/order/{order_id}")
