#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingWav(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/rating/sample/wav/"
    

    """
    The uploaded wav track entitled "Gola1" has a 1 star rating. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingWav1Star(self):
        self.login(self.testUser)
        response = self.postSampleTrack("wav_rating_1_stars.wav")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola1")
        assert track.rating == 2
    

    """
    The uploaded wav track entitled "Gola2" has a 2 stars rating. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingWav2Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("wav_rating_2_stars.wav")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola2")
        assert track.rating == 4
    

    """
    The uploaded wav track entitled "Gola3" has a 3 stars rating. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingWav3Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("wav_rating_3_stars.wav")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola3")
        assert track.rating == 6
    

    """
    The uploaded wav track entitled "Gola4" has a 4 stars rating. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingWav4Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("wav_rating_4_stars.wav")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola4")
        assert track.rating == 8


    """
    The uploaded wav track entitled "Gola" has a 5 stars rating. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingWav5Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("wav_rating_5_stars.wav")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola5")
        assert track.rating == 10


    """
    The uploaded track entitled "GolaNone" hasn't a rating tag. The corresponding value in the database 
    must then be None.
    """
    def test_trackPostRatingWavNoStar(self):
        self.login(self.testUser)
        response = self.postSampleTrack("wav_rating_None.wav")
        track = LibraryTrack.objects.get(user=self.testUser, title="GolaNone")
        assert track.rating == None
