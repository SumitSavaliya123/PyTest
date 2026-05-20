# conftest.py - Shared fixtures for the entire test suite

import pytest
import requests
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import BASE_URL, ENDPOINTS, DEFAULT_HEADERS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


# ── Session-scoped: one HTTP session for all tests ─────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    """Base URL for JSONPlaceholder API."""
    return BASE_URL


@pytest.fixture(scope="session")
def endpoints():
    """All API endpoint URLs."""
    return ENDPOINTS


@pytest.fixture(scope="session")
def api_session():
    """
    Reusable requests.Session with default headers.
    Session-scoped → created once, shared across all tests.
    """
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    logger.info(f"API Session created → {BASE_URL}")
    yield session
    session.close()
    logger.info("API Session closed")


# ── Function-scoped helpers ────────────────────────────────────────────────────

@pytest.fixture
def posts_url(endpoints):
    return endpoints["posts"]


@pytest.fixture
def users_url(endpoints):
    return endpoints["users"]


@pytest.fixture
def comments_url(endpoints):
    return endpoints["comments"]


@pytest.fixture
def todos_url(endpoints):
    return endpoints["todos"]


# ── Pre-seeded data fixtures ───────────────────────────────────────────────────

@pytest.fixture(scope="session")
def existing_post(api_session, endpoints):
    """
    Fetch a real post from the API once per session.
    Used in tests that need a valid existing resource.
    """
    response = api_session.get(f"{endpoints['posts']}/1", timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, "Failed to fetch seed post"
    return response.json()


@pytest.fixture(scope="session")
def existing_user(api_session, endpoints):
    """Fetch a real user from the API once per session."""
    response = api_session.get(f"{endpoints['users']}/1", timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, "Failed to fetch seed user"
    return response.json()


@pytest.fixture
def sample_post_payload():
    """Fresh post payload for each test."""
    return {
        "title":  "Fixture Generated Post",
        "body":   "This post was created by a pytest fixture.",
        "userId": 1,
    }


@pytest.fixture
def sample_patch_payload():
    """Minimal payload for PATCH requests."""
    return {"title": "Patched Title from Fixture"}


# ── Faker-based dynamic data fixture ──────────────────────────────────────────

@pytest.fixture
def fake_post_payload():
    """
    Dynamically generated post data using Faker.
    Each test call gets unique data.
    """
    try:
        from faker import Faker
        fake = Faker()
        return {
            "title":  fake.sentence(nb_words=6).rstrip("."),
            "body":   fake.paragraph(nb_sentences=3),
            "userId": fake.random_int(min=1, max=10),
        }
    except ImportError:
        return {
            "title":  "Dynamic Test Post",
            "body":   "Generated without Faker library.",
            "userId": 1,
        }


# ── Reporting hook ─────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def log_test_name(request):
    """Auto-log test name at start/end — visible in CI logs."""
    logger.info(f"▶ START  {request.node.nodeid}")
    yield
    logger.info(f"■ FINISH {request.node.nodeid}")
