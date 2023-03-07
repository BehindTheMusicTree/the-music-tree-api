#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingKid3Mp3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/rating/kid3/mp3/sample/"

    """
    The uploaded mp3 track has a no rating from Kid3. The corresponding 
    value in the app must then be None.
    """
    def test_trackPostRatingKid3Mp3NoRating(self):
        self.login(self.testUser)
        response = self.postSampleTrack("no rating.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == None

    """
    The uploaded mp3 track has a 1 star rating from Kid3. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingKid3Mp31Star(self):
        self.login(self.testUser)
        response = self.postSampleTrack("1 star.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 2
    

    """
    The uploaded mp3 track has a 2 stars rating set from Kid3. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingKid3Mp32Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("2 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 4
    

    """
    The uploaded mp3 track has a 3 stars rating set from Kid3. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingKid3Mp33Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("3 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 6

    """
    The uploaded mp3 track has a 4 stars rating set from Kid3. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingKid3Mp34Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("4 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 8

    """
    The uploaded mp3 track has a 5 stars rating set from Kid3. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingKid3Mp35Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("5 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 10