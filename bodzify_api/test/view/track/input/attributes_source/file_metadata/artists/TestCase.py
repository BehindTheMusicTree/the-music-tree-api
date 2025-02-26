from rest_framework import status

from bodzify_api import settings
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.test.view.track.input.attributes_source.file_metadata.FieldStrFromFileMetadataTestCase import (
    FieldStrNullableFromFileMetadataTestCase
)


class TestCase(FieldStrNullableFromFileMetadataTestCase):
    file_extension: str

    def test_none_then_none(self) -> None:
        response = self._post_lib_track_with_generic_sample_no_tags(extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 0

    def test_longest_then_ok(self) -> None:
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == 'a' * settings.ARTIST_NAME_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
