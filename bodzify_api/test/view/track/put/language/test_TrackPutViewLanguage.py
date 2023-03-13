#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCaseLanguage(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataLanguage']

    """
    Language isn't specified. It must not be updated.
    """
    def test_trackPutLanguageUnchanged(self):
        data = {
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.language == "Latin"
        

    """
    Updating the language value to "French"
    """
    def test_trackPutLanguageFrench(self):
        data = {
            "language": "French"
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.language == "French"
        

    """
    Language value is empty. The updated value must be None.
    """
    def test_trackPutLanguageNone(self):
        data = {
            "language": None
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.language == None


    """
    The "language" value's length (101) is above the maximum allowed (100). 
    The status code should then be 400 (bad request).
    """
    def test_trackPutLanguageTooLong(self):
        data = {
            "language": "a" * 101,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
