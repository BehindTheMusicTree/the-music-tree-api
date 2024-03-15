#!/usr/bin/env python

import logging

from bodzify_api.test.get_filters.GetFilterTestCase import GetFilterTestCase

logger = logging.getLogger('bodyzify_api')


class GetFilterWithSpecificValuesTestCase(GetFilterTestCase):

    def setUp(self, specific_values: list[str], allow_empty_value, methods_names_to_implement=None):
        class_methods_to_implement = ['test_value_is_wrong_then_error']
        class_methods_to_implement += [
            f'test_value_is_{specific_value}_then_results' for specific_value in specific_values]
        if methods_names_to_implement:
            class_methods_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement=methods_names_to_implement, allow_empty_value=allow_empty_value)
