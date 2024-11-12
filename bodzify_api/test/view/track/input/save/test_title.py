from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.lib_track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_longest_then_ok(self):
        value = "a" * settings.LIB_TRACK_TITLE_LEN_MAX
        data = {PutFields.TITLE: value}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == value

    def test_too_long_then_error(self):
        value = "a" * (settings.LIB_TRACK_TITLE_LEN_MAX + 1)
        data = {PutFields.TITLE: value}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
