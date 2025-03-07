
from bodzify_api.test.utils.AppTestCase import AppTestCase


class NullableCharBodyDataTestCase(AppTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_longest_then_ok',
                                            'test_empty_then_ok',
                                            'test_too_large_then_400',
                                            'test_multi_value_then_400',]
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)
