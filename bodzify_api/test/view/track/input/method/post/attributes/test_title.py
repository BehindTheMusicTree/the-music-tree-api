from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.utils.lib_track.TestLibTrackUrl import TestLibTrackUrl
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_not_povided_then_set_from_filename_without_dots(self):
        response = self._post_lib_track(TestLibTrackFilename.FILENAME_DOT_NOT_IN_FILENAME_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename=dotnotinfilename"

    def test_not_povided_then_set_from_filename_with_dots(self):
        response = self._post_lib_track(TestLibTrackFilename.FILENAME_DOT_IN_FILENAME_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename=dot.in.filename"

    def test_not_povided_then_set_from_filename_with_spaces_removing_extra_spaces(self):
        response = self._post_lib_track(TestLibTrackFilename.FILENAME_SPACES_TRAILING_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename= with spaces"

    def test_not_providing_title_nor_artist_and_original_filename_too_long_then_generate_with_app_prefixe(self):
        response = self._post_lib_track_from_url(TestLibTrackUrl.LONG_MP3)

        assert True
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title.startswith(settings.LIB_TRACK_GENERATED_TITLE_PREFIXE)
