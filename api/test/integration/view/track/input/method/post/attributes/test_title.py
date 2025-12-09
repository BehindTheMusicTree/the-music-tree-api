from rest_framework import status

from api import settings
from api.test.utils.track.TrackTestFilename import TrackTestFilename
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_not_povided_then_set_from_filename_without_dots(self):
        response = self._post_track(TrackTestFilename.FILENAME_DOTNOTINFILENAME_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename=dotnotinfilename"

    def test_not_povided_then_set_from_filename_with_dots(self):
        response = self._post_track(TrackTestFilename.FILENAME_DOT_IN_FILENAME_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename=dot.in.filename"

    def test_not_povided_then_set_from_filename_with_spaces_removing_extra_spaces(self):
        response = self._post_track(TrackTestFilename.FILENAME_WITH_SPACES_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename= with spaces"
