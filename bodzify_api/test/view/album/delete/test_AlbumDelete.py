#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.Artist import Artist
from bodzify_api.test.view.album.AlbumViewTestCase import AlbumViewTestCase
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class AlbumDeleteTestCase1(AlbumViewTestCase):

	fixtures = ['initial_data', 'TestUserData']
	sampleDirectoryRelativePath = "test/view/album/delete/sample/1/"

	"""
	The album "Black Holes And Revelation" has two tracks "Assassin" and "Starlight" (with 
	respective filenames "Assassin.mp3" and "Starlight.mp3").
	The deletion of the album must delete the two tracks with their files.
	"""
	def test_albumDelete2Tracks(self):
		self._login(self.testUser)

		album = G(Album, user=self.testUser, uuid="f36nS4LVDssLh4BvTSST54", name="Black Holes And Revelations")
		track1 = G(
				LibraryTrack, 
				user=self.testUser, 
				file=self.testUserLibraryAbsolutePath + "Assassin.mp3", 
				title="Assassin",
				album=album,
    			genre=)
		track2 = G(
				LibraryTrack, 
				user=self.testUser, 
				file=self.testUserLibraryAbsolutePath + "Starlight.mp3", 
				title="Starlight", 
				album=album)
		
		response = self._loginAndDelete(albumUuid=album.uuid)

		assert response.status_code == status.HTTP_204_NO_CONTENT
		assert Album.objects.filter(uuid="f36nS4LVDssLh4BvTSST54").exists() == False
		assert LibraryTrack.objects.filter(user=self.testUser, title="Assassin").exists() == False
		assert LibraryTrack.objects.filter(user=self.testUser, title="Starlight").exists() == False
		assert self._doesUserTrackFileExist("Assassin.mp3") == False
		assert self._doesUserTrackFileExist("Starlight.mp3") == False


	# """
	# The album "Black Holes And Revelations" has:
	# 	- one track "Assassin" with artist "Matthew Bellamy";
	# 	- two album artists named "Muse" and "Pol".
	# The artist "Pol" has another track linked to it but in another album. 
	# This test checks if the album deletion:
	# 	- triggers the deletion of the artist "Matthew Bellamy" as it was not linked to any album 
	# 	and the only track it was linked to is deleted;
	# 	- triggers the deletion of the artist "Muse" as it was not linked to any track and
	# 	the only album it was linked to is deleted;
	# 	- does not trigger the deletion of the artist "Pol" as it has still a track linked to it.
	# """
	# def test_albumDeleteWithArtistDeletion(self):
	# 	artistMatthew = G(
	# 		Artist,
	# 		user=self.testUser,
	# 		name="Matthew Bellamy"
	# 	)
	# 	artistPol = G(
	# 		Artist,
	# 		user=self.testUser,
	# 		name="Pol"
	# 	)
	# 	albumBlackHoles = G(
	# 		Album,
	# 		uuid="f36nS4LVDssLh4BvTSST54",
	# 		name="Black Holes And Revelations",
	# 		albumArtists=[artistMatthew, artistPol]
	# 	)
	# 	trackAssassin = G(
	# 		LibraryTrack, 
	# 		user=self.testUser, 
	# 		title="Assassin",
	# 		artist=artistMatthew
    # 	)
	# 	trackBlue = G(
	# 		LibraryTrack, 
	# 		user=self.testUser, 
	# 		title="Blue",
	# 		artist=artistPol
    # 	)
  
	# 	response = self._loginAndDelete(albumUuid=albumBlackHoles.uuid)

	# 	assert response.status_code == status.HTTP_204_NO_CONTENT
	# 	assert Album.objects.filter(user=self.testUser, name="Matthew Bellamy").exists() == False
	# 	assert Artist.objects.filter(user=self.testUser, name="Muse").exists() == False
	# 	assert Artist.objects.filter(user=self.testUser, name="Pol").exists() == True
