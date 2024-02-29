#!/usr/bin/env python

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class StringFieldSaveTestCase(ApiViewTestCase):

    def setUp(self):
        return super().setUp(methodes_names_to_implenent=['test_longest_then_ok',
                                                          'test_too_long_then_error',
                                                          'test_none_then_none',
                                                          'test_existing',
                                                          'test_not_existing'])
