#!/usr/bin/env python

import logging
import os

from ddf import G
from rest_framework import status

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.album.AlbumViewTestCase import AlbumViewTestCase

logger = logging.getLogger('bodzify_api')


class TestCase(AlbumViewTestCase):

    """
    The album "Black Holes And Revelation" has two tracks "Assassin" and "Starlight" (with 
    respective filenames "Assassin.mp3" and "Starlight.mp3").
    The deletion of the album must delete the two tracks linked.
    """

    def test_2_tracks_linked(self):
        black_holes_album = G(Album, user=self.test_user,
                              name="Black Holes And Revelations")
        assassin_track_filename = "Assassin.mp3"
        assassin_track = G(
            LibraryTrack,
            user=self.test_user,
            file=str(self.test_user_library_abs_path /
                     assassin_track_filename),
            title="Assassin",
            album=black_holes_album,
            duration=0)
        starlight_track_filename = "Starlight.mp3"
        starlightTrack = G(
            LibraryTrack,
            user=self.test_user,
            file=str(self.test_user_library_abs_path /
                     starlight_track_filename),
            title="Starlight",
            album=black_holes_album,
            duration=0)
        assert self.does_track_filename_exist_in_test_user_library(
            assassin_track_filename) == True
        assert self.does_track_filename_exist_in_test_user_library(
            starlight_track_filename) == True

        response = self.delete(album_uuid=black_holes_album.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(
            uuid=black_holes_album.uuid).exists() == False
        assert LibraryTrack.objects.filter(
            user=self.test_user, title=assassin_track.title).exists() == False
        assert LibraryTrack.objects.filter(
            user=self.test_user, title=starlightTrack.title).exists() == False
        assert self.does_track_filename_exist_in_test_user_library(
            assassin_track_filename) == False
        assert self.does_track_filename_exist_in_test_user_library(
            starlight_track_filename) == False

    """
    The album "Black Holes And Revelations" has:
    	- one track "Assassin" with artist "Matthew Bellamy";
    	- two album artists named "Muse" and "Pol".
    The artist "Pol" has another track "Blue" linked to it but with no album.
    This test checks if the album deletion:
    	- triggers the deletion of the artist "Matthew Bellamy" as it was not linked to any album
    	and the only track it was linked to is deleted;
    	- triggers the deletion of the artist "Muse" as it was not linked to any track and
    	the only album it was linked to is deleted;
    	- does not trigger the deletion of the artist "Pol" as it has still a track linked to it.
    """

    def test_with_artist_deletion(self):
        matthew_artist = G(Artist, user=self.test_user, name="Matthew Bellamy")
        muse_artist = G(Artist, user=self.test_user, name="Muse")
        pol_artist = G(Artist, user=self.test_user, name="Pol")
        black_holes_album = G(
            Album,
            user=self.test_user,
            name="Black Holes And Revelations",
            album_artists=[matthew_artist, muse_artist]
        )
        G(
            LibraryTrack,
            user=self.test_user,
            title="Assassin",
            artist=matthew_artist,
            album=black_holes_album,
            duration=0
        )
        G(
            LibraryTrack,
            user=self.test_user,
            title="Blue",
            artist=pol_artist,
            duration=0
        )

        response = self.delete(album_uuid=black_holes_album.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(
            user=self.test_user, name=matthew_artist.name).exists() == False
        assert Artist.objects.filter(
            user=self.test_user, name=muse_artist.name).exists() == False
        assert Artist.objects.filter(
            user=self.test_user, name=pol_artist.name).exists() == True
