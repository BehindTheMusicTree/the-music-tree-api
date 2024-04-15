#!/usr/bin/env python

import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

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
