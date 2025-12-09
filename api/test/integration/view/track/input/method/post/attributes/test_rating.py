from rest_framework import status

from api.test.utils.track.TrackTestFilename import TrackTestFilename
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_not_povided_then_none(self):
        response = self._post_track(TrackTestFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None
