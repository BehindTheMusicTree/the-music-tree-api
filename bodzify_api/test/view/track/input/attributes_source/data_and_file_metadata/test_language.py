from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_title_in_both_then_take_data(self):
        data_language = "fr"
        data_dict = {PostFields.LANGUAGE: data_language}
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == data_language
