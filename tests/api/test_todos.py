# tests/api/test_todos.py

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import REQUEST_TIMEOUT, HTTP_OK
from tests.schemas.schemas import TODO_SCHEMA
from tests.utils.helpers import assert_schema

@pytest.mark.todos        # your new custom marker
class TestTodos:

    def test_get_all_todos(self, api_session, todos_url):
        response = api_session.get(todos_url, timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_OK

    @pytest.mark.parametrize("todo_id", [1, 50, 100])
    def test_todo_schema(self, api_session, todos_url, todo_id):
        response = api_session.get(f"{todos_url}/{todo_id}", timeout=REQUEST_TIMEOUT)
        assert_schema(response.json(), TODO_SCHEMA)