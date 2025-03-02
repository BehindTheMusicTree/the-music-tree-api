from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class RatingTestCase(LibTrackTestCase):

    def test_value_then_ok(self):
        value = 1
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.RATING: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == value

    def test_empty_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.RATING: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None
