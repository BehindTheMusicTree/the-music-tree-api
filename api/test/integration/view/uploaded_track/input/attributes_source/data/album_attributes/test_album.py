from rest_framework import status

from api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_value_then_ok(self):
        value = 'fofof'
        data = {PostFields.ALBUM_NAME: value, PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: []}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == value

    def test_empty_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.ALBUM_NAME: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None
