#!/usr/bin/env python

import logging
from ddf import G
from rest_framework import status

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.File import File
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
        black_holes_album = G(Album, user=self.test_user, name="Black Holes And Revelations")
        assassin_track_filename = "Assassin.mp3"
        file_obj1 = G(File,
                      user=self.test_user,
                      file=str(self.test_user_lib_abs_path / assassin_track_filename),
                      size_in_ko=None,
                      size_in_mo=None)
        assassin_track = G(LibraryTrack,
                           user=self.test_user,
                           file_obj=file_obj1,
                           title="Assassin",
                           album=black_holes_album)
        starlight_track_filename = "Starlight.mp3"
        file_obj2 = G(File,
                      user=self.test_user,
                      file=str(self.test_user_lib_abs_path / starlight_track_filename),
                      size_in_ko=None,
                      size_in_mo=None)
        starlight_track = G(LibraryTrack,
                            user=self.test_user,
                            file_obj=file_obj2,
                            title="Starlight",
                            album=black_holes_album)
        assert self._does_track_filename_exist_in_test_user_lib(assassin_track_filename) == True
        assert self._does_track_filename_exist_in_test_user_lib(starlight_track_filename) == True

        response = self.delete(album_uuid=black_holes_album.uuid)  # type: ignore

        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert Album.objects.filter(uuid=black_holes_album.uuid).exists() == False
        assert LibraryTrack.objects.filter(
            user=self.test_user, title=assassin_track.title).exists() == False  # type: ignore
        assert LibraryTrack.objects.filter(
            user=self.test_user, title=starlight_track.title).exists() == False  # type: ignore
        assert self._does_track_filename_exist_in_test_user_lib(assassin_track_filename) == False
        assert self._does_track_filename_exist_in_test_user_lib(starlight_track_filename) == False

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
        black_holes_album = G(Album,
                              user=self.test_user,
                              name="Black Holes And Revelations",
                              album_artists=[matthew_artist, muse_artist])
        G(LibraryTrack, user=self.test_user, title="Assassin", artist=matthew_artist, album=black_holes_album)
        G(LibraryTrack, user=self.test_user, title="Blue", artist=pol_artist)

        response = self.delete(album_uuid=black_holes_album.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert Album.objects.filter(user=self.test_user, name=matthew_artist.name).exists() == False  # type: ignore
        assert Artist.objects.filter(user=self.test_user, name=muse_artist.name).exists() == False  # type: ignore
        assert Artist.objects.filter(user=self.test_user, name=pol_artist.name).exists() == True  # type: ignore
