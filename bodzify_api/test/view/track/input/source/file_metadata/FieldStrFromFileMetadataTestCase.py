#!/usr/bin/env python

import pytest

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class FieldStrFromFileMetadataTestCase(ApiViewTestCase):

    def setUp(self):
        super().setUp(methodes_names_to_implement=['test_none_then_none',
                                                   'test_longest'])
