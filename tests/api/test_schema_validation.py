# tests/api/test_schema_validation.py
# Dedicated schema validation tests across all endpoints

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import REQUEST_TIMEOUT
from tests.schemas.schemas import (
    POST_SCHEMA, POST_LIST_SCHEMA,
    USER_SCHEMA, COMMENT_SCHEMA, TODO_SCHEMA,
)
from tests.utils.helpers import assert_schema, validate_schema


@pytest.mark.schema
class TestSchemaValidation:
    """Dedicated schema validation across all resource types."""

    # ── Posts ──────────────────────────────────────────────────────────────────

    def test_posts_list_schema(self, api_session, endpoints):
        """GET /posts → full list matches POST_LIST_SCHEMA."""
        response = api_session.get(endpoints["posts"], timeout=REQUEST_TIMEOUT)
        assert_schema(response.json(), POST_LIST_SCHEMA, label="posts list")

    @pytest.mark.parametrize("post_id", [1, 25, 50, 75, 100])
    def test_single_post_schema(self, api_session, endpoints, post_id):
        """GET /posts/{id} → matches POST_SCHEMA."""
        response = api_session.get(f"{endpoints['posts']}/{post_id}", timeout=REQUEST_TIMEOUT)
        assert_schema(response.json(), POST_SCHEMA, label=f"post/{post_id}")

    # ── Users ──────────────────────────────────────────────────────────────────

    @pytest.mark.parametrize("user_id", [1, 3, 7, 10])
    def test_user_schema(self, api_session, endpoints, user_id):
        """GET /users/{id} → matches USER_SCHEMA."""
        response = api_session.get(f"{endpoints['users']}/{user_id}", timeout=REQUEST_TIMEOUT)
        assert_schema(response.json(), USER_SCHEMA, label=f"user/{user_id}")

    # ── Comments ───────────────────────────────────────────────────────────────

    @pytest.mark.parametrize("comment_id", [1, 100, 300, 500])
    def test_comment_schema(self, api_session, endpoints, comment_id):
        """GET /comments/{id} → matches COMMENT_SCHEMA."""
        response = api_session.get(f"{endpoints['comments']}/{comment_id}", timeout=REQUEST_TIMEOUT)
        assert_schema(response.json(), COMMENT_SCHEMA, label=f"comment/{comment_id}")

    # ── Todos ──────────────────────────────────────────────────────────────────

    @pytest.mark.parametrize("todo_id", [1, 50, 100, 150, 200])
    def test_todo_schema(self, api_session, endpoints, todo_id):
        """GET /todos/{id} → matches TODO_SCHEMA."""
        response = api_session.get(f"{endpoints['todos']}/{todo_id}", timeout=REQUEST_TIMEOUT)
        assert_schema(response.json(), TODO_SCHEMA, label=f"todo/{todo_id}")

    # ── Required field presence ────────────────────────────────────────────────

    @pytest.mark.parametrize("field", ["userId", "id", "title", "body"])
    def test_post_has_required_fields(self, api_session, endpoints, field):
        """GET /posts/1 → required field present."""
        response = api_session.get(f"{endpoints['posts']}/1", timeout=REQUEST_TIMEOUT)
        assert field in response.json(), f"Missing field: {field}"

    @pytest.mark.parametrize("field", ["id", "name", "username", "email", "address", "company"])
    def test_user_has_required_fields(self, api_session, endpoints, field):
        """GET /users/1 → required field present."""
        response = api_session.get(f"{endpoints['users']}/1", timeout=REQUEST_TIMEOUT)
        assert field in response.json(), f"Missing field: {field}"

    # ── Type checks ────────────────────────────────────────────────────────────

    def test_post_types(self, api_session, endpoints):
        """GET /posts/1 → field types are correct."""
        data = api_session.get(f"{endpoints['posts']}/1", timeout=REQUEST_TIMEOUT).json()
        assert isinstance(data["id"],     int)
        assert isinstance(data["userId"], int)
        assert isinstance(data["title"],  str)
        assert isinstance(data["body"],   str)

    def test_todo_completed_is_boolean(self, api_session, endpoints):
        """GET /todos/1 → 'completed' field is a boolean."""
        data = api_session.get(f"{endpoints['todos']}/1", timeout=REQUEST_TIMEOUT).json()
        assert isinstance(data["completed"], bool)

    # ── Negative schema tests ──────────────────────────────────────────────────

    @pytest.mark.negative
    def test_invalid_data_fails_schema(self):
        """Manually crafted bad data should fail POST_SCHEMA validation."""
        bad_data = {"userId": "not-an-int", "title": 123, "body": None}
        valid, error = validate_schema(bad_data, POST_SCHEMA)
        assert not valid, "Expected schema validation to fail on bad data"
