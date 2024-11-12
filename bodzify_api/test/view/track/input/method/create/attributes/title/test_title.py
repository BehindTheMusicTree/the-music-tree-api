from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_not_povided_then_set_from_filename_without_dots(self):
        response = self._post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == self.LibTrackGenericSamplesFilenameWithoutExtension.TAGS_NONE

    def test_not_povided_then_set_from_filename_with_dots(self):
        filename_without_extension = "dot.in.filename"
        response = self._post_lib_track_with_specific_sample(filename_without_extension + ".mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == filename_without_extension

    def test_not_povided_then_set_from_filename_with_spaces_removing_extra_spaces(self):
        filename_with_extension = "with spaces  .mp3"
        title_expected = "with spaces"
        response = self._post_lib_track_with_specific_sample(filename_with_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == title_expected

    def test_not_povided_then_set_from_filename_with_expression_to_exclude(self):
        filename_with_extension = "dodido myfreemp3.vip .mp3"
        title_expected = "dodido"
        response = self._post_lib_track_with_specific_sample(filename_with_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == title_expected
