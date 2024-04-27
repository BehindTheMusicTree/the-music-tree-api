#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_linked_album_and_artist_deletion_as_nothing_linked_to_it_anymore(self):
        album_name = "Chuck"
        album = self.model_fixture_factory.create_album(name=album_name)
        artist_name = "Sum 41"
        artist = self.model_fixture_factory.create_artist(name=artist_name)
        track = self.model_fixture_factory.create_lib_track(title="We're All To Blame",
                                                            artist=artist,
                                                            album=album)
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(name=album_name).exists() == False
        assert Artist.objects.filter(name=artist_name).exists() == False
