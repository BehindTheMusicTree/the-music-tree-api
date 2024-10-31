
from rest_framework import status

from bodzify_api.serializer.schema.track.input.endpoint.post import \
    Fields as PostFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_title_in_both_then_take_data(self):
        data_title = "Rock"
        data_dict = {PostFields.TITLE: data_title}
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == data_title
