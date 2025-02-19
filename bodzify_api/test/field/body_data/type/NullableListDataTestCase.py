"""
This module provides a base test case for fields that accept multiple values in multipart/form-data.

Array notation is the only supported way to send multiple values in multipart/form-data:

Example for multiple values:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/v0.1.1/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]=value1' \\
  --form 'field[]=value2'
```

To send a null value using array notation, you can:
a) Omit the field completely
b) Send an empty array:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/v0.1.1/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]='
```
c) Send an explicit empty array:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/v0.1.1/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]=[]'
```

Advantages of array notation:
- Explicit about sending multiple values
- Follows REST API best practices
- Makes it easier to add/remove values
- Avoids potential issues with comma escaping
- Consistent with HTML form handling

Other methods like repeated fields or comma-separated values are not supported and will result in validation errors.
"""

from bodzify_api.test.ApiTestCase import ApiTestCase


class NullableListDataTestCase(ApiTestCase):
    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        list_methods_to_implement = [
            'test_too_long_then_error',
            'test_longest_then_ok',
            'test_array_notation_then_ok',
            'test_empty_array_then_none',
            'test_values_with_one_empty_then_error',
            'test_non_array_then_error',
            'test_comma_separated_then_only_one_value',
            'test_duplicate_values_then_error',
            'test_malformed_array_field_name_then_error'
        ]
        if methods_names_to_implement:
            list_methods_to_implement += methods_names_to_implement

        super().setUp(methods_names_to_implement=list_methods_to_implement)
