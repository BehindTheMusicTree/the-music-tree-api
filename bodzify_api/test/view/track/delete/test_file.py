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

    def test_when_no_file_linked(self):
        track_title = "We"
        track = G(LibraryTrack, user=self.test_user, title=track_title)
        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert LibraryTrack.objects.filter(user=self.test_user, title=track_title).exists() == False
