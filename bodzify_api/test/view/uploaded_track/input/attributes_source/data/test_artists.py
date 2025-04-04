from rest_framework import status

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_value_then_ok(self) -> None:
        value = 'rovk'
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.ARTISTS_NAMES_MULTIPART: [value]})

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == value

    def test_empty_then_none(self) -> None:
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RATING_ID3V2_1_STAR_MP3, **{PostFields.ARTISTS_NAMES_MULTIPART: []})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 0
