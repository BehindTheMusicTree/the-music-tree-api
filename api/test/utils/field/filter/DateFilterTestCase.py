

from api.test.utils.field.filter.FilterTestCase import FilterTestCase


class DateFilterTestCase(FilterTestCase):

    def setUp(self, methods_names_to_implement=None):
        class_methods_to_implement = ['test_date_then_results',
                                      'test_format_is_wrong_then_400_bad_request',
                                      'test_empty_then_400_bad_request']
        if methods_names_to_implement:
            class_methods_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement=methods_names_to_implement)
