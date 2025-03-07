

from bodzify_api.test.utils.ApiTestCase import ApiTestCase


class ForeignKeyBodyDataTestCase(ApiTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_value_then_ok',
                                            'test_empty_then_none',
                                            'test_multi_value_then_400',
                                            'test_non_existing_then_400',
                                            'test_invalid_uuid_then_400']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)
