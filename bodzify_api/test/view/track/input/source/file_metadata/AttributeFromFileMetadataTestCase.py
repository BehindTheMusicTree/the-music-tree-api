#!/usr/bin/env python

import pytest

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class FieldFromFileMetadataTestCase(ApiViewTestCase):

    def setUp(self):
        super().setUp(methodes_names_to_implenent=['test_none_then_none',
                                                   'test_longest'])
