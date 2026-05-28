import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import REQUEST_TIMEOUT, HTTP_OK, HTTP_CREATED
from tests.schemas.schemas import COMMENT_SCHEMA
from tests.utils.helpers import assert_schema, log_response


@pytest.mark.comments
class TestComments:

    def test_get_all_comments_200(self, api_session, comments_url):
        response = api_session.get(comments_url, timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_OK

    def test_get_all_comments_count(self, api_session, comments_url):
        response = api_session.get(comments_url, timeout=REQUEST_TIMEOUT)
        assert len(response.json()) == 500

    @pytest.mark.schema
    @pytest.mark.parametrize("comment_id", [1, 50, 100, 250, 500])
    def test_comment_schema(self, api_session, comments_url, comment_id):
        """GET /comments/{id} → matches COMMENT_SCHEMA."""
        response = api_session.get(f"{comments_url}/{comment_id}", timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_OK
        assert_schema(response.json(), COMMENT_SCHEMA, label=f"comment/{comment_id}")

    def test_comment_email_format(self, api_session, comments_url):
        """GET /comments → first 10 comments all have @ in email."""
        response = api_session.get(comments_url, timeout=REQUEST_TIMEOUT)
        for comment in response.json()[:10]:
            assert "@" in comment["email"]

    @pytest.mark.parametrize("post_id", [1, 2, 5, 10])
    def test_filter_comments_by_post(self, api_session, comments_url, post_id):
        """GET /comments?postId={id} → returns only comments for that post."""
        response = api_session.get(
            comments_url,
            params={"postId": post_id},
            timeout=REQUEST_TIMEOUT,
        )
        log_response(response)
        comments = response.json()
        assert len(comments) == 5  # JSONPlaceholder: always 5 per post
        assert all(c["postId"] == post_id for c in comments)

    def test_create_comment_201(self, api_session, comments_url):
        """POST /comments → 201 Created."""
        payload = {
            "postId": 1,
            "name":   "Automated Test Comment",
            "email":  "tester@example.com",
            "body":   "This comment was created by an automated test.",
        }
        response = api_session.post(comments_url, json=payload, timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_CREATED
        data = response.json()
        assert data["name"]  == payload["name"]
        assert data["email"] == payload["email"]
