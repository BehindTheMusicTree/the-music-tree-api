from rest_framework import status

from api import settings
from api.test.utils.track.TrackTestFilename import TrackTestFilename
from api.test.utils.track.TrackDownloadTestUrl import TrackDownloadTestUrl
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

    def test_not_providing_title_nor_artist_and_original_filename_too_long_then_generate_with_app_prefixe(self):
        response = self._post_track_from_url(TrackDownloadTestUrl.LONG_MP3)

        assert True
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title.startswith(settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE)
