from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_rating_in_both_then_take_data(self):
        data_rating = 7
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_1_STAR_MP3,
                                             **{PostFields.RATING: data_rating})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == data_rating
