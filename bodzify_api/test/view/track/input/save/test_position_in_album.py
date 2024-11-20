from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.lib_track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.POSITION_IN_ALBUM: None})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.position_in_album == None

    def test_zero_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.POSITION_IN_ALBUM: 0})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_one_then_ok(self):
        position_in_album = 1

        data_dict = {PostFields.POSITION_IN_ALBUM: position_in_album}
        response = self._post_lib_track_with_generic_sample_no_tags(**data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == position_in_album

    def test_max_then_ok(self):
        position_in_album = settings.LIB_TRACK_POSITION_IN_ALBUM_MAX

        data_dict = {PostFields.POSITION_IN_ALBUM: position_in_album}
        response = self._post_lib_track_with_generic_sample_no_tags(**data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == position_in_album

    def test_max_plus_one_then_error(self):
        position_in_album = settings.LIB_TRACK_POSITION_IN_ALBUM_MAX + 1

        data_dict = {PostFields.POSITION_IN_ALBUM: position_in_album}
        response = self._post_lib_track_with_generic_sample_no_tags(**data_dict)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_negative_one_then_error(self):
        position_in_album = -1

        data_dict = {PostFields.POSITION_IN_ALBUM: position_in_album}
        response = self._post_lib_track_with_generic_sample_no_tags(**data_dict)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_integer_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.POSITION_IN_ALBUM: 5.5})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
