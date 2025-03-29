

from bodzify_api.test.utils.field.filter.FilterTestCase import FilterTestCase


class NotNullableFreeCharFilterTestCase(FilterTestCase):
    filter_field = None

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_contains_in_another_case_then_results',
                                            'test_not_provided_then_results',
                                            'test_empty_then_400_bad_request',]
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(methods_names_to_implement=class_methods_names_to_implement)
