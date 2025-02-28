

from bodzify_api.test.utils.ApiTestCase import ApiTestCase


class FilterTestCase(ApiTestCase):
    filter_field = None

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_not_provided_then_results']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(methods_names_to_implement=class_methods_names_to_implement)
