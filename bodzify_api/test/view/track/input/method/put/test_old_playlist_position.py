#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    CriteriaPlaylist
from bodzify_api.serializer.schema.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_new_criteria_then_decrease_positions_of_following_tracks_in_old_criteria(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        lib_track_following2 = self.model_fixture_factory.create_lib_track_with_file(title="Lodwdw", genre=old_genre)
        lib_track_following1 = self.model_fixture_factory.create_lib_track_with_file(title="cdss", genre=old_genre)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", genre=old_genre)
        data = {PutFields.GENRE_NAME: "Rock"}
        response = self._put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        old_genre_playlist = CriteriaPlaylist.objects.get(criteria=old_genre).base_playlist
        assert LibTrackPlaylistPositionRel.objects.get(base_playlist=old_genre_playlist,
                                                       library_track=lib_track_following1).position == 1
        assert LibTrackPlaylistPositionRel.objects.get(base_playlist=old_genre_playlist,
                                                       library_track=lib_track_following2).position == 2
