#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingMp3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/rating/sample/mp3/"
    

    """
    The uploaded mp3 track entitled "Gola1" has a 1 star rating. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingMp31Star(self):
        self.login(self.testUser)
        response = self.postSampleTrack("mp3_rating_1_stars.mp3")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola1")
        assert track.rating == 2
    

    """
    The uploaded mp3 track entitled "Gola2" has a 2 stars rating. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingMp32Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("mp3_rating_2_stars.mp3")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola2")
        assert track.rating == 4
    

    """
    The uploaded mp3 track entitled "Gola3" has a 3 stars rating. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingMp33Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("mp3_rating_3_stars.mp3")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola3")
        assert track.rating == 6
    

    """
    The uploaded mp3 track entitled "Gola4" has a 4 stars rating. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingMp34Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("mp3_rating_4_stars.mp3")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola4")
        assert track.rating == 8


    """
    The uploaded mp3 track entitled "Gola" has a 5 stars rating. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingMp35Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("mp3_rating_5_stars.mp3")
        track = LibraryTrack.objects.get(user=self.testUser, title="Gola5")
        assert track.rating == 10


    """
    The uploaded track entitled "GolaNone" hasn't a rating tag. The corresponding value in the database 
    must then be None.
    """
    def test_trackPostRatingMp3NoStar(self):
        self.login(self.testUser)
        response = self.postSampleTrack("mp3_rating_None.mp3")
        track = LibraryTrack.objects.get(user=self.testUser, title="GolaNone")
        assert track.rating == None
