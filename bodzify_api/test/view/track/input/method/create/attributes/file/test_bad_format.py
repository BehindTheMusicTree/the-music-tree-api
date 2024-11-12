import pytest

from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TextCase(LibTrackTestCase):

    def test_bad_format_then_error(self):
        response = self._post_lib_track_with_specific_sample("bad_format.wav")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
