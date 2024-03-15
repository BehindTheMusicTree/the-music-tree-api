#!/usr/bin/env python

from bodzify_api.test.view.track.input.save.FieldStrNullableTestCase import FieldStrNullableTestCase


class FieldModelStrTestCase(FieldStrNullableTestCase):

    def setUp(self):
        return super().setUp(methods_names_to_implement=['test_existing', 'test_not_existing'])
