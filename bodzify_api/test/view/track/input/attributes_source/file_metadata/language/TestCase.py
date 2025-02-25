from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.view.track.input.attributes_source.file_metadata.FieldStrFromFileMetadataTestCase import \
    FieldStrNullableFromFileMetadataTestCase


class TestCase(FieldStrNullableFromFileMetadataTestCase):
    file_extension: str

    def test_none_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == None

    def test_longest_then_ok(self):
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == 'a' * settings.LIB_TRACK_LANGUAGE_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
