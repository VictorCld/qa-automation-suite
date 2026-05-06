import pytest
from api.services.pet_service import PetService
from api.utils.factories import make_pet
from api.models.pet_model import PetSchema


@pytest.fixture
def svc():
    return PetService()


@pytest.fixture
def pet(svc):
    payload = make_pet()
    svc.create(payload)
    yield payload
    svc.delete(payload["id"])


@pytest.mark.api
class TestPetCRUD:
    def test_create_returns_200(self, svc):
        payload = make_pet()
        response = svc.create(payload)
        assert response.status_code == 200
        svc.delete(payload["id"])

    def test_create_returns_correct_name_and_status(self, svc):
        payload = make_pet(name="Rex", status="available")
        response = svc.create(payload)
        body = response.json()
        assert body["name"] == "Rex"
        assert body["status"] == "available"
        svc.delete(payload["id"])

    def test_get_by_id_returns_200(self, svc, pet):
        response = svc.get_by_id(pet["id"])
        assert response.status_code == 200
        assert response.json()["id"] == pet["id"]

    def test_get_nonexistent_pet_returns_404(self, svc):
        response = svc.get_by_id(999999999)
        assert response.status_code == 404

    def test_update_pet_name(self, svc, pet):
        pet["name"] = "UpdatedName"
        response = svc.update(pet)
        assert response.status_code == 200
        assert response.json()["name"] == "UpdatedName"

    def test_delete_returns_200(self, svc):
        payload = make_pet()
        svc.create(payload)
        response = svc.delete(payload["id"])
        assert response.status_code == 200

    def test_find_by_status_returns_list(self, svc):
        response = svc.find_by_status("available")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_find_by_status_all_match_status(self, svc):
        response = svc.find_by_status("pending")
        assert response.status_code == 200
        for pet in response.json()[:10]:
            assert pet.get("status") == "pending"

    def test_response_has_required_fields(self, svc, pet):
        response = svc.get_by_id(pet["id"])
        assert PetSchema.REQUIRED_FIELDS.issubset(response.json().keys())
