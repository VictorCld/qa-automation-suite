# Test Automation Project — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete test automation project with API (Petstore) and Web (SauceDemo) suites, GitHub Actions CI/CD, Allure reports, and Docker support — all in a single Python repository.

**Architecture:** Service Layer pattern for API tests (one service class per resource), Page Object Model for Web tests (one page class per page). Both suites use pytest with `@pytest.mark.api` / `@pytest.mark.web` markers so they can run independently or together.

**Tech Stack:** Python 3.12, pytest, requests, selenium 4, webdriver-manager, allure-pytest, python-dotenv, Docker, GitHub Actions

---

## File Map

```
test-automation-project/
├── api/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pet_model.py          # PetSchema (required fields, valid statuses)
│   │   └── user_model.py         # UserSchema (required fields)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pet_service.py        # PetService — wraps /pet endpoints
│   │   ├── user_service.py       # UserService — wraps /user endpoints
│   │   └── store_service.py      # StoreService — wraps /store endpoints
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_pet.py           # Pet CRUD + validation tests
│   │   ├── test_user.py          # User CRUD + login tests
│   │   └── test_store.py         # Store inventory + order tests
│   └── utils/
│       ├── __init__.py
│       └── factories.py          # make_pet(), make_user(), make_order()
├── web/
│   ├── __init__.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── login_page.py         # LoginPage — open() + login()
│   │   ├── inventory_page.py     # InventoryPage — add_product_to_cart() + go_to_cart()
│   │   ├── cart_page.py          # CartPage — get_item_names() + proceed_to_checkout()
│   │   └── checkout_page.py      # CheckoutPage — fill_shipping_info() + finish_order() + get_confirmation_message()
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_checkout_e2e.py  # E2E: login → cart → checkout
│   └── utils/
│       ├── __init__.py
│       └── driver_factory.py     # create_driver() — headless aware
├── .github/
│   └── workflows/
│       └── ci.yml                # Parallel API + Web jobs
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── conftest.py
├── .env.example
├── .gitignore
└── README.md
```

---

## Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `pytest.ini`
- Create: `conftest.py`
- Create: `.env.example`
- Create: `.gitignore`
- Create: all `__init__.py` files (empty)

- [ ] **Step 1: Create requirements.txt**

```
pytest==8.3.5
requests==2.32.3
selenium==4.27.1
webdriver-manager==4.0.2
allure-pytest==2.13.5
python-dotenv==1.0.1
```

- [ ] **Step 2: Create pytest.ini**

```ini
[pytest]
markers =
    api: API test suite (Petstore)
    web: Web test suite (SauceDemo)
pythonpath = .
```

- [ ] **Step 3: Create conftest.py**

```python
from dotenv import load_dotenv

load_dotenv()
```

- [ ] **Step 4: Create .env.example**

```
BASE_URL=https://petstore.swagger.io/v2
SAUCE_URL=https://www.saucedemo.com
SAUCE_USER=standard_user
SAUCE_PASSWORD=secret_sauce
HEADLESS=true
```

- [ ] **Step 5: Create .gitignore**

```
.env
__pycache__/
*.pyc
.pytest_cache/
allure-results/
allure-report/
.DS_Store
```

- [ ] **Step 6: Create all package __init__.py files (all empty)**

Paths to create:
```
api/__init__.py
api/models/__init__.py
api/services/__init__.py
api/tests/__init__.py
api/utils/__init__.py
web/__init__.py
web/pages/__init__.py
web/tests/__init__.py
web/utils/__init__.py
```

- [ ] **Step 7: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: all packages install without error.

- [ ] **Step 8: Verify pytest discovers no tests yet**

```bash
pytest --collect-only
```

Expected: `no tests ran`

- [ ] **Step 9: Commit**

```bash
git add requirements.txt pytest.ini conftest.py .env.example .gitignore api/ web/
git commit -m "feat: project scaffolding with pytest and dependencies"
```

---

## Task 2: API Models and Factories

**Files:**
- Create: `api/models/pet_model.py`
- Create: `api/models/user_model.py`
- Create: `api/utils/factories.py`

- [ ] **Step 1: Create api/models/pet_model.py**

```python
class PetSchema:
    REQUIRED_FIELDS = {"id", "name", "status", "photoUrls"}
    VALID_STATUSES = {"available", "pending", "sold"}
```

- [ ] **Step 2: Create api/models/user_model.py**

