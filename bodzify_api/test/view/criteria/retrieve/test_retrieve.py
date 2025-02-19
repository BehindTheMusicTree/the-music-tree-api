from uuid import UUID
from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.output.Fields import Fields as RetrieveFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(GenreTestCase):

    def test_name(self):
        name = 'rock'
        uuid = self.model_fixture_factory.create_genre(name=name).uuid
        response = self._retrieve_genre(uuid=uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[RetrieveFields.NAME] == name

    def test_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name='rock')

        title1 = 'stylax'
        track1_uuid = self.model_fixture_factory.create_lib_track_with_file(
            title=title1, genre=criteria, use_manager_for_genre_playlist_adding=True).uuid

        title2 = 'bien'
        track2_uuid = self.model_fixture_factory.create_lib_track_with_file(
            title=title2, genre=criteria,
            use_manager_for_genre_playlist_adding=True).uuid

        response = self._retrieve_genre(uuid=criteria.uuid)
        assert response.status_code == status.HTTP_200_OK
        lib_tracks = self.result[to_camel_case(RetrieveFields.LIB_TRACKS_NOT_ARCHIVED_PUBLIC)]
        assert len(lib_tracks) == 2
        titles = [track[RetrieveFields.LIB_TRACKS_TITLE] for track in lib_tracks]
        assert title1 in titles
        assert title2 in titles
        uuids = [UUID(track[RetrieveFields.UUID]) for track in lib_tracks]
        assert track1_uuid in uuids
        assert track2_uuid in uuids
