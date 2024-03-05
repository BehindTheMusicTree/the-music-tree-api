#!/usr/bin/env python

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class FieldStrTestCase(ApiViewTestCase):

    def setUp(self, methods_names_to_implement=None):
        class_methods_to_implement = ['test_longest_then_ok',
                                      'test_too_long_then_error',
                                      'test_none_then_none']
        if methods_names_to_implement:
            class_methods_to_implement += methods_names_to_implement
        return super().setUp(methodes_names_to_implement=methods_names_to_implement)
