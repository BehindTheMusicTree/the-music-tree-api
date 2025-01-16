
from typing import Optional
from bodzify_api.test.ApiTestCase import ApiTestCase


class SaveBodyDataTestCase(ApiTestCase):

    def setUp(self, methods_names_to_implement: Optional[list[str]] = None) -> None:
        class_methods_names_to_implement = ['test_longest_then_ok',
                                            'test_too_long_then_error',
                                            'test_multiple_values_then_error']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(methods_names_to_implement=class_methods_names_to_implement)
