# Test Automation Project — Design Spec
**Date:** 2026-05-06  
**Status:** Approved

---

## Overview

Single repository containing API and Web test automation suites, integrated with GitHub Actions CI/CD pipeline. Built with Python, pytest, Selenium, and Allure reports.

**Targets:**
- API: Swagger Petstore (`https://petstore.swagger.io/v2`)
- Web: SauceDemo (`https://www.saucedemo.com`)

---

## Repository Structure

```
test-automation-project/
├── api/
│   ├── tests/
│   │   ├── test_pet.py
│   │   ├── test_user.py
│   │   └── test_store.py
│   ├── services/
│   │   ├── pet_service.py
│   │   ├── user_service.py
│   │   └── store_service.py
│   ├── models/
│   │   ├── pet_model.py
│   │   └── user_model.py
│   └── utils/
│       └── factories.py
├── web/
│   ├── tests/
│   │   └── test_checkout_e2e.py
│   ├── pages/
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   └── utils/
│       └── driver_factory.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── conftest.py
└── README.md
```

---

## Technology Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.12 | Primary language |
| pytest | latest | Test runner for API and Web |
| requests | latest | HTTP client for API tests |
| selenium | 4.x | Browser automation |
| webdriver-manager | latest | Auto-manages ChromeDriver |
| allure-pytest | latest | Test reporting |
| python-dotenv | latest | Environment variable loading |

---

## API Automation

### Architecture: Service Layer Pattern

Each service class wraps HTTP calls for one resource domain:

**`PetService`**
- `create(payload) -> Response`
- `get_by_id(pet_id) -> Response`
- `update(payload) -> Response`
- `delete(pet_id) -> Response`
- `find_by_status(status) -> Response`

**`UserService`**
- `create(payload) -> Response`
- `get_by_username(username) -> Response`
- `update(username, payload) -> Response`
- `delete(username) -> Response`
- `login(username, password) -> Response`

**`StoreService`**
- `get_inventory() -> Response`
- `create_order(payload) -> Response`
- `get_order(order_id) -> Response`
- `delete_order(order_id) -> Response`

### Factory Pattern

`factories.py` generates isolated test data per test run using `uuid` to avoid ID collisions:

```python
make_pet(name, status) -> dict
make_user(username) -> dict
make_order(pet_id) -> dict
```

### Test Coverage

Each test file covers CRUD + validations:
- Status code assertions (200, 201, 404, etc.)
- Response payload schema validation
- Each test is independent: creates and cleans its own data

### Endpoints Covered

| Resource | Endpoints |
|---|---|
| Pet | POST /pet, GET /pet/{id}, PUT /pet, DELETE /pet/{id}, GET /pet/findByStatus |
| User | POST /user, GET /user/{username}, PUT /user/{username}, DELETE /user/{username}, GET /user/login |
| Store | GET /store/inventory, POST /store/order, GET /store/order/{id}, DELETE /store/order/{id} |

---

## Web Automation

### Architecture: Page Object Model (POM)

One class per page — each class exposes action methods, no raw Selenium calls in tests.

**`LoginPage`**
- `login(username, password) -> None`

**`InventoryPage`**
- `add_product_to_cart(product_name) -> None`
- `go_to_cart() -> None`

**`CartPage`**
- `get_item_names() -> list[str]`
- `proceed_to_checkout() -> None`

**`CheckoutPage`**
- `fill_shipping_info(first, last, zip_code) -> None`
- `finish_order() -> None`
- `get_confirmation_message() -> str`

### Driver Factory

`driver_factory.py` reads the `HEADLESS` environment variable:
- `HEADLESS=true` (default in CI and Docker): Chrome runs headless
- `HEADLESS=false` (local dev): Chrome runs with window

### E2E Scenario

1. Navigate to SauceDemo
2. Login with `standard_user` / `secret_sauce`
3. Add two products to cart (`Sauce Labs Backpack`, `Sauce Labs Bike Light`)
4. Navigate to cart — assert both items present
5. Proceed to checkout — fill first name, last name, zip code
6. Finish order — assert confirmation message `"Thank you for your order!"`

---

## CI/CD — GitHub Actions

**Trigger:** `push` and `pull_request` on any branch.

**Jobs run in parallel:**

```yaml
jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps: install deps → run pytest -m api → upload Allure results

  web-tests:
    runs-on: ubuntu-latest
    steps: install Chrome → install deps → run pytest -m web → upload Allure results
```

Allure results uploaded as GitHub Actions artifacts per job.

---

## Docker

`Dockerfile` based on `python:3.12-slim` with Chrome and ChromeDriver installed.

`docker-compose.yml` defines a `tests` service with environment variables injected.

Usage:
```bash
docker-compose run --rm tests pytest -m api
docker-compose run --rm tests pytest -m web
docker-compose run --rm tests pytest
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://petstore.swagger.io/v2` | Petstore API base URL |
| `SAUCE_URL` | `https://www.saucedemo.com` | SauceDemo URL |
| `SAUCE_USER` | `standard_user` | SauceDemo username |
| `SAUCE_PASSWORD` | `secret_sauce` | SauceDemo password |
| `HEADLESS` | `true` | Run Chrome headless |

Loaded via `.env` file locally, injected via GitHub Actions env in CI.

---

## pytest Configuration

`pytest.ini` defines two markers:
- `@pytest.mark.api` — API test suite
- `@pytest.mark.web` — Web test suite

Run commands:
```bash
pytest -m api          # API only
pytest -m web          # Web only
pytest                 # All tests
pytest --alluredir=allure-results  # With Allure output
```

---

## Commit Convention

Format: `type: short description`

| Type | When to use |
|---|---|
| `feat` | New feature or test scenario |
| `test` | New or updated test cases |
| `fix` | Bug fix in test or helper code |
| `ci` | CI/CD workflow changes |
| `docs` | README or documentation |
| `refactor` | Code restructuring without behavior change |

Examples:
- `feat: add pet CRUD service layer`
- `test: implement checkout E2E scenario`
- `ci: add GitHub Actions workflow for API and web tests`
- `docs: add README with setup and execution instructions`

---

## Differentials Included

- Allure reports (HTML visual reports as GitHub Artifacts)
- Docker support (Dockerfile + docker-compose.yml)
- Parallel test execution (CI jobs run in parallel)
- Environment variables via python-dotenv
- Parameterized tests where applicable (e.g., pet status values)
