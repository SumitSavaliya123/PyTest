# data/test_data.py - Static + generated test data for parametrize

# ── Posts ──────────────────────────────────────────────────────────────────────

VALID_POST_PAYLOADS = [
    {
        "title": "Introduction to Pytest",
        "body":  "Pytest is a powerful testing framework for Python.",
        "userId": 1,
    },
    {
        "title": "API Automation with Requests",
        "body":  "The requests library makes HTTP calls simple and elegant.",
        "userId": 2,
    },
    {
        "title": "Data-Driven Testing",
        "body":  "Parametrize your tests to run the same logic with many inputs.",
        "userId": 3,
    },
]

INVALID_POST_PAYLOADS = [
    pytest_id := ({"title": "", "body": "body", "userId": 1}, "empty_title"),
    ({"title": "title", "body": "", "userId": 1},              "empty_body"),
    ({"title": "title", "body": "body", "userId": -1},         "negative_userId"),
]

# ── Update payloads ────────────────────────────────────────────────────────────

PATCH_PAYLOADS = [
    ({"title": "Updated Title"},               "patch_title"),
    ({"body": "Updated body content"},          "patch_body"),
    ({"title": "New Title", "body": "New Body"}, "patch_title_and_body"),
]

PUT_PAYLOADS = [
    {
        "id":     1,
        "title":  "Full PUT Replace",
        "body":   "This replaces the entire post resource.",
        "userId": 1,
    },
    {
        "id":     2,
        "title":  "Another PUT Test",
        "body":   "PUT must send the complete representation.",
        "userId": 2,
    },
]

# ── Non-existent IDs ──────────────────────────────────────────────────────────

NONEXISTENT_IDS = [9999, 99999, 100001]

# ── Valid post IDs to fetch ───────────────────────────────────────────────────

VALID_POST_IDS = [1, 5, 10, 50, 100]

# ── User IDs ──────────────────────────────────────────────────────────────────

VALID_USER_IDS = [1, 2, 3, 4, 5]
