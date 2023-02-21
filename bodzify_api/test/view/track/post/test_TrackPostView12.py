#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesIds
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCase12(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/12/"

    """
    File entitled "Jobi" has a non existing genre "House". Thus:
     - a new genre "House" must be created with parent genre "All";
     - a new genre playlist linked to the genre "House" must be created;
     - The track created must be linked to the new genre and the new playlist.
    """
    def test_libraryTrackPost12NewGenre(self):
        self.login(self.testUser)
        response = self.postSampleTrack("sample_with_genre_house.flac")

        track = LibraryTrack.objects.get(user=self.testUser, title="Jobi")
        
        assert Criteria.objects.filter(
                user=self.testUser, type=CriteriaTypesIds.GENRE, name="House").exists()
        houseGenre = Criteria.objects.get(
                user=self.testUser, type=CriteriaTypesIds.GENRE, name="House")
        assert houseGenre.parent == Criteria.objects.get(
                user=self.testUser, 
                type=CriteriaTypesIds.GENRE, 
                name=CriteriaSpecialNames.GENRE_ALL)

        assert Playlist.objects.filter(
                user=self.testUser, type=PlaylistTypeIds.GENRE, criteria=houseGenre).exists()
        playlist = Playlist.objects.get(
                user=self.testUser, type=CriteriaTypesIds.GENRE, criteria=houseGenre)
        assert track in list(playlist.librarytrack_set.all())
        assert track.genre == houseGenre 
