import pytest
from api.services.store_service import StoreService
from api.services.pet_service import PetService
from api.utils.factories import make_pet, make_order


@pytest.fixture
def store_svc():
    return StoreService()


@pytest.fixture
def pet_svc():
    return PetService()


@pytest.fixture
def order(store_svc, pet_svc):
    pet_payload = make_pet()
    pet_svc.create(pet_payload)
    order_payload = make_order(pet_payload["id"])
    store_svc.create_order(order_payload)
    yield order_payload, pet_payload
    store_svc.delete_order(order_payload["id"])
    pet_svc.delete(pet_payload["id"])


@pytest.mark.api
class TestStoreCRUD:
    def test_get_inventory_returns_200(self, store_svc):
        response = store_svc.get_inventory()
        assert response.status_code == 200

    def test_inventory_returns_dict(self, store_svc):
        response = store_svc.get_inventory()
        assert isinstance(response.json(), dict)

    def test_create_order_returns_200(self, store_svc, pet_svc):
        pet_payload = make_pet()
        pet_svc.create(pet_payload)
        order_payload = make_order(pet_payload["id"])
        response = store_svc.create_order(order_payload)
        assert response.status_code == 200
        store_svc.delete_order(order_payload["id"])
        pet_svc.delete(pet_payload["id"])

    def test_create_order_returns_correct_pet_id(self, store_svc, pet_svc):
        pet_payload = make_pet()
        pet_svc.create(pet_payload)
        order_payload = make_order(pet_payload["id"])
        response = store_svc.create_order(order_payload)
        assert response.json()["petId"] == pet_payload["id"]
        store_svc.delete_order(order_payload["id"])
        pet_svc.delete(pet_payload["id"])

    def test_get_order_by_id(self, store_svc, order):
        order_payload, _ = order
        response = store_svc.get_order(order_payload["id"])
        assert response.status_code == 200
        assert response.json()["id"] == order_payload["id"]

    def test_delete_order_returns_200(self, store_svc, pet_svc):
        pet_payload = make_pet()
        pet_svc.create(pet_payload)
        order_payload = make_order(pet_payload["id"])
        store_svc.create_order(order_payload)
        response = store_svc.delete_order(order_payload["id"])
        assert response.status_code == 200
        pet_svc.delete(pet_payload["id"])

    def test_get_nonexistent_order_returns_404(self, store_svc):
        response = store_svc.get_order(999999999)
        assert response.status_code == 404
