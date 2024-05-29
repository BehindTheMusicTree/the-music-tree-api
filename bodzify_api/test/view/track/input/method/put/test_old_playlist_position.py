#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.serializer.track.input.endpoint.put import FIELDS as PUT_FIELDS


class TestCase(TrackTestCase):

    def test_new_criteria_then_decrease_positions_of_following_tracks_in_old_criteria(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        lib_track_following2 = self.model_fixture_factory.create_lib_track(title="Lodwdw", genre=old_genre)
        lib_track_following1 = self.model_fixture_factory.create_lib_track(title="cdss", genre=old_genre)
        lib_track = self.model_fixture_factory.create_lib_track(title="Love", genre=old_genre)
        data = {PUT_FIELDS.GENRE_NAME: "Rock"}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        old_genre_playlist = CriteriaPlaylist.objects.get(criteria=old_genre).base_playlist
        assert PlaylistLibTrackRelation.objects.get(playlist=old_genre_playlist,
                                                    library_track=lib_track_following1).position == 1
        assert PlaylistLibTrackRelation.objects.get(playlist=old_genre_playlist,
                                                    library_track=lib_track_following2).position == 2
