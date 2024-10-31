
import pytest
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_missing_then_error(self):
        response = self._post_lib_track_without_file()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
