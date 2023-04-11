#!/usr/bin/env python
import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackDeleteViewTestCase(ApiViewTestCase):

    def test_fileDeletion(self):
        filename = "sample.mp3"
        filePathRelativeToMediaDir = self.testUserLibraryPathRelativeToMediaDir + filename
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=filePathRelativeToMediaDir,
                  title="We're All To Blame",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        assert self.doesTrackFilenameExistInTestUserLibrary(filename) == True
        assert track.fileExists == True
        response = self.deleteTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(uuid=track.uuid).exists() == False
        assert self.doesTrackFilenameExistInTestUserLibrary(filename) == False

    def test_linkedAlbumAndArtistDeletionAsNothingLinkedToItAnymore(self):
        albumName = "Chuck"
        album = G(Album, user=self.testUser, name=albumName)
        artistName = "Sum 41"
        artist = G(Artist, user=self.testUser, name=artistName)
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="We're All To Blame",
                  artist=artist,
                  album=album,
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        response = self.deleteTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(
            user=self.testUser, name=albumName).exists() == False
        assert Artist.objects.filter(
            user=self.testUser, name=artistName).exists() == False

    def test_whenNoFileLinked(self):
        trackTitle = "We"
        track = G(LibraryTrack,
                  user=self.testUser,
                  title=trackTitle,
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        response = self.deleteTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(
            user=self.testUser, title=trackTitle).exists() == False