```python
class UserSchema:
    REQUIRED_FIELDS = {"id", "username", "firstName", "lastName", "email", "phone"}
```

- [ ] **Step 3: Create api/utils/factories.py**

```python
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
```

- [ ] **Step 4: Verify factories import correctly**

```bash
python -c "from api.utils.factories import make_pet, make_user, make_order; print(make_pet())"
```

Expected: prints a dict with id, name, status, photoUrls, category, tags.

- [ ] **Step 5: Commit**

```bash
git add api/models/ api/utils/factories.py
git commit -m "feat: add API models schemas and data factories"
```

---

## Task 3: API Pet Service and Tests

**Files:**
- Create: `api/services/pet_service.py`
- Create: `api/tests/test_pet.py`

- [ ] **Step 1: Create api/services/pet_service.py**

```python
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
```

- [ ] **Step 2: Create api/tests/test_pet.py**

```python
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
```

- [ ] **Step 3: Run pet tests**

```bash
pytest api/tests/test_pet.py -v
```

Expected: all 9 tests PASS (Petstore is a live public API).

- [ ] **Step 4: Commit**

```bash
git add api/services/pet_service.py api/tests/test_pet.py
git commit -m "feat: add pet service layer and CRUD tests"
```

---

## Task 4: API User Service and Tests

**Files:**
- Create: `api/services/user_service.py`
- Create: `api/tests/test_user.py`

- [ ] **Step 1: Create api/services/user_service.py**

```python
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
```

- [ ] **Step 2: Create api/tests/test_user.py**

```python
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
```

- [ ] **Step 3: Run user tests**

```bash
pytest api/tests/test_user.py -v
```

Expected: all 8 tests PASS.

- [ ] **Step 4: Commit**

```bash
git add api/services/user_service.py api/tests/test_user.py
git commit -m "feat: add user service layer and CRUD tests"
```

---

## Task 5: API Store Service and Tests

**Files:**
- Create: `api/services/store_service.py`
- Create: `api/tests/test_store.py`

- [ ] **Step 1: Create api/services/store_service.py**

```python
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
```

- [ ] **Step 2: Create api/tests/test_store.py**

```python
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
```

- [ ] **Step 3: Run store tests**

```bash
pytest api/tests/test_store.py -v
```

Expected: all 7 tests PASS.

- [ ] **Step 4: Run full API suite with marker**

```bash
pytest -m api -v
```

Expected: all 24 API tests PASS.

- [ ] **Step 5: Commit**

```bash
git add api/services/store_service.py api/tests/test_store.py
git commit -m "feat: add store service layer and inventory/order tests"
```

---

## Task 6: Web Driver Factory

**Files:**
- Create: `web/utils/driver_factory.py`

- [ ] **Step 1: Create web/utils/driver_factory.py**

```python
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    if os.getenv("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
```

- [ ] **Step 2: Verify driver instantiates (requires Chrome installed)**

```bash
python -c "from web.utils.driver_factory import create_driver; d = create_driver(); print(d.title); d.quit()"
```

Expected: prints an empty string and exits without error.

- [ ] **Step 3: Commit**

```bash
git add web/utils/driver_factory.py
git commit -m "feat: add Selenium WebDriver factory with headless support"
```

---

## Task 7: Web Page Objects

**Files:**
- Create: `web/pages/login_page.py`
- Create: `web/pages/inventory_page.py`
- Create: `web/pages/cart_page.py`
- Create: `web/pages/checkout_page.py`

- [ ] **Step 1: Create web/pages/login_page.py**

```python
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

_URL = os.getenv("SAUCE_URL", "https://www.saucedemo.com")


class LoginPage:
    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _LOGIN_BTN = (By.ID, "login-button")

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def open(self) -> None:
        self._driver.get(_URL)

    def login(self, username: str, password: str) -> None:
        self._driver.find_element(*self._USERNAME).send_keys(username)
        self._driver.find_element(*self._PASSWORD).send_keys(password)
        self._driver.find_element(*self._LOGIN_BTN).click()
```

- [ ] **Step 2: Create web/pages/inventory_page.py**

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class InventoryPage:
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _ITEMS = (By.CLASS_NAME, "inventory_item")
    _ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def add_product_to_cart(self, product_name: str) -> None:
        for item in self._driver.find_elements(*self._ITEMS):
            if item.find_element(*self._ITEM_NAME).text == product_name:
                item.find_element(By.TAG_NAME, "button").click()
                return
        raise ValueError(f"Product '{product_name}' not found")

    def go_to_cart(self) -> None:
        self._driver.find_element(*self._CART_LINK).click()
