# Test Automation Project

API and Web test automation suite for [Swagger Petstore](https://petstore.swagger.io/v2) and [SauceDemo](https://www.saucedemo.com), with GitHub Actions CI/CD and Allure reports.

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
├── api/                    # API automation — Swagger Petstore
│   ├── models/             # Response schema definitions
│   ├── services/           # HTTP service classes (Service Layer)
│   ├── tests/              # Test files
│   └── utils/              # Data factories
├── web/                    # Web automation — SauceDemo
│   ├── pages/              # Page Object classes (POM)
│   ├── tests/              # E2E test files
│   └── utils/              # WebDriver factory
├── .github/workflows/      # GitHub Actions pipeline
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

Allure results are available as downloadable artifacts in the Actions tab after each run.

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

| Resource | Coverage |
|---|---|
| Pet | create, get by ID, update, delete, find by status, 404, schema validation |
| User | create, get by username, update, delete, login, 404, schema validation |
| Store | get inventory, create order, get order, delete order, 404 |

### Web — SauceDemo

| Scenario | Validation |
|---|---|
| Login | Redirects to inventory page |
| Add to cart | Both products appear in cart |
| Checkout | Order confirmation message displayed |
