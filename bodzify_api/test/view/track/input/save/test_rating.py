
from rest_framework import status

from bodzify_api.serializer.schema.lib_track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_empty_then_none(self):
        data_dict = {PostFields.RATING: None}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == None

    def test_zero(self):
        rating = 0
        data_dict = {PostFields.RATING: rating}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == rating

    def test_four(self):
        rating = 4
        data_dict = {PostFields.RATING: rating}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == rating

    def test_ten(self):
        rating = 10
        data_dict = {PostFields.RATING: rating}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == rating

    def test_error_when_above_maximum(self):
        data_dict = {PostFields.RATING: 11}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_error_when_below_minimum(self):
        data_dict = {PostFields.RATING: -1}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_error_when_not_integer(self):
        data_dict = {PostFields.RATING: 5.5}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
