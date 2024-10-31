
import datetime

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_multiple_release_dates_then_earliest(self):
        response = self._post_lib_track_with_specific_sample("queen_multiple_release_dates.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.musicbrainz_recording
        assert self.saved_lib_track.track_file.musicbrainz_recording.release_date == datetime.date(1977, 10, 28)
