from rest_framework import status


from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_short_wav_then_ok(self):
        response = self._post_track(duration_in_sec=1)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.duration_in_sec == 1

    def test_SMALL_MP3_then_ok(self):
        response = self._post_track(duration_in_sec=1)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.duration_in_sec == 1

    def test_short_flac_then_ok(self):
        response = self._post_track(duration_in_sec=1)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.duration_in_sec == 1

    def test_normal_wav_then_ok(self):
        response = self._post_track(duration_in_sec=472)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.duration_in_sec == 472

    def test_wav_with_issues_while_reading_duration_from_mutagen_and_tynitag_then_ok(self):
        response = self._post_track(duration_in_sec=1)
        assert response.status_code == status.HTTP_201_CREATED

    def test_normal_mp3_then_ok(self):
        response = self._post_track(duration_in_sec=277)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.duration_in_sec == 277

    def test_normal_flac_then_ok(self):
        response = self._post_track(duration_in_sec=335)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.duration_in_sec == 335
