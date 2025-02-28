
from bodzify_api.test.utils.ApiTestCase import ApiTestCase


class NotNullableCharBodyDataTestCase(ApiTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_longest_then_ok',
                                            'test_too_large_then_400',
                                            'test_empty_then_400',
                                            'test_list_then_400',]
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement)
