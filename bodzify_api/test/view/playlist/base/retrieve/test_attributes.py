from rest_framework import status

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.model.playlist.base.output.detailed import Fields as RetrieveFields
from bodzify_api.test.view.playlist.base.PlaylistTestCase import PlaylistTestCase


class TestCase(PlaylistTestCase):

    def test_retrieve_simple_then_ok(self):
        name = 'cuisine'
        playlist_uuid = self.model_fixture_factory.create_manual_playlist(name=name).uuid

        response = self._retrieve_playlist(uuid=playlist_uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[RetrieveFields.NAME] == name

    def test_retrieve_genre_then_ok(self):
        name = 'rock'
        genre = self.model_fixture_factory.create_genre(name=name)
        playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1,
                                                                  criteria=genre,
                                                                  type=CriteriaTypePks.GENRE)

        response = self._retrieve_playlist(uuid=playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[RetrieveFields.NAME] == name

    def test_retrieve_tag_then_ok(self):
        name = 'foot'
        tag = self.model_fixture_factory.create_tag(name=name)
        playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1,
                                                                  criteria=tag,
                                                                  type=CriteriaTypePks.TAG)

        response = self._retrieve_playlist(uuid=playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[RetrieveFields.NAME] == name
