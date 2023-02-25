#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingMp3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/RatingMp3/"

    """
    The uploaded wav track entitled "Gola" has the maximum rating of 5 stars. The corresponding 
    value in the database must then be 10.
    """
    def test_libraryTrackPostRatingMp3Max(self):
        self.login(self.testUser)
        response = self.postSampleTrack("mp3_rating_5_stars.mp3")

        track = LibraryTrack.objects.get(user=self.testUser, title="Gola")
        
        assert track.rating == 10

    """
    The uploaded track entitled "Abs" hasn't a rating tag. The corresponding value in the database 
    must then be None.
    """
    def test_libraryTrackPostRatingMp3None(self):
        self.login(self.testUser)
        response = self.postSampleTrack("mp3_rating_None.mp3")

        track = LibraryTrack.objects.get(user=self.testUser, title="Abs")
        
        assert track.rating == None

    """
    The uploaded track entitled "Hey Jude" has a rating of 2 stars (over 5). The corresponding 
    value in the database must then be 4.
    """
    def test_libraryTrackPostRatingMp3With2Stars(self):
        self.login(self.testUser)
        response = self.postSampleTrack("mp3_rating_2_stars.mp3")

        track = LibraryTrack.objects.get(user=self.testUser, title="Hey Jude")
        
        assert track.rating == 4
