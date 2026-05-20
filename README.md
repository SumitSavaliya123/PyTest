# 🧪 Pytest CRUD API Automation Demo

A production-grade API test automation project using **JSONPlaceholder** as the target API.

## 📁 Project Structure

```
pytest_crud_demo/
├── config.py                        # Base URL, endpoints, constants
├── pytest.ini                       # Pytest configuration & markers
├── requirements.txt                 # All dependencies
├── Makefile                         # Shortcut commands
├── .github/
│   └── workflows/
│       └── ci.yml                   # GitHub Actions CI/CD pipeline
├── data/
│   └── test_data.py                 # Static data for parametrize
├── tests/
│   ├── conftest.py                  # Shared fixtures (session, URLs, payloads)
│   ├── schemas/
│   │   └── schemas.py               # JSON Schema definitions
│   ├── utils/
│   │   └── helpers.py               # Schema validation, logging, assertions
│   └── api/
│       ├── test_posts_crud.py       # Full CRUD tests for /posts
│       ├── test_users.py            # GET + schema tests for /users
│       ├── test_comments.py         # CRUD + filtering for /comments
│       └── test_schema_validation.py # Cross-endpoint schema tests
└── reports/                         # Auto-generated (HTML, JSON, coverage)
```

## 🚀 Quick Start

```bash
# 1. Clone and enter the project
git clone <your-repo> && cd pytest_crud_demo

# 2. Install dependencies
pip install -r requirements.txt
# or
make install

# 3. Run all tests
pytest
# or
make test
```

## 🏷️ Test Markers

Run targeted subsets of tests using markers:

```bash
pytest -m smoke      # Quick sanity checks
pytest -m crud       # Full CRUD operations
pytest -m schema     # Schema validation only
pytest -m negative   # Error/edge case tests
pytest -m posts      # All /posts tests
pytest -m users      # All /users tests
pytest -m comments   # All /comments tests
```

## 📊 Reports

After running tests, find reports in `reports/`:

| File | Description |
|---|---|
| `report.html` | Visual HTML test report |
| `report.json` | Machine-readable JSON results |
| `coverage/` | HTML coverage report |

Open the HTML report:
```bash
open reports/report.html   # macOS
xdg-open reports/report.html  # Linux
```

## 🔑 Key Features

### ✅ Fixtures (`conftest.py`)
- `api_session` — session-scoped `requests.Session` with shared headers
- `existing_post` / `existing_user` — pre-fetched seed data (session-scoped)
- `fake_post_payload` — Faker-generated dynamic test data
- `log_test_name` — autouse fixture that logs every test name

### ✅ Data-Driven Tests
```python
@pytest.mark.parametrize("post_id", [1, 10, 50, 100])
def test_get_single_post_by_id(self, api_session, posts_url, post_id):
    ...
```

### ✅ Schema Validation
```python
from tests.schemas.schemas import POST_SCHEMA
from tests.utils.helpers import assert_schema

assert_schema(response.json(), POST_SCHEMA, label="post/1")
```

### ✅ CI/CD (GitHub Actions)
- Matrix testing across Python 3.10, 3.11, 3.12
- Separate schema validation job
- Artifact upload of HTML reports
- Codecov integration

## 🛠️ Running in Parallel

```bash
pip install pytest-xdist
pytest -n auto   # Uses all CPU cores
# or
make parallel
```

## 🧹 Clean Up

```bash
make clean
```

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `pytest` | Test framework |
| `requests` | HTTP client |
| `jsonschema` | JSON Schema validation |
| `pytest-html` | HTML report generation |
| `pytest-cov` | Coverage reporting |
| `pytest-xdist` | Parallel test execution |
| `pytest-json-report` | JSON report generation |
| `Faker` | Dynamic test data generation |
