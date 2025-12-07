from rest_framework import status

from api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_genre_name_in_both_then_take_data(self):
        data_genre_name = "Rock"
        data_dict = {PostFields.GENRE: data_genre_name}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == data_genre_name

    def test_genre_uuid_in_data_and_genre_name_in_matadata_then_take_data(self):
        data_genre_name = "Rock"
        genre_uuid = self.model_fixture_factory.create_genre(name=data_genre_name).uuid

        data_dict = {PostFields.GENRE: genre_uuid}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == data_genre_name
