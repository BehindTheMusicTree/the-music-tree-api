
from rest_framework import status

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.schema.track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase \
    import NullableStrFieldFromDataTestCase


class TestCase(NullableStrFieldFromDataTestCase):
    post_field_key = PostFields.ALBUM_ARTISTS_NAMES

    def test_value_then_ok(self):
        value = 'astititit'
        data = {
            PostFields.ALBUM_NAME: 'albumito',
            PostFields.ALBUM_ARTISTS_NAMES: value
        }
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album
        assert self.saved_lib_track.album.album_artists.all()[0].name == value

    def test_empty_then_none(self):
        data = {
            PostFields.ALBUM_NAME: "albumito",
            PostFields.ALBUM_ARTISTS_NAMES: ""
        }
        response = self._post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album
        assert self.saved_lib_track.album.album_artists.count() == 0
