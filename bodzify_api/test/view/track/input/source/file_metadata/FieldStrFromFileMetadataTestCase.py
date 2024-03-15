#!/usr/bin/env python

import pytest

from bodzify_api.test.ApiTestCase import ApiTestCase


@pytest.mark.django_db
class FieldStrNullableFromFileMetadataTestCase(ApiTestCase):

    def setUp(self):
        super().setUp(methods_names_to_implement=['test_none_then_none',
                                                  'test_longest'])
