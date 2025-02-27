from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import (
    NullableStrFieldFromDataTestCase
)


class TestCase(NullableStrFieldFromDataTestCase):
    post_field_key = PostFields.GENRE_NAME

    def test_value_then_ok(self):
        value = 'rovk'
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.GENRE_NAME: value})
        assert response.status_code == status.HTTP_201_CREATED
        genre = self.saved_object.genre
        assert genre
        assert genre.name == value

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_1_star(**{PostFields.GENRE_NAME: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None
