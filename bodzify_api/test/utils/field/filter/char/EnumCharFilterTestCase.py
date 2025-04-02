
from bodzify_api.test.utils.field.filter.FilterTestCase import FilterTestCase


class EnumCharFilterTestCase(FilterTestCase):

    def setUp(self, specific_values: list[str], methods_names_to_implement=None):
        class_methods_to_implement = [
            'test_invalid_enum_then_400_bad_request',
            'test_empty_then_400_bad_request',
            *[f'test_value_is_{specific_value}_then_results' for specific_value in specific_values]
        ]
        if methods_names_to_implement:
            class_methods_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement=methods_names_to_implement)
