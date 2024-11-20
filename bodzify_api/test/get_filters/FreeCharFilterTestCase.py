from typing import Optional

from bodzify_api.test.get_filters.FilterTestCase import FilterTestCase


class FreeCharFilterTestCase(FilterTestCase):
    filter_field = None

    def setUp(self, allow_empty_value: bool = False, methods_names_to_implement: Optional[list[str]] = None) -> None:
        class_methods_names_to_implement = ['test_contains_in_another_case_then_results']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(allow_empty_value=allow_empty_value, methods_names_to_implement=class_methods_names_to_implement)
