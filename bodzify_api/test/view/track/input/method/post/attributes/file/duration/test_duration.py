from rest_framework import status


from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_short_wav_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.DURATION_LESS_THAN_1_SEC_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.duration_in_sec == 1
        assert self.saved_object.track_file.duration_in_sec == 1

    def test_SMALL_MP3_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.DURATION_LESS_THAN_1_SEC_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.duration_in_sec == 1

    def test_short_flac_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.DURATION_LESS_THAN_1_SEC_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.duration_in_sec == 1

    def test_normal_wav_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.DURATION_472S_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.duration_in_sec == 472

    def test_wav_with_issues_while_reading_duration_from_mutagen_and_tynitag_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.DURATION_1S_ISSUE_READING_FROM_MUTAGEN_AND_TYNITAG_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_normal_mp3_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.DURATION_277S_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.duration_in_sec == 277

    def test_normal_flac_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.DURATION_335S_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.duration_in_sec == 335
