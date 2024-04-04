#!/usr/bin/env python

import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_file_deletion(self):
        filename = "sample.mp3"
        file_path_relative_to_media_dir = self.test_user_lib_path_relative_to_media_dir / filename
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(file_path_relative_to_media_dir),
                  title="We're All To Blame",
                  duration=0)
        assert self._does_track_filename_exist_in_test_user_lib(filename) == True
        assert track.file_exists  # type: ignore
        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert LibraryTrack.objects.filter(uuid=track.uuid).exists() == False  # type: ignore
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
        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert Album.objects.filter(user=self.test_user, name=album_name).exists() == False
        assert Artist.objects.filter(user=self.test_user, name=artist_name).exists() == False

    def test_when_no_file_linked(self):
        track_title = "We"
        track = G(LibraryTrack, user=self.test_user, title=track_title)
        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert LibraryTrack.objects.filter(user=self.test_user, title=track_title).exists() == False

    def test_removal_from_the_all_playlist(self):
        track = G(LibraryTrack, user=self.test_user, title="We're All To Blame")
        all_playlist = SimplePlaylist.objects.get(playlist__user=self.test_user,
                                                  name=PLAYLIST_SPECIAL_NAMES.ALL).playlist
        assert track in all_playlist.library_tracks.all()  # type: ignore
        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert track not in all_playlist.library_tracks.all()  # type: ignore

    def test_removal_from_the_genre_playlists(self):
        genre1_name = "Rock"
        genre1 = G(Criteria, name=genre1_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        genre2_name = "Hard rock"
        genre2 = G(Criteria, name=genre2_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=genre1)
        genre3_name = "Emo"
        genre3 = G(Criteria,
                   name=genre3_name,
                   user=self.test_user,
                   type=CRITERIA_TYPES_ID.GENRE,
                   parent=genre2)

        track = G(LibraryTrack, user=self.test_user, title="Love", genre=genre3)

        assert track in genre1.criteria_playlist.playlist.library_tracks.all()  # type: ignore
        assert track in genre2.criteria_playlist.playlist.library_tracks.all()  # type: ignore
        assert track in genre3.criteria_playlist.playlist.library_tracks.all()  # type: ignore

        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore

        assert track not in genre1.criteria_playlist.playlist.library_tracks.all()  # type: ignore
        assert track not in genre2.criteria_playlist.playlist.library_tracks.all()  # type: ignore
        assert track not in genre3.criteria_playlist.playlist.library_tracks.all()  # type: ignore

    def test_removal_then_next_tracks_in_playlist_decrease_position(self):
        track1 = G(LibraryTrack, user=self.test_user, title="We're All To Blame")
        track2 = G(LibraryTrack, user=self.test_user, title="Still Waiting")
        track3 = G(LibraryTrack, user=self.test_user, title="The Hell Song")

        playlist = SimplePlaylist.objects.get(playlist__user=self.test_user, name=PLAYLIST_SPECIAL_NAMES.ALL).playlist

        response = self.delete_lib_track(lib_track_uuid=track1.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert PlaylistLibTrackRelation.objects.get(playlist=playlist, library_track=track2).position == 1
        assert PlaylistLibTrackRelation.objects.get(playlist=playlist, library_track=track3).position == 2
