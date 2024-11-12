from rest_framework import status

from bodzify_api.serializer.schema.lib_track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_genre_name_in_both_then_take_data(self):
        data_genre_name = "Rock"
        data_dict = {PostFields.GENRE_NAME: data_genre_name}
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(kwargs=data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre
        assert self.saved_lib_track.genre.name == data_genre_name

    def test_genre_uuid_in_data_and_genre_name_in_matadata_then_take_data(self):
        data_genre_name = "Rock"
        genre_uuid = self.model_fixture_factory.create_genre(name=data_genre_name).uuid
        data_dict = {PostFields.GENRE_UUID: genre_uuid}
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(kwargs=data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre
        assert self.saved_lib_track.genre.name == data_genre_name
