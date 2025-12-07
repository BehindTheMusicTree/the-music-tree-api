from rest_framework import status

from api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TitleTestCase(UploadedTrackTestCase):

    def test_value_then_ok(self):
        value = 'fr'
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TITLE: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == value
