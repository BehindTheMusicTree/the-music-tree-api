from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class LanguageTestCase(LibTrackTestCase):

    def test_value_then_ok(self):
        value = 'fr'
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.LANGUAGE: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == value

    def test_empty_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.LANGUAGE: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == None
