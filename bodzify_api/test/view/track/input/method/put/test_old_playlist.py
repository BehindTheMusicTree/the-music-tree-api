#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_new_criteria_then_not_in_old_criteria_playlist_anymore(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        new_genre_name = "Rock"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", genre=old_genre)
        data = {PutFields.GENRE_NAME: new_genre_name}
        response = self._put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        old_genre_playlist = CriteriaPlaylist.objects.get(criteria=old_genre).base_playlist
        assert lib_track not in old_genre_playlist.library_tracks.all()
