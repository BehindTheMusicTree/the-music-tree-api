from rest_framework import status

from bodzify_api.serializer.schema.lib_track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import FieldIntFromDataTestCase


class RatingTestCase(FieldIntFromDataTestCase):
    post_field_key = PostFields.RATING

    def test_value_then_ok(self):
        value = 1
        response = self._post_lib_track_with_generic_sample_no_tags(kwargs={PostFields.RATING: value})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == value

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_1_star(kwargs={PostFields.RATING: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == None
