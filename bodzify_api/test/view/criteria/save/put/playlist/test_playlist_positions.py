#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPutSerializer import FIELDS as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_new_parent_then_update_new_parent_playlist(self):
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        track = G(LibraryTrack, user=self.test_user, genre=punk_genre, title="Rock song")
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)

        data = {PUT_FIELD.PARENT: rock_genre.uuid}  # type: ignore
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist
        assert playlist.library_tracks.first() == track  # type: ignore

    def test_new_parent_not_acendant_of_old_parent_then_remove_criteria_playlist_tracks_from_old_criteria_ascendants_playlist(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=rock_genre)
        track = G(LibraryTrack, user=self.test_user, genre=punk_genre, title="Rock song")

        data = {PUT_FIELD.PARENT: ''}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist
        assert playlist.library_tracks.first() != track  # type: ignore

    def test_new_parent_ascendant_of_old_parent_then_remove_criteria_playlist_tracks_from_playlists_of_criterias_in_between(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        track = G(LibraryTrack, user=self.test_user, genre=punk_genre, title="Rock song")

        data = {PUT_FIELD.PARENT: rock_genre.uuid}  # type: ignore
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist
        assert playlist.library_tracks.first() == track  # type: ignore
