#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPutSerializer import FIELDS as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_new_root_then_update_root_of_descendants(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)
        frenchhardcore_genre = self.model_fixture_factory.create_genre(name="French hardcore",
                                                                       parent=punkhardcore_genre)

        data = {PUT_FIELD.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        root_playlist = rock_genre.criteria_playlist  # type: ignore

        updated_punk_genre_playlist = CriteriaPlaylist.objects.get(criteria=punk_genre)
        assert updated_punk_genre_playlist.root == root_playlist

        updated_punkhardcore_genre_playlist = CriteriaPlaylist.objects.get(criteria=punkhardcore_genre)
        assert updated_punkhardcore_genre_playlist.root == root_playlist

        updated_frenchhardcore_genre_playlist = CriteriaPlaylist.objects.get(criteria=frenchhardcore_genre)
        assert updated_frenchhardcore_genre_playlist.root == root_playlist
