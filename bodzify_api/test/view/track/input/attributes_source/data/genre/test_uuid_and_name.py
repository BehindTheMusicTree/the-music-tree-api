
from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.lib_track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_uuid_and_name_fields_null_then_none(self):
        data = {
            PostFields.GENRE_NAME: None,
            PostFields.GENRE_UUID: None,
        }
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre == None

    def test_uuid_and_name_fields_not_both_null_then_error(self):
        data = {
            PostFields.GENRE_NAME: 'd',
            PostFields.GENRE_UUID: 'k' * settings.UUID_LEN,
        }
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
