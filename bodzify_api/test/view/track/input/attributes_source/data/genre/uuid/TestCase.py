from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.model.lib_track.input.post.Fields import     Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, ForeignKeyBodyDataTestCase):
    post_field_key = PostFields.GENRE_NAME

    def test_non_existing_then_error(self):
        data = {PostFields.GENRE_UUID: 'a' * settings.UUID_LEN}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_value_then_ok(self):
        genre_name = "Rock"
        genre_uuid = self.model_fixture_factory.create_genre(name=genre_name).uuid

        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.GENRE_UUID: genre_uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.GENRE_UUID: ''})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None
