
import pytest
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TextCase(LibTrackTestCase):

    def test_random_then_ok(self):
        response = self._post_lib_track_with_specific_sample("Kemar - France.mp3")
        assert response.status_code == status.HTTP_201_CREATED
