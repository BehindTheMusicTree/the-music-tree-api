import pytest
from rest_framework import status

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TextCase(LibTrackTestCase):

    def test_random_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.RECORDING_KEMAR_FRANCE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
