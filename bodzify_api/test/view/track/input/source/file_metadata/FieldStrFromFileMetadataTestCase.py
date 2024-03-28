#!/usr/bin/env python

import pytest

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class FieldStrNullableFromFileMetadataTestCase(TrackTestCase):

    def setUp(self):
        super().setUp(methods_names_to_implement=['test_none_then_none', 'test_longest'])
