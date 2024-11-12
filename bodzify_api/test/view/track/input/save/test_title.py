from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.lib_track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_longest_then_ok(self):
        value = "a" * settings.LIB_TRACK_TITLE_LEN_MAX
        response = self._post_lib_track_with_generic_sample_no_tags(kwargs={PutFields.TITLE: value})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == value

    def test_too_long_then_error(self):
        value = "a" * (settings.LIB_TRACK_TITLE_LEN_MAX + 1)
        response = self._post_lib_track_with_generic_sample_no_tags(kwargs={PutFields.TITLE: value})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
