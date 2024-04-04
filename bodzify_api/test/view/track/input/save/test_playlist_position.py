#!/usr/bin/env python

import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from bodzify_api.test.view import playlist
from bodzify_api.test.view.playlist.children import genre
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_new_genre_then_first_position(self):
        genre_name = "Rock"
        data = {POST_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        genre_playlist = CriteriaPlaylist.objects.get(criteria__name=genre_name).playlist
        assert PlaylistLibTrackRelation.objects.get(playlist=genre_playlist,
                                                    library_track=self.saved_lib_track).position == 1

    def test_existing_genre_then_first_position_and_other_tracks_after(self):
        genre_name = "Rock"
        genre = G(Criteria, name=genre_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        lib_track1 = G(LibraryTrack, user=self.test_user, title="We're All To Blame", genre=genre)
        lib_track2 = G(LibraryTrack, user=self.test_user, title="We're All To Blame", genre=genre)
        data = {POST_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        genre_playlist = CriteriaPlaylist.objects.get(criteria__name=genre_name).playlist
        assert PlaylistLibTrackRelation.objects.get(playlist=genre_playlist,
                                                    library_track=self.saved_lib_track).position == 1
        assert PlaylistLibTrackRelation.objects.get(playlist=genre_playlist, library_track=lib_track1).position == 3
        assert PlaylistLibTrackRelation.objects.get(playlist=genre_playlist, library_track=lib_track2).position == 2
