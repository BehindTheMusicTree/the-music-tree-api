#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.criteria.input.schema.endpoint.put import Fields as PutFields
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_renaming(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        genre_new_name = "Punk"
        data = {PutFields.NAME: genre_new_name}
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        playlist = self.saved_genre
        assert playlist.name == genre_new_name

    def test_new_parent_then_update_playlist_parent(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        hardcore_genre = self.model_fixture_factory.create_genre(name="Hardcore")
        data = {PutFields.PARENT: hardcore_genre.uuid}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        punk_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=punk_genre)
        hardcore_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=hardcore_genre)
        assert punk_playlist.parent == hardcore_playlist

    def test_new_root_then_update_playlist_root(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        hardcore_genre = self.model_fixture_factory.create_genre(name="Hardcore")
        data = {PutFields.PARENT: hardcore_genre.uuid}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        punk_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=punk_genre)
        hardcore_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=hardcore_genre)
        assert punk_playlist.root == hardcore_playlist

    def test_new_parent_then_update_new_parent_playlist(self):
        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        track = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre, title="Rock song")
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")

        data = {PutFields.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=rock_genre).base_playlist
        assert playlist.library_tracks.first() == track

    def test_new_parent_not_acendant_of_old_parent_then_remove_criteria_playlist_tracks_from_old_criteria_ascendants_playlist(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        track = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre, title="Rock song")

        data = {PutFields.PARENT: ''}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=rock_genre).base_playlist
        assert playlist.library_tracks.first() != track

    def test_new_parent_undirect_ascendant_of_old_parent_then_update_positions_in_criterias_in_between(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punk_playlist: CriteriaPlaylist = punk_genre.criteria_playlist
        punk_fr_genre = self.model_fixture_factory.create_genre(name="Punk FR", parent=punk_genre)

        track_punk = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre, title="Punk song")
        self.model_fixture_factory.create_lib_track_with_file(genre=punk_fr_genre, title="punk fr song")

        data = {PutFields.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=punk_fr_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert punk_playlist.library_tracks.count() == 1
        assert punk_playlist.library_tracks.first() == track_punk
