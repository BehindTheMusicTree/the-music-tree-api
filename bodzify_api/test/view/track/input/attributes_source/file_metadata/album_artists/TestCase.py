from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.view.track.input.attributes_source.file_metadata.FieldStrFromFileMetadataTestCase import     FieldStrNullableFromFileMetadataTestCase


class TestCase(FieldStrNullableFromFileMetadataTestCase):
    file_extension: str

    def test_none_then_none(self):
        response = \
            self._post_lib_track_with_generic_sample_tag_album_koko_without_album_artists(extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.album_artists.count() == 0

    def test_longest_then_ok(self):
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED

        expected_name = 'a' * settings.ARTIST_NAME_LEN_MAX
        album = self.saved_object.album
        assert album
        assert album.name == expected_name


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
