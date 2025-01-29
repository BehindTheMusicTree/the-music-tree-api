from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_extra_field_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(
            **{PostFields.TITLE: "Rock", "extra_field": "extra_value"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
