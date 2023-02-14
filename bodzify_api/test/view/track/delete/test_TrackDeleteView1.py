#!/usr/bin/env python
import os
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class TrackDeleteViewTestCase1(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackDeleteData1']

    def setUp(self) -> None:
        obj= super().setUp("test/view/track/delete/sample1/")
        self.copySamplesToTestUserLibraryIfNecessary()
        return obj

    def test_libraryTrackDelete1(self):
        self.login(self.testUser)

        """
        Deleting the track '1-03 - We're All To Blame' must delete the associated file 
        'delete_1-03 - We're All To Blame.mp3'.
        """
        response = self.deleteTrack(trackUuid="36nS4LVDssLh4BvTARbJEK")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(title="1-03 - We're All To Blame").exists() == False
        assert os.path.isfile(
                self.testUserLibraryAbsolutePath + "delete_1-03 - We're All To Blame.mp3") == False
