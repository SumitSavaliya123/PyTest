# tests/api/test_users.py
# Tests for /users endpoint — schema validation, nested object checks, filtering

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import REQUEST_TIMEOUT, HTTP_OK, HTTP_NOT_FOUND
from tests.schemas.schemas import USER_SCHEMA
from tests.utils.helpers import assert_schema, assert_response_time, log_response


@pytest.mark.users
@pytest.mark.smoke
class TestGetUsers:

    def test_get_all_users_returns_200(self, api_session, users_url):
        """GET /users → 200 OK."""
        response = api_session.get(users_url, timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_OK

    def test_get_all_users_count(self, api_session, users_url):
        """GET /users → 10 users returned."""
        response = api_session.get(users_url, timeout=REQUEST_TIMEOUT)
        assert len(response.json()) == 10

    @pytest.mark.schema
    @pytest.mark.parametrize("user_id", [1, 2, 3, 5, 10])
    def test_user_schema_validation(self, api_session, users_url, user_id):
        """GET /users/{id} → response matches USER_SCHEMA."""
        response = api_session.get(f"{users_url}/{user_id}", timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_OK
        assert_schema(response.json(), USER_SCHEMA, label=f"user/{user_id}")

    def test_user_has_valid_email(self, api_session, users_url):
        """GET /users → every user email contains @ symbol."""
        response = api_session.get(users_url, timeout=REQUEST_TIMEOUT)
        for user in response.json():
            assert "@" in user["email"], f"Invalid email for user id={user['id']}"

    def test_user_has_nested_address(self, api_session, users_url):
        """GET /users/1 → address object has city, street, zipcode."""
        response = api_session.get(f"{users_url}/1", timeout=REQUEST_TIMEOUT)
        address = response.json()["address"]
        for field in ["city", "street", "zipcode"]:
            assert field in address, f"Missing address field: {field}"

    def test_user_has_geo_coordinates(self, api_session, users_url):
        """GET /users/1 → address.geo has lat and lng."""
        response = api_session.get(f"{users_url}/1", timeout=REQUEST_TIMEOUT)
        geo = response.json()["address"]["geo"]
        assert "lat" in geo
        assert "lng" in geo

    def test_user_has_company(self, api_session, users_url):
        """GET /users/1 → company object has name, catchPhrase, bs."""
        response = api_session.get(f"{users_url}/1", timeout=REQUEST_TIMEOUT)
        company = response.json()["company"]
        for field in ["name", "catchPhrase", "bs"]:
            assert field in company, f"Missing company field: {field}"

    @pytest.mark.negative
    def test_get_nonexistent_user(self, api_session, users_url):
        """GET /users/9999 → 404 Not Found."""
        response = api_session.get(f"{users_url}/9999", timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_NOT_FOUND

    def test_get_user_response_time(self, api_session, users_url):
        """GET /users/1 → response within 3 seconds."""
        response = api_session.get(f"{users_url}/1", timeout=REQUEST_TIMEOUT)
        assert_response_time(response)

    def test_filter_posts_by_user(self, api_session, endpoints):
        """GET /posts?userId=1 → all posts belong to userId 1."""
        response = api_session.get(
            endpoints["posts"],
            params={"userId": 1},
            timeout=REQUEST_TIMEOUT,
        )
        log_response(response)
        assert response.status_code == HTTP_OK
        posts = response.json()
        assert len(posts) > 0
        assert all(p["userId"] == 1 for p in posts)

    @pytest.mark.parametrize("user_id, expected_post_count", [
        (1, 10),
        (2, 10),
        (3, 10),
    ], ids=["user_1", "user_2", "user_3"])
    def test_user_post_count(self, api_session, endpoints, user_id, expected_post_count):
        """GET /posts?userId={id} → each user has exactly 10 posts."""
        response = api_session.get(
            endpoints["posts"],
            params={"userId": user_id},
            timeout=REQUEST_TIMEOUT,
        )
        assert len(response.json()) == expected_post_count
