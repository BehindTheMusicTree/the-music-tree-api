#!/usr/bin/env python

from ddf import G
from rest_framework import status
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.serializer.track.input.endpoint.LibTrackPutSerializer import FIELDS as PUT_FIELDS


class TestCase(TrackTestCase):

    def test_new_criteria_then_decrease_positions_of_following_tracks_in_old_criteria(self):
        old_genre = G(Criteria, name="Metal", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        lib_track_following2 = G(LibraryTrack, user=self.test_user, title="Lodwdw", genre=old_genre)
        lib_track_following1 = G(LibraryTrack, user=self.test_user, title="cdss", genre=old_genre)
        lib_track = G(LibraryTrack, user=self.test_user, title="Love", genre=old_genre)
        data = {PUT_FIELDS.GENRE_NAME: "Rock"}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore

        old_genre_playlist = CriteriaPlaylist.objects.get(criteria=old_genre).playlist
        assert PlaylistLibTrackRelation.objects.get(playlist=old_genre_playlist,
                                                    library_track=lib_track_following1).position == 1
        assert PlaylistLibTrackRelation.objects.get(playlist=old_genre_playlist,
                                                    library_track=lib_track_following2).position == 2
