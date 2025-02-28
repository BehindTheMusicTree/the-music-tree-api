from rest_framework import status

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_not_povided_then_set_from_filename_without_dots(self):
        response = self._post_lib_track(TestLibTrackFilename.FILENAME_DOT_NOT_IN_FILENAME_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename=dotnotinfilename"

    def test_not_povided_then_set_from_filename_with_dots(self):
        filename_without_extension = "dot.in.filename"
        response = self._post_lib_track(TestLibTrackFilename.FILENAME_DOT_IN_FILENAME_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == filename_without_extension

    def test_not_povided_then_set_from_filename_with_spaces_removing_extra_spaces(self):
        response = self._post_lib_track(TestLibTrackFilename.FIL)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == title_expected

    def test_not_povided_then_set_from_filename_with_expression_to_exclude(self):
        filename_with_extension = "dodido myfreemp3.vip .mp3"
        title_expected = "dodido"
        response = self._post_lib_track(filename_with_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == title_expected
