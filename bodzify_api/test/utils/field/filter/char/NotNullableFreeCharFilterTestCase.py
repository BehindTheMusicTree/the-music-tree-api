

from bodzify_api.test.utils.field.filter.char.FreeCharFilterTestCase import     FreeCharFilterTestCase


class NotNullableFreeCharFilterTestCase(FreeCharFilterTestCase):
    filter_field = None

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_contains_in_another_case_then_results']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(allow_empty_value=False, methods_names_to_implement=class_methods_names_to_implement)
