
from rest_framework import status


from bodzify_api.serializer.schema.track.output.Fields import Fields as LibTrackFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase
from bodzify_api.utils.utils import to_camel_case


class TestCase(LibTrackTestCase):

    def test_filter_not_existing_then_error(self):
        response = self._get_lib_tracks(sdkfhsdkjfhskjfh='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
