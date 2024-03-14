#!/usr/bin/env python

import logging

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from rest_framework import status

logger = logging.getLogger('bodyzify_api')


class GetFilterTestCase(ApiViewTestCase):
    filter_field = None

    def setUp(self, methods_names_to_implement=None):
        class_methods_names_to_implement = ['test_filter_is_empty_then_results',
                                            'test_filter_is_not_provided_then_results']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement=class_methods_names_to_implement)
