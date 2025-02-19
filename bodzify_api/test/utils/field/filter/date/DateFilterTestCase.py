from bodzify_api.test.field.filter.FilterTestCase import FilterTestCase


class DateFilterTestCase(FilterTestCase):

    def setUp(self, methods_names_to_implement=None):
        class_methods_to_implement = ['test_format_is_wrong_then_error']
        if methods_names_to_implement:
            class_methods_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement=methods_names_to_implement, allow_empty_value=False)
