from bodzify_api.test.field.filter.FilterTestCase import FilterTestCase


class EnumCharFilterTestCase(FilterTestCase):

    def setUp(self, specific_values: list[str], allow_empty_value, methods_names_to_implement=None):
        class_methods_to_implement = [
            'test_value_is_wrong_then_error',
            *[f'test_value_is_{specific_value}_then_results' for specific_value in specific_values]
        ]
        if methods_names_to_implement:
            class_methods_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement=methods_names_to_implement, allow_empty_value=allow_empty_value)
