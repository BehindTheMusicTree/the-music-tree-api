from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_none_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.ALBUM_KOKO_ID3V2_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 0

    def test_max_id3v1_small_file_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_ID3V1_SMALL_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 1
        artist = self.saved_object.artists.first()
        assert artist
        assert artist.name == 'a' * settings.ARTIST_NAME_LEN_MAX_ID3V1

    def test_max_id3v1_big_file_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_ID3V1_BIG_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 1
        artist = self.saved_object.artists.first()
        assert artist
        assert artist.name == 'a' * settings.ARTIST_NAME_LEN_MAX_ID3V1

    def test_long_id3v2_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 1
        artist = self.saved_object.artists.first()
        assert artist
        assert len(artist.name) == settings.ARTIST_NAME_LEN_MAX
        assert artist.name == 'a' * settings.ARTIST_NAME_LEN_MAX

    def test_long_riff_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_RIFF_SMALL_WAV)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 1
        artist = self.saved_object.artists.first()
        assert artist
        assert len(artist.name) == settings.ARTIST_NAME_LEN_MAX
        assert artist.name == 'a' * settings.ARTIST_NAME_LEN_MAX

    def test_long_vorbis_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 1
        artist = self.saved_object.artists.first()
        assert artist
        assert len(artist.name) == settings.ARTIST_NAME_LEN_MAX
        assert artist.name == 'a' * settings.ARTIST_NAME_LEN_MAX

    def test_3_separated_by_antislash_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.ARTISTS_ONE_TWO_THREE_ANTISLASH_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 3
        artists = self.saved_object.artists.all()
        assert [artist.name for artist in artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_comma_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.ARTISTS_ONE_TWO_THREE_COMMA_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 3
        artists = self.saved_object.artists.all()
        assert [artist.name for artist in artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_double_antislash_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.ARTISTS_ONE_TWO_THREE_DOUBLE_ANTISLASH_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 3
        artists = self.saved_object.artists.all()
        assert [artist.name for artist in artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_double_slash_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.ARTISTS_ONE_TWO_THREE_DOUBLE_SLASH_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 3
        artists = self.saved_object.artists.all()
        assert [artist.name for artist in artists] == ['One', 'Two', 'Three']

    def test_3_multi_tags_and_slash_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.ARTISTS_ONE_TWO_THREE_MULTI_TAGS_AND_SLASH_VORBIS)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 3
        artists = self.saved_object.artists.all()
        assert [artist.name for artist in artists] == ['One', 'Two', 'Three']

    def test_3_multi_tags_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.ARTISTS_ONE_TWO_THREE_MULTI_TAGS_VORBIS)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 3
        artists = self.saved_object.artists.all()
        assert [artist.name for artist in artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_semicolon_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.ARTISTS_ONE_TWO_THREE_SEMICOLON_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 3
        artists = self.saved_object.artists.all()
        assert [artist.name for artist in artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_slash_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.ARTISTS_ONE_TWO_THREE_SLASH_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 3
        artists = self.saved_object.artists.all()
        assert [artist.name for artist in artists] == ['One', 'Two', 'Three']
