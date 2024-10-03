#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.BasePlaylist import SpecialNames as PlaylistSpecialNames
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view import playlist
from bodzify_api.test.view.playlist.children import genre
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_new_genre_then_first_position(self):
        genre_name = "Rock"
        data = {PostFields.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        genre_playlist = CriteriaPlaylist.objects.get(criteria__name=genre_name).base_playlist
        assert PlaylistLibTrackRelation.objects.get(base_playlist=genre_playlist,
                                                    library_track=self.lib_track_saved).position == 1

    def test_existing_genre_then_first_position_and_other_tracks_after(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        lib_track1 = self.model_fixture_factory.create_lib_track(title="We're All To Blame", genre=genre)
        lib_track2 = self.model_fixture_factory.create_lib_track(title="We're All To Blame", genre=genre)
        data = {PostFields.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        genre_playlist = CriteriaPlaylist.objects.get(criteria__name=genre_name).base_playlist
        assert PlaylistLibTrackRelation.objects.get(base_playlist=genre_playlist,
                                                    library_track=self.lib_track_saved).position == 1
        assert PlaylistLibTrackRelation.objects.get(
            base_playlist=genre_playlist, library_track=lib_track1).position == 3
        assert PlaylistLibTrackRelation.objects.get(
            base_playlist=genre_playlist, library_track=lib_track2).position == 2
