#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingMusicBeeFlac(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/rating/musicbee/flac/sample/"


    """
    The uploaded flac track has no rating from MusicBee. The corresponding 
    value in the app must then be None.
    """
    def test_trackPostRatingMusicBeeFlacNoRating(self):
        self.login(self.testUser)
        response = self.postSampleTrack("no rating.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == None


    """
    The uploaded flac track has a 0 star rating from MusicBee. The corresponding 
    value in the app must then be 0.
    """
    def test_trackPostRatingMusicBeeFlac0Star(self):
        self.login(self.testUser)
        response = self.postSampleTrack("no star.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 0


    """
    The uploaded flac track has a 0,5 star rating from MusicBee. The corresponding 
    value in the app must then be 1.
    """
    def test_trackPostRatingMusicBeeFlacHalfStar(self):
        self.login(self.testUser)
        response = self.postSampleTrack("0 5 star.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 1


    """
    The uploaded flac track has a 1 star rating from MusicBee. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingMusicBeeFlac1Star(self):
        self.login(self.testUser)
        response = self.postSampleTrack("1 star.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 2


    """
    The uploaded flac track has a 1,5 star rating from MusicBee. The corresponding 
    value in the app must then be 3.
    """
    def test_trackPostRatingMusicBeeFlac1AndHalfStar(self):        
        self.login(self.testUser)
        response = self.postSampleTrack("1 5 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 3
    

    """
    The uploaded flac track has a 2 stars rating set from MusicBee. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingMusicBeeFlac2Stars(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("2 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 4


    """
    The uploaded flac track has a 2,5 stars rating from MusicBee. The corresponding 
    value in the app must then be 5.
    """
    def test_trackPostRatingMusicBeeFlac2AndHalfStar(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("2 5 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 5
    

    """
    The uploaded flac track has a 3 stars rating set from MusicBee. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingMusicBeeFlac3Stars(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("3 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 6
        

    """
    The uploaded flac track has a 3,5 stars rating from MusicBee. The corresponding 
    value in the app must then be 7.
    """
    def test_trackPostRatingMusicBeeFlac3AndHalfStar(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("3 5 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 7


    """
    The uploaded flac track has a 4 stars rating set from MusicBee. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingMusicBeeFlac4Stars(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("4 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 8
        

    """
    The uploaded flac track has a 4,5 stars rating from MusicBee. The corresponding 
    value in the app must then be 9.
    """
    def test_trackPostRatingMusicBeeFlac4AndHalfStar(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("4 5 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 9


    """
    The uploaded flac track has a 5 stars rating set from MusicBee. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingMusicBeeFlac5Stars(self):       
        self.login(self.testUser)
        response = self.postSampleTrack("5 stars.flac")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 10
