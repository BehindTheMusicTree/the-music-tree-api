from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_ok_when_max_length(self):
        sample_150_char_long_char_name = ("kwPD6Zd3y5hQxbyFbNq895XZyFf7ycvJJ0Nf4vK5cFX5vt53fB8670j63Mx2" +
                                          "ruMgVZ46B78iqu6vQpJ7hytZLbbv5Q1L6tiP6MfZAF" +
                                          "RnidA8RrEKPnCxbNRUkQtdzBub7TW5zn0MuKqX5GzGd5.mp3")
        response = self._post_lib_track_with_specific_sample(
            specific_sample_filename=sample_150_char_long_char_name, data_dict={})
        assert response.status_code == status.HTTP_201_CREATED

    def test_error_when_too_long(self):
        sample_151_char_long_char_name = ("kwPD6Zd3y5hQxbyFbNq895XZyFf7ycvJJ0Nf4vK5cFX5vt53fB8670j63Mx2" +
                                          "ruMgVZ46B78iqu6vQpJ7hytZLbbv5Q1L6tiP6MfZAF" +
                                          "RnidA8RrEKPnCxbNRUkQtdzBub7TW5zn0MuKqX5GzGd51.mp3")
        response = self._post_lib_track_with_specific_sample(
            specific_sample_filename=sample_151_char_long_char_name, data_dict={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
