#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames


@pytest.mark.django_db
class TrackPostViewTestCase1(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPostData1']
    sampleDirectoryRelativePath = "test/view/track/post/sample/1/"

    """
     - FLAC file;
     - existing artist "PNL";
     - non existing album "Dans La Légende";
     - one non existing Album artist "Triste" and one existing "PNL";
     - with new genre "French cloud rap". Thus the track must be in two playlists: the one linked
     with the "All" genre and the one linked with the "French cloud rap" genre. 
    """
    def test_libraryTrackPost1(self):
        self.login(self.testUser)
        response = self.postSampleTrack("1-08 - Luz De Luna.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(user=self.testUser, title="Luz De Luna")
        assert track.artist.name == "PNL"
        assert track.album.name == "Dans La Légende"
        assert track.album.albumArtists.filter(user=self.testUser, name="PNL").exists()
        assert track.album.albumArtists.filter(user=self.testUser, name="Triste").exists()
        assert track.genre.name == "French cloud rap"
        assert track.fileExtension == ".flac"
        allPlaylist = Playlist.objects.get(
                user=self.testUser, 
                type=PlaylistTypeIds.GENRE, 
                criteria__name=CriteriaSpecialNames.GENRE_ALL)
        franchCloudRapPlaylist = Playlist.objects.get(
                user=self.testUser, 
                type=PlaylistTypeIds.GENRE, 
                criteria__name="French cloud rap")
        assert allPlaylist in list(track.playlists.all())
        assert franchCloudRapPlaylist in list(track.playlists.all())