```

- [ ] **Step 3: Create web/pages/cart_page.py**

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CartPage:
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def get_item_names(self) -> list[str]:
        return [el.text for el in self._driver.find_elements(*self._ITEM_NAMES)]

    def proceed_to_checkout(self) -> None:
        self._driver.find_element(*self._CHECKOUT_BTN).click()
```

- [ ] **Step 4: Create web/pages/checkout_page.py**

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CheckoutPage:
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _ZIP_CODE = (By.ID, "postal-code")
    _CONTINUE_BTN = (By.ID, "continue")
    _FINISH_BTN = (By.ID, "finish")
    _CONFIRMATION = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def fill_shipping_info(self, first: str, last: str, zip_code: str) -> None:
        self._driver.find_element(*self._FIRST_NAME).send_keys(first)
        self._driver.find_element(*self._LAST_NAME).send_keys(last)
        self._driver.find_element(*self._ZIP_CODE).send_keys(zip_code)
        self._driver.find_element(*self._CONTINUE_BTN).click()

    def finish_order(self) -> None:
        self._driver.find_element(*self._FINISH_BTN).click()

    def get_confirmation_message(self) -> str:
        return self._driver.find_element(*self._CONFIRMATION).text
```

- [ ] **Step 5: Commit**

```bash
git add web/pages/
git commit -m "feat: add Page Object Model — login, inventory, cart, checkout pages"
```

---

## Task 8: Web E2E Tests

**Files:**
- Create: `web/tests/test_checkout_e2e.py`

- [ ] **Step 1: Create web/tests/test_checkout_e2e.py**

```python
import os
import pytest
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage
from web.utils.driver_factory import create_driver

_USER = os.getenv("SAUCE_USER", "standard_user")
_PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
_PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


@pytest.fixture
def driver():
    d = create_driver()
    yield d
    d.quit()


