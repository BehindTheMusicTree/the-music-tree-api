from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.lib_track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase \
    import NullableUuidFieldFromDataTestCase


class TestCase(NullableUuidFieldFromDataTestCase):
    post_field_key = PostFields.GENRE_NAME

    def test_non_existing_uuid_then_error(self):
        data = {PostFields.GENRE_UUID: 'a' * settings.UUID_LEN}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_value_then_ok(self):
        genre_name = "Rock"
        genre_uuid = self.model_fixture_factory.create_genre(name=genre_name).uuid
        data = {PostFields.GENRE_UUID: genre_uuid}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre
        assert self.saved_lib_track.genre.name == genre_name

    def test_empty_then_none(self):
        data = {PostFields.GENRE_UUID: ''}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre == None
