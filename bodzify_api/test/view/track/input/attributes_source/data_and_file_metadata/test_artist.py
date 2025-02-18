from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_artist_in_both_then_take_data(self):
        data_artist_name = "Rock"
        data_dict = {PostFields.ARTISTS_NAMES: data_artist_name}
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(**data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        artists = self.saved_object.artists.all()
        artist = artists.first()
        assert artist
        assert artist.name == data_artist_name
