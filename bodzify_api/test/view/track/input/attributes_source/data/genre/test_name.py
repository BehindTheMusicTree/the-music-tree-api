from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_value_then_ok(self):
        value = 'rovk'
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: value})
        assert response.status_code == status.HTTP_201_CREATED
        genre = self.saved_object.genre
        assert genre
        assert genre.name == value

    def test_empty_then_none(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None
