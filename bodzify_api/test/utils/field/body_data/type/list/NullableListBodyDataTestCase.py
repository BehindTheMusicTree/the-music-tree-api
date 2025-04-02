"""
This module provides a base test case for nullable fields that accept multiple values in multipart/form-data.

In multipart/form-data requests, array notation with the [] suffix is REQUIRED:

Example for multiple values:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]=value1' \\
  --form 'field[]=value2'
```

To send a null value, you can:
a) Omit the field completely
b) Send an empty array:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]='
```
c) Send an explicit empty array:
```bash
curl --request POST \\
  --url http://127.0.0.1:8000/api/vX.Y.Z/endpoint/ \\
  --header 'content-type: multipart/form-data' \\
  --form 'field[]=[]'
```

For JSON requests, use NullableJsonListBodyDataTestCase which does NOT use the [] suffix.
"""

from bodzify_api.test.utils.AppTestCase import AppTestCase


class NullableListBodyDataTestCase(AppTestCase):
    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_largest_then_ok',
                                            'test_empty_then_ok',
                                            'test_comma_separated_then_only_one_value',
                                            'test_one_too_large_then_400_bad_request',
                                            'test_multiple_with_one_too_large_then_400_bad_request',
                                            'test_multiple_with_one_empty_then_400_bad_request',
                                            'test_malformed_array_then_400_bad_request',
                                            'test_duplicate_values_then_400_bad_request',]
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement

        super().setUp(class_methods_names_to_implement)
