#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames


@pytest.mark.django_db
class TrackPostViewTestCase4(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPostData4']
    sampleDirectoryRelativePath = "test/view/track/post/sample/4/"

    """
    - Without genre.
    - With two album artists "Eminem" and "Dad" with "Eminem already existing.
    - One album artist existing.
    - No artist.
    """
    def test_libraryTrackPost4(self):
        self.login(self.testUser)

        response = self.postSampleTrack("Eminem_Without_Me_sans_genre.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(user=self.testUser, title="Without Me")
        assert track.artist_id is None
        assert track.album.name == "The Eminem Show (Expanded Edition)"
        assert track.genre.name == "Genreless"
        assert track.fileExtension == ".mp3"
        assert track.playlists.filter(
                user=self.testUser, criteria__name=CriteriaSpecialNames.GENRE_GENRELESS).exists()
        assert track.playlists.filter(
                user=self.testUser, criteria__name=CriteriaSpecialNames.GENRE_ALL).exists()
        assert track.album.albumArtists.filter(user=self.testUser, name="Eminem").exists()
        assert track.album.albumArtists.filter(user=self.testUser, name="Dad").exists()
