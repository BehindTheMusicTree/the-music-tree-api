

from bodzify_api.test.utils.field.filter.FilterTestCase import FilterTestCase


class CharFilterTestCase(FilterTestCase):
    filter_field = None

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_contains_in_another_case_then_results',
                                            'test_empty_then_results',]
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(methods_names_to_implement=class_methods_names_to_implement)
