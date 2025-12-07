from api.test.utils.AppTestCase import AppTestCase


class PrimaryCharBodyDataTestCase(AppTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_largest_then_ok',
                                            'test_too_large_then_400_bad_request',
                                            'test_empty_then_400_bad_request',
                                            'test_multi_value_then_400_bad_request',
                                            'test_already_exists_then_400_bad_request']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)
