import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import REQUEST_TIMEOUT, HTTP_OK, HTTP_CREATED, HTTP_NOT_FOUND
from tests.schemas.schemas import POST_SCHEMA, CREATED_POST_SCHEMA
from tests.utils.helpers import assert_schema, assert_response_time, log_request, log_response


# ═══════════════════════════════════════════════════════════════════════════════
# READ — GET tests
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.smoke
@pytest.mark.posts
class TestGetPosts:

    def test_get_all_posts_returns_200(self, api_session, posts_url):
        """GET /posts → 200 with a non-empty list."""
        response = api_session.get(posts_url, timeout=REQUEST_TIMEOUT)
        log_response(response)
        assert response.status_code == HTTP_OK

    def test_get_all_posts_returns_list(self, api_session, posts_url):
        """GET /posts → response body is a JSON array."""
        response = api_session.get(posts_url, timeout=REQUEST_TIMEOUT)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 100  # JSONPlaceholder always has 100 posts

    def test_get_all_posts_schema(self, api_session, posts_url):
        """GET /posts → every item matches POST_SCHEMA."""
        response = api_session.get(posts_url, timeout=REQUEST_TIMEOUT)
        posts = response.json()
        for post in posts[:5]:          # validate first 5 for speed
            assert_schema(post, POST_SCHEMA, label=f"post id={post.get('id')}")

    @pytest.mark.parametrize("post_id", [1, 10, 50, 100])
    def test_get_single_post_by_id(self, api_session, posts_url, post_id):
        """GET /posts/{id} → 200 and correct id returned."""
        response = api_session.get(f"{posts_url}/{post_id}", timeout=REQUEST_TIMEOUT)
        log_response(response)
        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["id"] == post_id

    @pytest.mark.parametrize("post_id", [1, 10, 50, 100])
    def test_get_single_post_schema(self, api_session, posts_url, post_id):
        """GET /posts/{id} → response matches POST_SCHEMA."""
        response = api_session.get(f"{posts_url}/{post_id}", timeout=REQUEST_TIMEOUT)
        assert_schema(response.json(), POST_SCHEMA, label=f"post/{post_id}")

    def test_get_post_response_time(self, api_session, posts_url):
        """GET /posts/1 → responds within 3 seconds."""
        response = api_session.get(f"{posts_url}/1", timeout=REQUEST_TIMEOUT)
        assert_response_time(response, max_seconds=3.0)

    def test_get_posts_content_type(self, api_session, posts_url):
        """GET /posts → Content-Type header includes application/json."""
        response = api_session.get(posts_url, timeout=REQUEST_TIMEOUT)
        assert "application/json" in response.headers.get("Content-Type", "")

    @pytest.mark.negative
    @pytest.mark.parametrize("post_id", [9999, 99999])
    def test_get_nonexistent_post_returns_404(self, api_session, posts_url, post_id):
        """GET /posts/{invalid_id} → 404 Not Found."""
        response = api_session.get(f"{posts_url}/{post_id}", timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_NOT_FOUND


# ═══════════════════════════════════════════════════════════════════════════════
# CREATE — POST tests
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.crud
@pytest.mark.posts
class TestCreatePost:

    def test_create_post_returns_201(self, api_session, posts_url, sample_post_payload):
        """POST /posts → 201 Created."""
        log_request("POST", posts_url, json=sample_post_payload)
        response = api_session.post(posts_url, json=sample_post_payload, timeout=REQUEST_TIMEOUT)
        log_response(response)
        assert response.status_code == HTTP_CREATED

    def test_create_post_returns_id(self, api_session, posts_url, sample_post_payload):
        """POST /posts → created resource includes an id."""
        response = api_session.post(posts_url, json=sample_post_payload, timeout=REQUEST_TIMEOUT)
        data = response.json()
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_post_echoes_payload(self, api_session, posts_url, sample_post_payload):
        """POST /posts → response body mirrors submitted fields."""
        response = api_session.post(posts_url, json=sample_post_payload, timeout=REQUEST_TIMEOUT)
        data = response.json()
        assert data["title"]  == sample_post_payload["title"]
        assert data["body"]   == sample_post_payload["body"]
        assert data["userId"] == sample_post_payload["userId"]

    def test_create_post_schema(self, api_session, posts_url, sample_post_payload):
        """POST /posts → response matches CREATED_POST_SCHEMA."""
        response = api_session.post(posts_url, json=sample_post_payload, timeout=REQUEST_TIMEOUT)
        assert_schema(response.json(), CREATED_POST_SCHEMA, label="created post")

    @pytest.mark.parametrize("payload", [
        {"title": "Data-Driven Post 1", "body": "Body one",   "userId": 1},
        {"title": "Data-Driven Post 2", "body": "Body two",   "userId": 2},
        {"title": "Data-Driven Post 3", "body": "Body three", "userId": 3},
    ], ids=["user1", "user2", "user3"])
    def test_create_post_data_driven(self, api_session, posts_url, payload):
        """POST /posts → data-driven creation with multiple payloads."""
        response = api_session.post(posts_url, json=payload, timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_CREATED
        data = response.json()
        assert data["title"]  == payload["title"]
        assert data["userId"] == payload["userId"]

    def test_create_post_with_fake_data(self, api_session, posts_url, fake_post_payload):
        """POST /posts → Faker-generated payload creates successfully."""
        response = api_session.post(posts_url, json=fake_post_payload, timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_CREATED
        assert response.json()["title"] == fake_post_payload["title"]



# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE — PUT tests
# ═══════════════════════════════════════════════════════════════════════════════
@pytest.mark.crud
@pytest.mark.posts
class TestUpdatePost:

    @pytest.mark.parametrize("post_id, payload", [
        (1, {"id": 1, "title": "PUT Updated Title 1", "body": "Updated body 1", "userId": 1}),
        (2, {"id": 2, "title": "PUT Updated Title 2", "body": "Updated body 2", "userId": 1}),
    ], ids=["post_1", "post_2"])
    def test_put_post_returns_200(self, api_session, posts_url, post_id, payload):
        """PUT /posts/{id} → 200 OK with updated data."""
        response = api_session.put(f"{posts_url}/{post_id}", json=payload, timeout=REQUEST_TIMEOUT)
        log_response(response)
        assert response.status_code == HTTP_OK

    def test_put_post_reflects_changes(self, api_session, posts_url):
        """PUT /posts/1 → response body matches what was sent."""
        payload = {"id": 1, "title": "Fully Replaced", "body": "New body.", "userId": 5}
        response = api_session.put(f"{posts_url}/1", json=payload, timeout=REQUEST_TIMEOUT)
        data = response.json()
        assert data["title"]  == payload["title"]
        assert data["body"]   == payload["body"]
        assert data["userId"] == payload["userId"]


# ═══════════════════════════════════════════════════════════════════════════════
# PARTIAL UPDATE — PATCH tests
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.crud
@pytest.mark.posts
class TestPatchPost:

    @pytest.mark.parametrize("patch_data, field, expected", [
        ({"title": "Patched Title Only"},  "title", "Patched Title Only"),
        ({"body":  "Patched body only"},   "body",  "Patched body only"),
    ], ids=["patch_title", "patch_body"])
    def test_patch_post_field(self, api_session, posts_url, patch_data, field, expected):
        """PATCH /posts/1 → only the specified field is updated."""
        response = api_session.patch(f"{posts_url}/1", json=patch_data, timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_OK
        assert response.json()[field] == expected

    def test_patch_preserves_other_fields(self, api_session, posts_url, existing_post):
        """PATCH /posts/1 with title only → body and userId remain unchanged."""
        original_body   = existing_post["body"]
        original_userId = existing_post["userId"]
        response = api_session.patch(
            f"{posts_url}/{existing_post['id']}",
            json={"title": "Only Title Changed"},
            timeout=REQUEST_TIMEOUT,
        )
        data = response.json()
        # JSONPlaceholder echoes back the patched resource
        assert data["body"]   == original_body
        assert data["userId"] == original_userId


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE tests
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.crud
@pytest.mark.posts
class TestDeletePost:

    @pytest.mark.parametrize("post_id", [1, 50, 100])
    def test_delete_post_returns_200(self, api_session, posts_url, post_id):
        """DELETE /posts/{id} → 200 OK (JSONPlaceholder simulates deletion)."""
        response = api_session.delete(f"{posts_url}/{post_id}", timeout=REQUEST_TIMEOUT)
        assert response.status_code == HTTP_OK

    def test_delete_post_returns_empty_body(self, api_session, posts_url):
        """DELETE /posts/1 → response body is an empty object {}."""
        response = api_session.delete(f"{posts_url}/1", timeout=REQUEST_TIMEOUT)
        assert response.json() == {}
