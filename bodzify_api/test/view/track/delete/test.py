#!/usr/bin/env python
import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


@pytest.mark.django_db
class TrackDeleteViewTestCase(ApiViewTestCase):

    def test_fileDeletion(self):
        filename = "sample.mp3"
        filePathRelativeToMediaDir = self.testUserLibraryPathRelativeToMediaDir + filename
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=filePathRelativeToMediaDir,
                  title="We're All To Blame",
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
                  duration=0)
        response = self.deleteTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(
            user=self.testUser, title=trackTitle).exists() == False
        
    def test_removalFromTheAllPlaylist(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="We're All To Blame",
                  duration=0)
        allPlaylist = SimplePlaylist.objects.get(user=self.testUser, name=PLAYLIST_SPECIAL_NAMES.ALL)
        assert track in allPlaylist.librarytrack_set.all()
        response = self.deleteTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert track not in allPlaylist.librarytrack_set.all()
        
    def test_removalFromTheGenrePlaylists(self):        
        rockGenreName = "Rock"
        hardrockGenreName = "Hard rock"
        emoGenreName = "Emo"

        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: rockGenreName
        }
        self.postGenre(dataJson)
        rockGenre = self.savedGenre
        rockPlaylist = CriteriaPlaylist.objects.get(
            user=self.testUser, type=CriteriaTypesId.GENRE, criteria=rockGenre)

        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: hardrockGenreName,
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rockGenre.uuid
        }
        self.postGenre(dataJson)
        hardrockGenre = self.savedGenre
        hardrockPlaylist = CriteriaPlaylist.objects.get(
            user=self.testUser, type=CriteriaTypesId.GENRE, criteria=hardrockGenre)

        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: emoGenreName,
            CRITERIA_ATTRIBUTES_LABEL.PARENT: hardrockGenre.uuid
        }
        self.postGenre(dataJson)
        emoGenre = self.savedGenre
        emoPlaylist = CriteriaPlaylist.objects.get(
            user=self.testUser, type=CriteriaTypesId.GENRE, criteria=emoGenre)

        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  duration=0,
                  genre=emoGenre)
        
        assert track in emoPlaylist.librarytrack_set.all()
        assert track in hardrockPlaylist.librarytrack_set.all()
        assert track in rockPlaylist.librarytrack_set.all()
        
        response = self.deleteTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        assert track not in emoPlaylist.librarytrack_set.all()
        assert track not in hardrockPlaylist.librarytrack_set.all()
        assert track not in rockPlaylist.librarytrack_set.all()
        
        
