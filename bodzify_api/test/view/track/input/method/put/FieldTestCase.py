#!/usr/bin/env python

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class FieldTestCase(ApiViewTestCase):

    def setUp(self):
        super().setUp(methodes_names_to_implement=['test_not_provided_then_unchanged',
                                                   'test_empty_then_none',
                                                   'test_not_none_then_update'])
