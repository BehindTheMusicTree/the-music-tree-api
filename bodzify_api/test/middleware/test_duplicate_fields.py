import json
from django.test import RequestFactory

from bodzify_api.middleware.duplicate_fields.middleware import DuplicateFieldsMiddleware
from bodzify_api.middleware.duplicate_fields.JsonDuplicateKeyDetectingDecoder import JsonDuplicateKeyDetectingDecoder


def test_duplicates_not_in_same_object():
    """Test that duplicate fields are only detected when they appear in the same object."""
    # Create a JSON with duplicate fields in different objects
    json_data = {
        "user1": {
            "name": "John",
            "age": 30
        },
        "user2": {
            "name": "Jane",
            "age": 25
        }
    }

    # Convert to JSON string
    json_str = json.dumps(json_data)

    # Create decoder and decode
    decoder = JsonDuplicateKeyDetectingDecoder()
    decoder.decode(json_str)

    # Verify no duplicates were found since they're in different objects
    assert len(decoder.tracker.duplicates) == 0


def test_duplicates_in_same_object():
    """Test that duplicate fields are detected when they appear in the same object."""
    # Create a JSON with duplicate fields in the same object
    json_data = {
        "name": "John",
        "name": "Jane",  # Duplicate field
        "age": 30
    }

    # Convert to JSON string
    json_str = json.dumps(json_data)

    # Create decoder and decode
    decoder = JsonDuplicateKeyDetectingDecoder()
    decoder.decode(json_str)

    # Verify duplicate was found
    assert len(decoder.tracker.duplicates) == 1
    assert decoder.tracker.duplicates[0] == "name"


def test_duplicates_in_nested_objects():
    """Test that duplicate fields are detected in nested objects but not across objects."""
    # Create a JSON with duplicate fields in nested objects
    json_data = {
        "outer": {
            "inner1": {
                "name": "John",
                "name": "Jane"  # Duplicate in inner1
            },
            "inner2": {
                "name": "Bob"  # Not a duplicate
            }
        }
    }

    # Convert to JSON string
    json_str = json.dumps(json_data)

    # Create decoder and decode
    decoder = JsonDuplicateKeyDetectingDecoder()
    decoder.decode(json_str)

    # Verify only the duplicate in inner1 was found
    assert len(decoder.tracker.duplicates) == 1
    assert decoder.tracker.duplicates[0] == "name"


def test_middleware_duplicates_not_in_same_object():
    """Test that the middleware correctly handles duplicates not in the same object."""
    # Create a JSON with duplicate fields in different objects
    json_data = {
        "user1": {
            "name": "John",
            "age": 30
        },
        "user2": {
            "name": "Jane",
            "age": 25
        }
    }

    # Create a request with the JSON data
    factory = RequestFactory()
    request = factory.post(
        '/api/test/',
        data=json.dumps(json_data),
        content_type='application/json'
    )

    # Create middleware instance
    middleware = DuplicateFieldsMiddleware(get_response=lambda r: None)

    # Process the request
    response = middleware(request)

    # Verify no error response was returned since duplicates are in different objects
    assert response is None
