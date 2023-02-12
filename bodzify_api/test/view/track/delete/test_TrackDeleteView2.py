#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class TrackDeleteViewTestCase2(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackDeleteData2']

    def setUp(self) -> None:
        obj= super().setUp("test/view/track/delete/sample2/")
        self.copySamplesToTestUserLibrary()
        return obj

    def test_libraryTrackDelete2(self):
        self.login(self.testUser)

        """
        Deleting the track '1-03 - We're All To Blame' must also delete : 
            - The track's album 'X' must also be deleted as it has no track anymore.
            - The track's artist 'Linkin Park' must also be deleted as it has no associated track 
        or album anymore.
        """
        response = self.deleteTrack(trackUuid="36nS4LVDssLh4BvTARbJEK")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(user=self.testUser, name="X").exists() == False
        assert Artist.objects.filer(user=self.testUser, name="Linkin Park").exists() == False
