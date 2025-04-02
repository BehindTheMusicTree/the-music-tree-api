"""
This module provides a base test case for required fields that accept multiple values in multipart/form-data.

Array notation with the [] suffix is required for sending multiple values in multipart/form-data:

Example for multiple values:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]=value1' \\
  --form 'field[]=value2'
```

Since this test case is for non-nullable fields, the following should result in validation errors:
a) Omitting the field completely
b) Sending an empty array:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]='
```
c) Sending an explicit empty array:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]=[]'
```

Advantages of array notation with [] suffix for multipart:
- Explicit about sending multiple values
- Follows form submission conventions
- Makes it easier to add/remove values
- Avoids potential issues with comma escaping
- Consistent with HTML form handling

Other methods like repeated fields or comma-separated values are not supported and will result in validation errors.
"""

from bodzify_api.test.utils.AppTestCase import AppTestCase


class NotNullableMultipartListBodyDataTestCase(AppTestCase):
    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = [
            'test_multipart_array_largest_then_ok',
            'test_multipart_array_empty_then_400_bad_request',
            'test_multipart_array_one_too_large_then_400_bad_request',
            'test_multipart_array_multiple_with_one_too_large_then_400_bad_request',
            'test_multipart_array_multiple_with_one_empty_then_400_bad_request',
            'test_multipart_array_malformed_array_then_400_bad_request',
            'test_multipart_array_duplicate_values_then_400_bad_request',
        ]
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement

        super().setUp(class_methods_names_to_implement)