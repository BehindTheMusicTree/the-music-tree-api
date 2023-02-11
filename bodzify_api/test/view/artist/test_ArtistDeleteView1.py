from rest_framework import status

from bodzify_api.test.view.artist.ArtistViewTestCase import ArtistViewTestCase
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ArtistDeleteViewTestCase1(ArtistViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewArtistDeleteData1']

    def test_artistDelete1(self):
        self.login(self.testUser)

        # Artist with one track
        response = self.delete(artistUuid="Lsji85mqisjdjf885DHD65")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Artist.objects.filter(uuid="Lsji85mqisjdjf885DHD65").exists() == False
        assert LibraryTrack.objects.filter(uuid="36nS4LVDssLh4BvTARbJEK").exists() == False
