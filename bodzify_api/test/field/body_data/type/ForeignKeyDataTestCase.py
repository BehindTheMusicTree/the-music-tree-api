from bodzify_api.test.ApiTestCase import ApiTestCase


class ForeignKeyDataTestCase(ApiTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_non_existing_then_error',
                                            'test_value_then_ok',
                                            'test_empty_then_none',
                                            'test_multiple_values_then_error',
                                            'test_invalid_uuid_then_error']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement)
