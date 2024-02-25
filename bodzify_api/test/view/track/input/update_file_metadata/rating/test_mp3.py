#!/usr/bin/env python

from bodzify_api.test.view.track.input.update_file_metadata.rating.UpdateFileMetadataRatingTestCase \
    import UpdateFileMetadataRatingTestCase


class TestCase(UpdateFileMetadataRatingTestCase):
    file_extension = 'mp3'
    value_max_in_metadata = 255

    def setUp(self):
        super().setUp()
        self.file_extension = 'mp3'
        self.value_max_in_metadata = 255

    def test_on_missing_tag_then_ok(self):
        super().test_on_missing_tag_then_ok()

    def test_on_present_tag_then_ok(self):
        super().test_on_present_tag_then_ok()

    def test_max_then_ok(self):
        super().test_max_then_ok()

    def test_min_then_ok(self):
        super().test_min_then_ok()

    def test_none_then_none(self):
        super().test_none_then_none()

    def test_0_then_0(self):
        self._test_value(0, 0)

    def test_1_then_13(self):
        self._test_value(1, 13)

    def test_2_then_1(self):
        self._test_value(0, 0)

    def test_3_then_54(self):
        self._test_value(3, 54)

    def test_4_then_64(self):
        self._test_value(4, 64)

    def test_5_then_118(self):
        self._test_value(5, 118)

    def test_6_then_128(self):
        self._test_value(6, 128)

    def test_7_then_186(self):
        self._test_value(7, 186)

    def test_8_then_196(self):
        self._test_value(8, 196)

    def test_9_then_242(self):
        self._test_value(9, 242)

    def test_10_then_255(self):
        self._test_value(10, 255)