@pytest.mark.web
class TestCheckoutE2E:
    def test_login_navigates_to_inventory(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login(_USER, _PASSWORD)
        assert "inventory" in driver.current_url

    def test_add_products_appear_in_cart(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login(_USER, _PASSWORD)

        inventory = InventoryPage(driver)
        for product in _PRODUCTS:
            inventory.add_product_to_cart(product)
        inventory.go_to_cart()

        cart = CartPage(driver)
        items = cart.get_item_names()
        assert "Sauce Labs Backpack" in items
        assert "Sauce Labs Bike Light" in items

    def test_complete_checkout_shows_confirmation(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login(_USER, _PASSWORD)

        inventory = InventoryPage(driver)
        for product in _PRODUCTS:
            inventory.add_product_to_cart(product)
        inventory.go_to_cart()

        cart = CartPage(driver)
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_shipping_info("Test", "User", "12345")
        checkout.finish_order()

        assert checkout.get_confirmation_message() == "Thank you for your order!"
```

- [ ] **Step 2: Run web tests (Chrome must be installed)**

```bash
pytest -m web -v
```

Expected: all 3 tests PASS.

- [ ] **Step 3: Run full test suite to verify both suites pass**

```bash
pytest -v
```

Expected: all 27 tests PASS (24 API + 3 Web).

- [ ] **Step 4: Commit**

```bash
git add web/tests/test_checkout_e2e.py
git commit -m "test: implement SauceDemo E2E checkout scenario"
```

---

## Task 9: GitHub Actions CI/CD

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create .github/workflows/ci.yml**

```yaml
name: CI

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run API tests
        run: pytest -m api -v --alluredir=allure-results-api

      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results-api
          path: allure-results-api/

  web-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Chrome
        run: |
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Web tests
        env:
          HEADLESS: "true"
        run: pytest -m web -v --alluredir=allure-results-web

      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results-web
          path: allure-results-web/
```

- [ ] **Step 2: Commit**

```bash
git add .github/
git commit -m "ci: add GitHub Actions pipeline with parallel API and web jobs"
```

---

## Task 10: Docker

**Files:**
- Create: `Dockerfile`
- Create: `docker-compose.yml`

- [ ] **Step 1: Create Dockerfile**

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HEADLESS=true
ENV BASE_URL=https://petstore.swagger.io/v2
ENV SAUCE_URL=https://www.saucedemo.com
ENV SAUCE_USER=standard_user
ENV SAUCE_PASSWORD=secret_sauce
```

- [ ] **Step 2: Create docker-compose.yml**

```yaml
services:
  tests:
    build: .
    volumes:
      - ./allure-results:/app/allure-results
    env_file:
      - .env.example
    environment:
      HEADLESS: "true"
```

- [ ] **Step 3: Commit**

```bash
git add Dockerfile docker-compose.yml
git commit -m "feat: add Docker support with Chrome for containerized test execution"
```

---

## Task 11: README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create README.md**

```markdown
# Test Automation Project

API and Web test automation suite for Swagger Petstore and SauceDemo, with GitHub Actions CI/CD and Allure reports.

## Technologies

| Tool | Purpose |
|---|---|
| Python 3.12 | Primary language |
| pytest | Test runner |
| requests | HTTP client for API tests |
| Selenium 4 | Browser automation |
| webdriver-manager | Auto-manages ChromeDriver |
| allure-pytest | Visual test reports |
| python-dotenv | Environment variable loading |
| Docker | Containerized execution |
| GitHub Actions | CI/CD pipeline |

## Project Structure

```
test-automation-project/
├── api/               # API automation — Swagger Petstore
│   ├── models/        # Response schema definitions
│   ├── services/      # HTTP service classes (Service Layer)
│   ├── tests/         # Test files
│   └── utils/         # Data factories
├── web/               # Web automation — SauceDemo
│   ├── pages/         # Page Object classes (POM)
│   ├── tests/         # E2E test files
│   └── utils/         # WebDriver factory
├── .github/workflows/ # GitHub Actions pipeline
├── Dockerfile
├── docker-compose.yml
└── pytest.ini
```

## Installation

**Prerequisites:** Python 3.12, Chrome browser

```bash
git clone https://github.com/<your-username>/test-automation-project.git
cd test-automation-project
pip install -r requirements.txt
cp .env.example .env
```

## Running Tests

```bash
# All tests
pytest -v

# API tests only
pytest -m api -v

# Web tests only
pytest -m web -v

# With Allure report
pytest -v --alluredir=allure-results
allure serve allure-results
```

## Running with Docker

```bash
# Build image
docker-compose build

# Run API tests
docker-compose run --rm tests pytest -m api -v

# Run Web tests
docker-compose run --rm tests pytest -m web -v

# Run all tests
docker-compose run --rm tests pytest -v
```

## CI/CD Pipeline

GitHub Actions runs automatically on every push and pull request.

**Jobs run in parallel:**
- `api-tests` — installs dependencies, runs `pytest -m api`, uploads Allure artifacts
- `web-tests` — installs Chrome, runs `pytest -m web` in headless mode, uploads Allure artifacts

Allure results are available as downloadable artifacts in the Actions tab.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://petstore.swagger.io/v2` | Petstore API base URL |
| `SAUCE_URL` | `https://www.saucedemo.com` | SauceDemo URL |
| `SAUCE_USER` | `standard_user` | SauceDemo username |
| `SAUCE_PASSWORD` | `secret_sauce` | SauceDemo password |
| `HEADLESS` | `true` | Run Chrome in headless mode |

## Test Coverage

### API — Swagger Petstore
- **Pet:** create, get by ID, update, delete, find by status, 404 validation, schema validation
- **User:** create, get by username, update, delete, login, 404 validation, schema validation
- **Store:** get inventory, create order, get order, delete order, 404 validation

### Web — SauceDemo
- Login and redirect to inventory page
- Add products to cart and verify items
- Complete E2E checkout flow with order confirmation
```

- [ ] **Step 2: Commit README**

```bash
git add README.md
git commit -m "docs: add README with setup, execution, and CI/CD documentation"
```

---

## Task 12: Final Verification

- [ ] **Step 1: Run full test suite locally**

```bash
pytest -v --alluredir=allure-results
```

Expected: 27 tests — 24 API + 3 Web — all PASS.

- [ ] **Step 2: Generate and open Allure report (requires Allure CLI installed)**

```bash
allure serve allure-results
```

Expected: browser opens with visual report showing all tests.

- [ ] **Step 3: Push to GitHub and verify pipeline**

```bash
git remote add origin https://github.com/<your-username>/test-automation-project.git
git push -u origin master
```

Then go to the GitHub repository → Actions tab and verify both `api-tests` and `web-tests` jobs are green.

- [ ] **Step 4: Final commit if any adjustments were needed**

```bash
git add -A
git commit -m "fix: <describe any final adjustments>"
git push
```
```
