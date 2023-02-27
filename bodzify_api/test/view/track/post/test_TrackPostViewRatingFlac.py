#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingFlac(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/RatingFlac/"

    """
    The uploaded track entitled "Jobi" has 5 stars (the maximum rating, 100 out of 100 in a Flac 
    file). The corresponding value in the application must then be 10.
    """
    def test_libraryTrackPostRatingFlacMax(self):
        self.login(self.testUser)
        response = self.postSampleTrack("flac_rating_5_stars.flac")

        track = LibraryTrack.objects.get(user=self.testUser, title="Jobi")
        
        assert track.rating == 10

    """
    The uploaded track entitled "Lola" hasn't a rating tag. The corresponding value in the application 
    must then be None.
    """
    def test_libraryTrackPostRatingFlacNone(self):
        self.login(self.testUser)
        response = self.postSampleTrack("flac_rating_None.flac")

        track = LibraryTrack.objects.get(user=self.testUser, title="Lola")
        
        assert track.rating == None

    """
    The uploaded track entitled "The Foule" has a rating of 3 stars (60 over 100 for Vorbis tag 
    files like FLAC). The corresponding value in the application must then be 6 (out of 10).
    """
    def test_libraryTrackPostRatingFlac60(self):
        self.login(self.testUser)
        response = self.postSampleTrack("flac_rating_3_stars.flac")

        track = LibraryTrack.objects.get(user=self.testUser, title="The Foule")
        
        assert track.rating == 6
