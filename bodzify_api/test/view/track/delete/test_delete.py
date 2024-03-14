#!/usr/bin/env python

import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


@pytest.mark.django_db
class TrackDeleteViewTestCase(ApiViewTestCase):

    def test_file_deletion(self):
        filename = "sample.mp3"
        file_path_relative_to_media_dir = self.test_user_lib_path_relative_to_media_dir / filename
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(file_path_relative_to_media_dir),
                  title="We're All To Blame",
                  duration=0)
        assert self._does_track_filename_exist_in_test_user_lib(filename) == True
        assert track.file_exists == True
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(uuid=track.uuid).exists() == False
        assert self._does_track_filename_exist_in_test_user_lib(filename) == False

    def test_linked_album_and_artist_deletion_as_nothing_linked_to_it_anymore(self):
        album_name = "Chuck"
        album = G(Album, user=self.test_user, name=album_name)
        artist_name = "Sum 41"
        artist = G(Artist, user=self.test_user, name=artist_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="We're All To Blame",
                  artist=artist,
                  album=album,
                  duration=0)
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(user=self.test_user, name=album_name).exists() == False
        assert Artist.objects.filter(user=self.test_user, name=artist_name).exists() == False

    def test_when_no_file_linked(self):
        track_title = "We"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title=track_title,
                  duration=0)
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(
            user=self.test_user, title=track_title).exists() == False

    def test_removal_from_the_all_playlist(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="We're All To Blame",
                  duration=0)
        all_playlist = SimplePlaylist.objects.get(
            playlist__user=self.test_user,
            name=PLAYLIST_SPECIAL_NAMES.ALL).playlist
        assert track in all_playlist.library_tracks.all()
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert track not in all_playlist.library_tracks.all()

    def test_removal_from_the_genre_playlists(self):
        rock_genre_name = "Rock"
        hardrock_genre_name = "Hard rock"
        emo_genre_name = "Emo"

        data_dict = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: rock_genre_name
        }
        self.post_genre(data_dict)
        rock_genre = self.saved_genre
        rock_playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist

        data_dict = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: hardrock_genre_name,
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock_genre.uuid
        }
        self.post_genre(data_dict)
        hardrock_genre = self.saved_genre
        hardrock_playlist = CriteriaPlaylist.objects.get(criteria=hardrock_genre).playlist

        data_dict = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: emo_genre_name,
            CRITERIA_ATTRIBUTES_LABEL.PARENT: hardrock_genre.uuid
        }
        self.post_genre(data_dict)
        emo_genre = self.saved_genre
        emo_playlist = CriteriaPlaylist.objects.get(criteria=emo_genre).playlist

        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0,
                  genre=emo_genre)

        assert track in emo_playlist.library_tracks.all()
        assert track in hardrock_playlist.library_tracks.all()
        assert track in rock_playlist.library_tracks.all()

        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert track not in emo_playlist.library_tracks.all()
        assert track not in hardrock_playlist.library_tracks.all()
        assert track not in rock_playlist.library_tracks.all()
