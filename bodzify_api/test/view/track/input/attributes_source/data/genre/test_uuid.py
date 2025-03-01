from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.ForeignKeyBodyDataTestCase import ForeignKeyBodyDataTestCase
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, ForeignKeyBodyDataTestCase):

    def test_non_existing_then_400(self):
        data = {PostFields.GENRE: '8adfc3f9-18f6-4f06-b3cb-e16d5032121w' * settings.UUID_LEN}
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_value_then_ok(self):
        genre_name = "Rock"
        genre_uuid = self.model_fixture_factory.create_genre(name=genre_name).uuid

        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name

    def test_empty_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.GENRE: ''})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None
