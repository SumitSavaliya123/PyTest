# tests/utils/helpers.py - Reusable helper functions

import json
import logging
import jsonschema
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


def validate_schema(data: dict | list, schema: dict) -> tuple[bool, str]:
    """
    Validate JSON data against a schema.
    Returns (True, "") on success or (False, error_message) on failure.
    """
    try:
        validate(instance=data, schema=schema)
        return True, ""
    except ValidationError as e:
        return False, e.message


def assert_schema(data, schema, label="response"):
    """Assert that data matches the schema, with a helpful error message."""
    valid, error = validate_schema(data, schema)
    assert valid, f"Schema validation failed for {label}: {error}"


def log_request(method: str, url: str, **kwargs):
    logger.info(f"REQUEST  {method.upper()} {url}")
    if kwargs.get("json"):
        logger.info(f"BODY     {json.dumps(kwargs['json'], indent=2)}")


def log_response(response):
    logger.info(f"RESPONSE {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
    try:
        logger.debug(f"BODY     {json.dumps(response.json(), indent=2)}")
    except Exception:
        logger.debug(f"BODY     {response.text[:500]}")


def assert_response_time(response, max_seconds: float = 3.0):
    """Assert response time is within acceptable limit."""
    elapsed = response.elapsed.total_seconds()
    assert elapsed <= max_seconds, (
        f"Response too slow: {elapsed:.3f}s (max {max_seconds}s)"
    )
