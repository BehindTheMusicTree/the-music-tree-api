#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria, CriteriaSpecialNames


@pytest.mark.django_db
class TrackPostViewTestCaseGenre(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/GenreNonExisting/"

    """
    Genre 'foo' non existing. The track must be in two playlists: the one linked
    with the "All" genre and the one linked with the "French cloud rap" genre. 
    """
    def test_libraryTrackPostGenreNonExisting(self):
        self.login(self.testUser)
        response = self.postSampleTrack("genre_non_existing.mp3")
        track = LibraryTrack.objects.get(user=self.testUser, title="Luz De Luna")
        assert response.status_code == status.HTTP_201_CREATED
        assert Criteria.objects.filter(user=self.testUser, name="Foo").exists()
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
