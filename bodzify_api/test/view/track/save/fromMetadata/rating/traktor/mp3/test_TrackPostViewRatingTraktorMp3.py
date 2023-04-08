#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingTraktorMp3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/rating/traktor/mp3/sample/"

    """
    The uploaded mp3 track has a no rating from Traktor. The corresponding 
    value in the app must then be None.
    """
    def test_trackPostRatingTraktorMp3NoRating(self):
        self._login(self.testUser)
        response = self.postSampleTrack("no rating.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == None

    """
    The uploaded mp3 track has a 1 star rating from Traktor. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingTraktorMp31Star(self):
        self._login(self.testUser)
        response = self.postSampleTrack("1 star.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 2
    

    """
    The uploaded mp3 track has a 2 stars rating set from Traktor. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingTraktorMp32Stars(self):
        self._login(self.testUser)
        response = self.postSampleTrack("2 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 4
    

    """
    The uploaded mp3 track has a 3 stars rating set from Traktor. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingTraktorMp33Stars(self):
        self._login(self.testUser)
        response = self.postSampleTrack("3 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 6

    """
    The uploaded mp3 track has a 4 stars rating set from Traktor. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingTraktorMp34Stars(self):
        self._login(self.testUser)
        response = self.postSampleTrack("4 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 8

    """
    The uploaded mp3 track has a 5 stars rating set from Traktor. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingTraktorMp35Stars(self):
        self._login(self.testUser)
        response = self.postSampleTrack("5 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 10