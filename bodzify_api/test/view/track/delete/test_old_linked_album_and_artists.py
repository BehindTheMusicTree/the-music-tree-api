#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_linked_album_then_delete_it_as_nothing_linked_to_it_anymore(self):
        album_name = "Chuck"
        album = self.model_fixture_factory.create_album(name=album_name)
        track = self.model_fixture_factory.create_lib_track_with_file(title="We're All To Blame", album=album)
        response = self._delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Album.objects.filter(user=self.test_user1, name=album_name).exists()

    def test_linked_album_with_another_artist_then_delete_other_artist_as_nothing_linked_to_it_anymore(self):
        green_artist = self.model_fixture_factory.create_artist(name="Green")
        album = self.model_fixture_factory.create_album(name="Chuck", album_artists=[green_artist])
        track = self.model_fixture_factory.create_lib_track_with_file(title="We're All To Blame", album=album)
        response = self._delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Artist.objects.filter(user=self.test_user1, name=green_artist.name).exists()

    def test_linked_artist_then_delete_it_as_nothing_linked_to_it_anymore(self):
        artist_name = "Sum 41"
        artist = self.model_fixture_factory.create_artist(name=artist_name)
        track = self.model_fixture_factory.create_lib_track_with_file(title="We're All To Blame", artists=[artist])
        response = self._delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Artist.objects.filter(user=self.test_user1, name=artist_name).exists()
