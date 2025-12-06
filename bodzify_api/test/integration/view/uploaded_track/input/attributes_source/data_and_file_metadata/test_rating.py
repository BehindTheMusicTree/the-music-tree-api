from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_rating_in_both_then_take_data(self):
        data_rating = 7
        response = self._post_uploaded_track(UploadedTrackTestFilename.RATING_ID3V2_1_STAR_MP3,
                                             **{PostFields.RATING: data_rating})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == data_rating
