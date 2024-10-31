
from rest_framework import status

from bodzify_api.serializer.schema.track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.playlist.children import genre
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import \
    NullableStrFieldFromDataTestCase


class TestCase(NullableStrFieldFromDataTestCase):
    post_field_key = PostFields.GENRE_NAME

    def test_value_then_ok(self):
        value = 'rovk'
        data = {PostFields.GENRE_NAME: value}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        genre = self.saved_lib_track.genre
        assert genre
        assert genre.name == value

    def test_empty_then_none(self):
        data = {PostFields.GENRE_NAME: ""}
        response = self._post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre == None
