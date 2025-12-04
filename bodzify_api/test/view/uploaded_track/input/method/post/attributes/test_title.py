from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.utils.uploaded_track.UploadedTrackDownloadTestUrl import UploadedTrackDownloadTestUrl
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_not_povided_then_set_from_filename_without_dots(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FILENAME_DOTNOTINFILENAME_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename=dotnotinfilename"

    def test_not_povided_then_set_from_filename_with_dots(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FILENAME_DOT_IN_FILENAME_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename=dot.in.filename"

    def test_not_povided_then_set_from_filename_with_spaces_removing_extra_spaces(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FILENAME_WITH_SPACES_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename= with spaces"

    def test_not_providing_title_nor_artist_and_original_filename_too_long_then_generate_with_app_prefixe(self):
        response = self._post_uploaded_track_from_url(UploadedTrackDownloadTestUrl.LONG_MP3)

        assert True
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title.startswith(settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE)
