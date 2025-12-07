"""
This module provides a base test case for required fields that accept multiple values in multipart/form-data.

In multipart/form-data requests, array notation with the [] suffix is REQUIRED:

Example for multiple values:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]=value1' \\
  --form 'field[]=value2'
```

Since this test case is for non-nullable fields, sending null values will result in validation errors:
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

For JSON requests, use NotNullableJsonListBodyDataTestCase which does NOT use the [] suffix.
"""

from api.test.utils.AppTestCase import AppTestCase


class NotNullableListBodyDataTestCase(AppTestCase):
    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_largest_then_ok',
                                            'test_empty_then_400_bad_request',
                                            'test_one_too_large_then_400_bad_request',
                                            'test_multiple_with_one_too_large_then_400_bad_request',
                                            'test_multiple_with_one_empty_then_400_bad_request',
                                            'test_malformed_array_then_400_bad_request',
                                            'test_duplicate_values_then_400_bad_request',]
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement

        super().setUp(class_methods_names_to_implement)
