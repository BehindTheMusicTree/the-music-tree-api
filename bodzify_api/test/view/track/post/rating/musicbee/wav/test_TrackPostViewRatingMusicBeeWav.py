#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingMusicBeeWav(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/rating/musicbee/wav/sample/"


    """
    The uploaded wav track has a no rating from MusicBee. The corresponding 
    value in the app must then be None.
    """
    def test_trackPostRatingMusicBeeWavNoRating(self):
        self.login(self.testUser)
        response = self.postSampleTrack("no rating.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == None


    """
    The uploaded wav track has a 0 star rating from MusicBee. The corresponding 
    value in the app must then be 0.
    """
    def test_trackPostRatingMusicBeeWav0Star(self):
        self.login(self.testUser)
        response = self.postSampleTrack("no star.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 0


    """
    The uploaded wav track has a 0,5 star rating from MusicBee. The corresponding 
    value in the app must then be 1.
    """
    def test_trackPostRatingMusicBeeWavHalfStar(self):
        self.login(self.testUser)
        response = self.postSampleTrack("0 5 star.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 1


    """
    The uploaded wav track has a 1 star rating from MusicBee. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingMusicBeeWav1Star(self):
        self.login(self.testUser)
        response = self.postSampleTrack("1 star.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 2


    """
    The uploaded wav track has a 1,5 star rating from MusicBee. The corresponding 
    value in the app must then be 3.
    """
    def test_trackPostRatingMusicBeeWav1AndHalfStar(self):        
        self.login(self.testUser)
        response = self.postSampleTrack("1 5 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 3
    

    """
    The uploaded wav track has a 2 stars rating set from MusicBee. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingMusicBeeWav2Stars(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("2 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 4


    """
    The uploaded wav track has a 2,5 stars rating from MusicBee. The corresponding 
    value in the app must then be 5.
    """
    def test_trackPostRatingMusicBeeWav2AndHalfStar(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("2 5 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 5
    

    """
    The uploaded wav track has a 3 stars rating set from MusicBee. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingMusicBeeWav3Stars(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("3 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 6
        

    """
    The uploaded wav track has a 3,5 stars rating from MusicBee. The corresponding 
    value in the app must then be 7.
    """
    def test_trackPostRatingMusicBeeWav3AndHalfStar(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("3 5 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 7


    """
    The uploaded wav track has a 4 stars rating set from MusicBee. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingMusicBeeWav4Stars(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("4 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 8
        

    """
    The uploaded wav track has a 4,5 stars rating from MusicBee. The corresponding 
    value in the app must then be 9.
    """
    def test_trackPostRatingMusicBeeWav4AndHalfStar(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("4 5 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 9


    """
    The uploaded wav track has a 5 stars rating set from MusicBee. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingMusicBeeWav5Stars(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("5 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 10
