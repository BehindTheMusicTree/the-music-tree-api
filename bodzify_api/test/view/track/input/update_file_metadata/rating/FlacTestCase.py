#!/usr/bin/env python

import logging
from bodzify_api.test.view.track.input.update_file_metadata.rating.UpdateFileMetadataRatingTestCase \
    import UpdateFileMetadataRatingTestCase

logger = logging.getLogger('bodzify_api')


class FlacTestCase(UpdateFileMetadataRatingTestCase):
    file_extension = 'flac'
    value_max_in_metadata = 100

    def test_1_then_10(self):
        self._test_value(1, 10)

    def test_2_then_20(self):
        self._test_value(2, 20)

    def test_3_then_30(self):
        self._test_value(3, 30)

    def test_4_then_40(self):
        self._test_value(4, 40)

    def test_5_then_50(self):
        self._test_value(5, 50)

    def test_6_then_60(self):
        self._test_value(6, 60)

    def test_7_then_70(self):
        self._test_value(7, 70)

    def test_8_then_80(self):
        self._test_value(8, 80)

    def test_9_then_90(self):
        self._test_value(9, 90)

    def test_10_then_100(self):
        self._test_value(10, 100)
