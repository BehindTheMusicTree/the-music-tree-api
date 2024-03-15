#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL, Criteria


class TestCase(ApiTestCase):

    def test_renaming(self):
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        genre_new_name = "Punk"
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genre_new_name
        }
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        playlist = CriteriaPlaylist.objects.get(criteria=rock_genre)
        assert playlist.name == genre_new_name

    def test_new_parent_then_update_new_parent_playlist(self):
        punk_genre = G(Criteria,
                       name="Punk",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        track = G(LibraryTrack,
                  user=self.test_user,
                  genre=punk_genre,
                  title="Rock song",
                  duration=100)
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock_genre.uuid
        }
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist
        assert playlist.library_tracks.first() == track

    def test_new_parent_not_acendant_of_old_parent_then_remove_criteria_playlist_tracks_from_old_criteria_ascendants_playlist(self):
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
                       name="Punk",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE,
                       parent=rock_genre)
        track = G(LibraryTrack,
                  user=self.test_user,
                  genre=punk_genre,
                  title="Rock song",
                  duration=100)
        self.post_lib_track_with_specific_sample(data_dict={})

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: ''
        }
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist
        assert playlist.library_tracks.first() != track

    def test_new_parent_ascendant_of_old_parent_then_remove_criteria_playlist_tracks_from_playlists_of_criterias_in_between(self):
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
                       name="Punk",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        track = G(LibraryTrack,
                  user=self.test_user,
                  genre=punk_genre,
                  title="Rock song",
                  duration=100)
        self.post_lib_track_with_specific_sample(data_dict={})

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock_genre.uuid
        }
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist
        assert playlist.library_tracks.first() == track
