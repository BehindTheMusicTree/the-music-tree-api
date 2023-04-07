#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingWmpMp3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/rating/wmp/mp3/sample/"

    """
    The uploaded mp3 track has a no rating from Windows Media Player. The corresponding 
    value in the app must then be None.
    """
    def test_trackPostRatingWmpMp3NoRating(self):
        self._login(self.testUser)
        self.postSampleTrack("no rating.mp3")
        assert self.savedTrack.rating == None

    """
    The uploaded mp3 track has a 1 star rating from Windows Media Player. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingWmpMp31Star(self):
        self._login(self.testUser)
        self.postSampleTrack("1 star.mp3")
        assert self.savedTrack.rating == 2
    

    """
    The uploaded mp3 track has a 2 stars rating set from Windows Media Player. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingWmpMp32Stars(self):
        self._login(self.testUser)
        self.postSampleTrack("2 stars.mp3")
        assert self.savedTrack.rating == 4
    

    """
    The uploaded mp3 track has a 3 stars rating set from Windows Media Player. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingWmpMp33Stars(self):
        self._login(self.testUser)
        self.postSampleTrack("3 stars.mp3")
        assert self.savedTrack.rating == 6

    """
    The uploaded mp3 track has a 4 stars rating set from Windows Media Player. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingWmpMp34Stars(self):
        self._login(self.testUser)
        self.postSampleTrack("4 stars.mp3")
        assert self.savedTrack.rating == 8

    """
    The uploaded mp3 track has a 5 stars rating set from Windows Media Player. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingWmpMp35Stars(self):
        self._login(self.testUser)
        self.postSampleTrack("5 stars.mp3")
        assert self.savedTrack.rating == 10