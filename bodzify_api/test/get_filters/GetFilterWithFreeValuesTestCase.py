

from bodzify_api.test.get_filters.GetFilterTestCase import GetFilterTestCase


class GetFilterWithFreeValuesTestCase(GetFilterTestCase):
    filter_field = None

    def setUp(self, allow_empty_value, methods_names_to_implement=None):
        class_methods_names_to_implement = ['test_different_case_then_results']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(
            allow_empty_value=allow_empty_value, methods_names_to_implement=class_methods_names_to_implement)
