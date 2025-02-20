from typing import Optional

from bodzify_api.test.ApiTestCase import ApiTestCase


class FilterTestCase(ApiTestCase):
    filter_field = None

    def setUp(self, allow_empty_value, methods_names_to_implement: Optional[list[str]] = None) -> None:
        class_methods_names_to_implement = [f'test_empty_then_{"results" if allow_empty_value else "error"}',
                                            'test_not_provided_then_results']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(methods_names_to_implement=class_methods_names_to_implement)
