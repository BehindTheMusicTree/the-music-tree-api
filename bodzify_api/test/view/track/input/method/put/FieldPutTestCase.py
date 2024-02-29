#!/usr/bin/env python

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class FieldFromPutTestCase(ApiViewTestCase):

    def setUp(self):
        super().setUp(methodes_names_to_implenent=['test_not_provided_then_unchanged',
                                                   'test_empty_then_none',
                                                   'test_not_none_then_update'])
