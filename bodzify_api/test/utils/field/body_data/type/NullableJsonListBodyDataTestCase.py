"""
This module provides a base test case for fields that accept multiple values in JSON requests.

For JSON, standard array notation is used without the [] suffix:

Example for multiple values:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: application/json' \\
  --data '{
      "field": ["value1", "value2"]
  }'
```

To send a null value using JSON array notation, you can:
a) Omit the field completely
b) Send an empty array:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: application/json' \\
  --data '{
      "field": []
  }'
```
c) Send an explicit null:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: application/json' \\
  --data '{
      "field": null
  }'
```

Advantages of standard JSON array notation:
- Follows JSON specification
- Works with standard JSON parsers
- More natural for API clients working with JSON
- Consistent with other API frameworks
"""

from bodzify_api.test.utils.AppTestCase import AppTestCase


class NullableJsonListBodyDataTestCase(AppTestCase):
    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = [
            'test_json_array_largest_then_ok',
            'test_json_array_empty_then_ok',
            'test_json_array_one_too_large_then_400_bad_request',
            'test_json_array_multiple_with_one_too_large_then_400_bad_request',
            'test_json_array_multiple_with_one_empty_then_400_bad_request',
            'test_json_array_duplicate_values_then_400_bad_request',
        ]
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement

        super().setUp(class_methods_names_to_implement)