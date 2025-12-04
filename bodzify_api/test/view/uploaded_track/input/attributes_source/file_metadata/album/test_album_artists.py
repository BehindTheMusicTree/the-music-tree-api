from rest_framework import status
from django.db.models.query import QuerySet

from bodzify_api import settings
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_none_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_KOKO_ID3V2_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.album_artists.count() == 0

    def test_long_id3v2_then_truncated(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)
        assert response.status_code == status.HTTP_201_CREATED

        assert self.saved_object.album
        assert self.saved_object.album.album_artists.count() == 1
        artist: Artist | None = self.saved_object.album.album_artists.first()
        assert artist
        assert len(artist.name) == settings.ARTIST_NAME_LEN_MAX
        assert artist.name == 'a' * settings.ARTIST_NAME_LEN_MAX

    def test_long_vorbis_then_truncated(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

        assert self.saved_object.album
        assert self.saved_object.album.album_artists.count() == 1
        artist: Artist | None = self.saved_object.album.album_artists.first()
        assert artist
        assert len(artist.name) == settings.ARTIST_NAME_LEN_MAX
        assert artist.name == 'a' * settings.ARTIST_NAME_LEN_MAX

    def test_3_separated_by_antislash_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_ARTISTS_ONE_TWO_THREE_ANTISLASH_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        album_artists: QuerySet[Artist] = self.saved_object.album.album_artists.all()
        assert album_artists.count() == 3
        assert [artist.name for artist in album_artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_comma_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_ARTISTS_ONE_TWO_THREE_COMMA_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        album_artists: QuerySet[Artist] = self.saved_object.album.album_artists.all()
        assert album_artists.count() == 3
        assert [artist.name for artist in album_artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_double_antislash_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.ALBUM_ARTISTS_ONE_TWO_THREE_DOUBLE_ANTISLASH_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        album_artists: QuerySet[Artist] = self.saved_object.album.album_artists.all()
        assert album_artists.count() == 3
        assert [artist.name for artist in album_artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_double_slash_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_ARTISTS_ONE_TWO_THREE_DOUBLE_SLASH_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        album_artists: QuerySet[Artist] = self.saved_object.album.album_artists.all()
        assert album_artists.count() == 3
        assert [artist.name for artist in album_artists] == ['One', 'Two', 'Three']

    def test_3_multi_tags_and_slash_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.ALBUM_ARTISTS_ONE_TWO_THREE_MULTI_TAGS_AND_SLASH_VORBIS)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        album_artists: QuerySet[Artist] = self.saved_object.album.album_artists.all()
        assert album_artists.count() == 2
        assert [artist.name for artist in album_artists] == ['One', 'Two/Three']

    def test_3_multi_tags_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_ARTISTS_ONE_TWO_THREE_MULTI_TAGS_VORBIS)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        album_artists: QuerySet[Artist] = self.saved_object.album.album_artists.all()
        assert album_artists.count() == 3
        assert [artist.name for artist in album_artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_semicolon_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_ARTISTS_ONE_TWO_THREE_SEMICOLON_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        album_artists: QuerySet[Artist] = self.saved_object.album.album_artists.all()
        assert album_artists.count() == 3
        assert [artist.name for artist in album_artists] == ['One', 'Two', 'Three']

    def test_3_separated_by_slash_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_ARTISTS_ONE_TWO_THREE_SLASH_ID3V2)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        album_artists: QuerySet[Artist] = self.saved_object.album.album_artists.all()
        assert album_artists.count() == 3
        assert [artist.name for artist in album_artists] == ['One', 'Two', 'Three']
