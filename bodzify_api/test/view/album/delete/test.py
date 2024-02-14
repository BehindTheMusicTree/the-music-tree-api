#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.Artist import Artist
from bodzify_api.test.view.album.AlbumViewTestCase import AlbumViewTestCase
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class TestCase(AlbumViewTestCase):

    """
		The album "Black Holes And Revelation" has two tracks "Assassin" and "Starlight" (with 
		respective filenames "Assassin.mp3" and "Starlight.mp3").
		The deletion of the album must delete the two tracks linked.
	"""

    def test_2TracksLinked(self):
        blackHolesAlbum = G(Album, user=self.test_user, name="Black Holes And Revelations")
        assassinTrackFilename = "Assassin.mp3"
        assassinTrack = G(
            LibraryTrack,
            user=self.test_user,
            file=self.test_user_library_abs_path / assassinTrackFilename,
            title="Assassin",
            album=blackHolesAlbum,
            duration=0)
        starlightTrackFilename = "Starlight.mp3"
        starlightTrack = G(
            LibraryTrack,
            user=self.test_user,
            file=self.test_user_library_abs_path / starlightTrackFilename,
            title="Starlight",
            album=blackHolesAlbum,
            duration=0)
        assert self.doesTrackFilenameExistInTestUserLibrary(assassinTrackFilename) == True
        assert self.doesTrackFilenameExistInTestUserLibrary(starlightTrackFilename) == True

        response = self.delete(albumUuid=blackHolesAlbum.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(uuid=blackHolesAlbum.uuid).exists() == False
        assert LibraryTrack.objects.filter(
            user=self.test_user, title=assassinTrack.title).exists() == False
        assert LibraryTrack.objects.filter(
            user=self.test_user, title=starlightTrack.title).exists() == False
        assert self.doesTrackFilenameExistInTestUserLibrary(assassinTrackFilename) == False
        assert self.doesTrackFilenameExistInTestUserLibrary(starlightTrackFilename) == False

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

    def test_withArtistDeletion(self):
        matthewArtist = G(Artist, user=self.test_user, name="Matthew Bellamy")
        museArtist = G(Artist, user=self.test_user, name="Muse")
        polArtist = G(Artist, user=self.test_user, name="Pol")
        blackHolesAlbum = G(
            Album,
            user=self.test_user,
            name="Black Holes And Revelations",
            album_artists=[matthewArtist, museArtist]
        )
        G(
            LibraryTrack,
            user=self.test_user,
            title="Assassin",
            artist=matthewArtist,
            album=blackHolesAlbum,
            duration=0
        )
        G(
            LibraryTrack,
            user=self.test_user,
            title="Blue",
            artist=polArtist,
            duration=0
        )

        response = self.delete(albumUuid=blackHolesAlbum.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(user=self.test_user, name=matthewArtist.name).exists() == False
        assert Artist.objects.filter(user=self.test_user, name=museArtist.name).exists() == False
        assert Artist.objects.filter(user=self.test_user, name=polArtist.name).exists() == True
