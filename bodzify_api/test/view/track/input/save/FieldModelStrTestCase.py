#!/usr/bin/env python

from bodzify_api.test.view.track.input.save.FieldStrTestCase import FieldStrTestCase


class FieldModelStrTestCase(FieldStrTestCase):

    def setUp(self):
        return super().setUp(methods_names_to_implement=['test_existing',
                                                         'test_not_existing'])
