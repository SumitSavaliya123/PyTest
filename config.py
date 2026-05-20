# config.py - Central configuration for the test suite

BASE_URL = "https://jsonplaceholder.typicode.com"

ENDPOINTS = {
    "posts":    f"{BASE_URL}/posts",
    "users":    f"{BASE_URL}/users",
    "comments": f"{BASE_URL}/comments",
    "todos":    f"{BASE_URL}/todos",
    "albums":   f"{BASE_URL}/albums",
}

# HTTP status codes
HTTP_OK         = 200
HTTP_CREATED    = 201
HTTP_NO_CONTENT = 204
HTTP_NOT_FOUND  = 404

# Timeouts
REQUEST_TIMEOUT = 10  # seconds

# Headers
DEFAULT_HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept":       "application/json",
}
