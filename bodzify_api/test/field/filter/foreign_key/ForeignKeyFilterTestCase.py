from bodzify_api.test.field.filter.FilterTestCase import FilterTestCase


class ForeignKeyFilterTestCase(FilterTestCase):

    def setUp(self, allow_empty_value, methods_names_to_implement=None):
        class_methods_to_implement = ['test_exists_then_ok',
                                      'test_does_not_exist_then_no_results',
                                      'test_empty_then_results_with_no_foreign_object']
        if methods_names_to_implement:
            class_methods_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement=methods_names_to_implement, allow_empty_value=allow_empty_value)
