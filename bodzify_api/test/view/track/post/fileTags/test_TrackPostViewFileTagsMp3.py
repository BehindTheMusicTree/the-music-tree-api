#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseFileTagsMp3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/FileTags/sample/mp3/"

    """
    - Mp3 with all tags;
    - the rating source is MusicBee with 2 starts.
    """
    def test_trackPostFileTagsMp3WithAllTags(self):
        self.login(self.testUser)
        response = self.postSampleTrack("with_all_tags.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(user=self.testUser, title="Partir Un Jour")
        assert track.artist.name == "2Be3"
        assert track.album.name == "Demain"
        assert track.album.albumArtists.filter(user=self.testUser, name="2Be3").exists()
        assert track.album.albumArtists.filter(user=self.testUser, name="Fillip").exists()
        assert track.genre.name == "Boys band eurodance"
        assert track.playlists.filter(user=self.testUser, criteria__name="Boys band eurodance").exists()
        assert track.rating == 4
        assert track.language == "French"
        assert track.fileExtension == ".mp3"

