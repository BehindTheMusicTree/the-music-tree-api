from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_value_then_ok(self):
        value = 'rovk'
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: value})
        assert response.status_code == status.HTTP_201_CREATED
        genre = self.saved_object.genre
        assert genre
        assert genre.name == value

    def test_empty_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None
