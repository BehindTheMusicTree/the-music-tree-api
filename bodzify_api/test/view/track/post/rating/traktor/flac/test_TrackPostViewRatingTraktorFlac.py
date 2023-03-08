#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingTraktorFlac(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/rating/traktor/flac/sample/"

    """
    The uploaded flac track has a no rating from Traktor. The corresponding 
    value in the app must then be None.
    """
    def test_trackPostRatingTraktorFlacNoRating(self):   
        self.login(self.testUser)
        response = self.postSampleTrack("no rating.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == None


    """
    The uploaded flac track has a 1 star rating from Traktor. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingTraktorFlac1Star(self):     
        self.login(self.testUser)
        response = self.postSampleTrack("1 star.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 2
    

    """
    The uploaded flac track has a 2 stars rating set from Traktor. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingTraktorFlac2Stars(self):  
        self.login(self.testUser)
        response = self.postSampleTrack("2 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 4
    

    """
    The uploaded flac track has a 3 stars rating set from Traktor. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingTraktorFlac3Stars(self):  
        self.login(self.testUser)
        response = self.postSampleTrack("3 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 6


    """
    The uploaded flac track has a 4 stars rating set from Traktor. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingTraktorFlac4Stars(self):  
        self.login(self.testUser)
        response = self.postSampleTrack("4 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 8


    """
    The uploaded flac track has a 5 stars rating set from Traktor. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingTraktorFlac5Stars(self):  
        self.login(self.testUser)
        response = self.postSampleTrack("5 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 10
