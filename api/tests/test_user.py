import pytest
from api.services.user_service import UserService
from api.utils.factories import make_user
from api.models.user_model import UserSchema


@pytest.fixture
def svc():
    return UserService()


@pytest.fixture
def user(svc):
    payload = make_user()
    svc.create(payload)
    yield payload
    svc.delete(payload["username"])


@pytest.mark.api
class TestUserCRUD:
    def test_create_returns_200(self, svc):
        payload = make_user()
        response = svc.create(payload)
        assert response.status_code == 200
        svc.delete(payload["username"])

    def test_get_by_username_returns_200(self, svc, user):
        response = svc.get_by_username(user["username"])
        assert response.status_code == 200
        assert response.json()["username"] == user["username"]

    def test_get_nonexistent_user_returns_404(self, svc):
        response = svc.get_by_username("nonexistent_user_xyz_abc_987")
        assert response.status_code == 404

    def test_update_user_first_name(self, svc, user):
        user["firstName"] = "Updated"
        response = svc.update(user["username"], user)
        assert response.status_code == 200

    def test_delete_returns_200(self, svc):
        payload = make_user()
        svc.create(payload)
        response = svc.delete(payload["username"])
        assert response.status_code == 200

    def test_login_returns_200(self, svc, user):
        response = svc.login(user["username"], user["password"])
        assert response.status_code == 200

    def test_login_response_contains_token(self, svc, user):
        response = svc.login(user["username"], user["password"])
        body = response.json()
        assert "message" in body
        assert "logged in user session" in body["message"].lower()

    def test_response_has_required_fields(self, svc, user):
        response = svc.get_by_username(user["username"])
        assert UserSchema.REQUIRED_FIELDS.issubset(response.json().keys())
