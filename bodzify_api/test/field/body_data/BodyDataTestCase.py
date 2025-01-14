
from typing import Optional
from bodzify_api.test.ApiTestCase import ApiTestCase


class BodyDataTestCase(ApiTestCase):

    def setUp(self, methods_names_to_implement: Optional[list[str]] = None) -> None:
        class_methods_names_to_implement = ['test_not_provided_then_unchanged', 'test_not_none_then_update']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(methods_names_to_implement=class_methods_names_to_implement)
