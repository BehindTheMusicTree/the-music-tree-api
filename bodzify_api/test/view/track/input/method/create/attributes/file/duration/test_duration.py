from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_short_wav_then_ok(self):
        response = self._post_lib_track_with_generic_sample_no_tags(extension='wav')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.duration_in_sec == self.SAMPLE_LIB_TRACK_WAV_DURATION

    def test_normal_wav_then_ok(self):
        response = self._post_lib_track_with_specific_sample('carminaremix_472s.wav')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.duration_in_sec == 472

    def test_wav_with_issues_while_reading_duration_from_mutagen_and_tynitag_then_ok(self):
        response = self._post_lib_track_with_specific_sample(
            '1_sec_but_issue_with_duration_reading_from_mutagen_and_tynitag.wav')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.duration_in_sec == 1

    def test_short_mp3_then_ok(self):
        response = self._post_lib_track_with_generic_sample_no_tags(extension='mp3')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.duration_in_sec == self.SAMPLE_LIB_TRACK_MP3_DURATION

    def test_normal_mp3_then_ok(self):
        response = self._post_lib_track_with_specific_sample('showmustgoon_277s.mp3')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.duration_in_sec == 277

    def test_flac_then_ok(self):
        response = self._post_lib_track_with_generic_sample_no_tags(extension='flac')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.duration_in_sec == self.SAMPLE_LIB_TRACK_FLAC_DURATION

    def test_normal_flac_then_ok(self):
        response = self._post_lib_track_with_specific_sample('drown_440s.flac')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.duration_in_sec == 440
