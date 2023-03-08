#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackDeleteViewTestCase1(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackDeleteData1']
    sampleDirectoryRelativePath = "test/view/track/delete/sample/1/"


    def test_libraryTrackDelete1(self):
        self.login(self.testUser)

        """
        Deleting the track entitled 'We're All To Blame' must delete the associated file 
        '1-03 - We're All To Blame.mp3'.
        """
        response = self._deleteTrack(trackUuid="36nS4LVDssLh4BvTARbJEK")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(user=self.testUser, title="We're All To Blame").exists() == False
        assert self.doesUserTrackFileExist("1-03 - We're All To Blame.mp3") == False
