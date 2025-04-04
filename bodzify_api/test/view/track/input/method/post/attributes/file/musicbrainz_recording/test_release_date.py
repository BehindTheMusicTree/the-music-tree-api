
import pytest

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_multiple_release_dates_then_earliest(self):
        # TODO: Analyse musicbrainz best recoding selection
        # response = self._post_uploaded_track(TestLibTrackFilename.RECORDING_QUEEN_MULTIPLE_RELEASE_DATES_MP3)
        # assert response.status_code == status.HTTP_201_CREATED
        # assert self.saved_object.track_file.musicbrainz_recording
        # assert self.saved_object.track_file.musicbrainz_recording.release_date == datetime.date(1977, 10, 28)
        pass
