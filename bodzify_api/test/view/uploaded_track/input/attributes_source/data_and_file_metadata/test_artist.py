from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_artist_in_both_then_take_data(self):
        data_artist_name = "Queen"
        data_dict = {PostFields.ARTISTS_NAMES_MULTIPART: [data_artist_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        artists = self.saved_object.artists.all()
        artist = artists.first()
        assert artist
        assert artist.name == data_artist_name
