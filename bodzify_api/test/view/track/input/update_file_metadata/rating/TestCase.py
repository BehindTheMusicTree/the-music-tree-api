from bodzify_api.utils.audio_metadata.AppMetadataKeys import AppMetadataKeys
from bodzify_api.serializer.model.lib_track.input.Fields import Fields as InoutFields
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataIntTestCase import \
    UpdateFileMetadataIntTestCase


class UpdateFileMetadataRatingTestCase(UpdateFileMetadataIntTestCase):
    save_field = InoutFields.RATING
    lib_track_app_metadata_key = AppMetadataKeys.RATING
    value_min = 0
    value_max = 10
    value_min_expected_in_metadata = 0


class FlacTestCase(UpdateFileMetadataRatingTestCase):
    file_extension = 'flac'
    value_max_expected_in_metadata = 100

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


class Mp3TestCase(UpdateFileMetadataRatingTestCase):
    file_extension = 'mp3'
    value_max_expected_in_metadata = 255

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


class WavTestCase(UpdateFileMetadataRatingTestCase):
    file_extension = 'wav'
    value_max_expected_in_metadata = 255

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
