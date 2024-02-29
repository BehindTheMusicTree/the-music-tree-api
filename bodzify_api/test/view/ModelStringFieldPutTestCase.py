#!/usr/bin/env python

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class ModelStringFieldPutViewTestCase(ApiViewTestCase):
    
    def setUp(self):
        return super().setUp(methodes_names_to_implenent=['test_not_provided_then_unchanged',
                                                           'test_none_then_none',
                                                           'test_empty_then_none',
                                                           'test_not_none_then_update'])