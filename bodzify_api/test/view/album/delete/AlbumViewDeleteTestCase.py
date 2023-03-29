#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.Artist import Artist
from bodzify_api.test.view.album.AlbumViewTestCase import AlbumViewTestCase
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class AlbumViewDeleteTestCase(AlbumViewTestCase):

    sampleDirectoryRelativePath = "test/view/album/delete/sample/1/"

    """
		The album "Black Holes And Revelation" has two tracks "Assassin" and "Starlight" (with 
		respective filenames "Assassin.mp3" and "Starlight.mp3").
		The deletion of the album must delete the two tracks with their files.
	"""

    def test_2TracksLinked(self):
        blackHolesAlbum = G(Album, user=self.testUser, name="Black Holes And Revelations")
        assassinTrack = G(
            LibraryTrack,
            user=self.testUser,
            file=self.testUserLibraryAbsolutePath + "Assassin.mp3",
            title="Assassin",
            album=blackHolesAlbum,
            genre=self.testUserGenrelessGenre,
            duration=0)
        starlightTrack = G(
            LibraryTrack,
            user=self.testUser,
            file=self.testUserLibraryAbsolutePath + "Starlight.mp3",
            title="Starlight",
            album=blackHolesAlbum,
            genre=self.testUserGenrelessGenre,
            duration=0)

        response = self._loginAndDelete(albumUuid=blackHolesAlbum.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(uuid=blackHolesAlbum.uuid).exists() == False
        assert LibraryTrack.objects.filter(
            user=self.testUser, title=assassinTrack.title).exists() == False
        assert LibraryTrack.objects.filter(
            user=self.testUser, title=starlightTrack.title).exists() == False
        assert self._doesUserTrackFileExist(assassinTrack.file.name) == False
        assert self._doesUserTrackFileExist(starlightTrack.file.name) == False

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
        matthewArtist = G(Artist, user=self.testUser, name="Matthew Bellamy")
        museArtist = G(Artist, user=self.testUser, name="Muse")
        polArtist = G(Artist, user=self.testUser, name="Pol")
        blackHolesAlbum = G(
            Album,
            user=self.testUser,
            name="Black Holes And Revelations",
            albumArtists=[matthewArtist, museArtist]
        )
        assassinTrack = G(
            LibraryTrack,
            user=self.testUser,
            title="Assassin",
            artist=matthewArtist,
            album=blackHolesAlbum,
            genre=self.testUserGenrelessGenre,
            duration=0
        )
        blueTrack = G(
            LibraryTrack,
            user=self.testUser,
            title="Blue",
            artist=polArtist,
            genre=self.testUserGenrelessGenre,
            duration=0
        )

        response = self._loginAndDelete(albumUuid=blackHolesAlbum.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(user=self.testUser, name=matthewArtist.name).exists() == False
        assert Artist.objects.filter(user=self.testUser, name=museArtist.name).exists() == False
        assert Artist.objects.filter(user=self.testUser, name=polArtist.name).exists() == True
