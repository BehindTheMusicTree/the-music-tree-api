#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.File import File
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.album.AlbumViewTestCase import AlbumViewTestCase


class TestCase(AlbumViewTestCase):

    """
    The album "Black Holes And Revelation" has two tracks "Assassin" and "Starlight" (with
    respective filenames "Assassin.mp3" and "Starlight.mp3").
    The deletion of the album must delete the two tracks linked.
    """

    def test_2_tracks_linked(self):
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations")
        assassin_track_filename = "Assassin.mp3"
        file_obj1 = self.create_file(file=str(self.self.lib_abs_path / assassin_track_filename))
        assassin_track = self.model_fixture_factory.create_lib_track(
            file_obj=file_obj1, title="Assassin", album=black_holes_album)
        starlight_track_filename = "Starlight.mp3"
        file_obj2 = self.create_file(file=str(self.self.lib_abs_path / starlight_track_filename))
        starlight_track = self.model_fixture_factory.create_lib_track(
            file_obj=file_obj2, title="Starlight", album=black_holes_album)
        assert self.test_user.does_track_filename_exist_in_lib(assassin_track_filename) == True
        assert self.test_user.does_track_filename_exist_in_lib(starlight_track_filename) == True

        response = self.delete(album_uuid=black_holes_album.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(uuid=black_holes_album.uuid).exists() == False
        assert LibraryTrack.objects.filter(title=assassin_track.title).exists() == False
        assert LibraryTrack.objects.filter(title=starlight_track.title).exists() == False
        assert self.test_user.does_track_filename_exist_in_lib(assassin_track_filename) == False
        assert self.test_user.does_track_filename_exist_in_lib(starlight_track_filename) == False

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
        matthew_artist = self.model_fixture_factory.create_artist(name="Matthew Bellamy")
        muse_artist = self.model_fixture_factory.create_artist(name="Muse")
        pol_artist = self.model_fixture_factory.create_artist(name="Pol")
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations",
                                                                    album_artists=[matthew_artist, muse_artist])
        self.model_fixture_factory.create_lib_track(title="Assassin", artist=matthew_artist, album=black_holes_album)
        self.model_fixture_factory.create_lib_track(title="Blue", artist=pol_artist)

        response = self.delete(album_uuid=black_holes_album.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(name=matthew_artist.name).exists() == False
        assert Artist.objects.filter(name=muse_artist.name).exists() == False
        assert Artist.objects.filter(name=pol_artist.name).exists() == True
