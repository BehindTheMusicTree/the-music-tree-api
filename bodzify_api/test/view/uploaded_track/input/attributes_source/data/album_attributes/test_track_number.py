from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_value_then_ok(self):
        value = 1
        data = {PostFields.ALBUM_NAME: 'albumito',
                PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: [],
                PostFields.TRACK_NUMBER: value}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == value

    def test_empty_then_none(self):
        data = {PostFields.ALBUM_NAME: "albumito",
                PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: [],
                PostFields.TRACK_NUMBER: None}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None

    def test_not_provided_then_none(self):
        data = {PostFields.ALBUM_NAME: "albumito", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: []}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None
