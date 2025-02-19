from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post.post import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_rating_in_both_then_take_data(self):
        data_rating = 7
        response = self._post_lib_track_with_generic_sample_1_star(**{PostFields.RATING: data_rating})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == data_rating
