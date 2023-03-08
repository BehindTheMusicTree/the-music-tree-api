#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingMusicBeeMp3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/rating/musicbee/mp3/sample/"


    """
    The uploaded mp3 track has no rating from MusicBee. The corresponding 
    value in the app must then be None.
    """
    def test_trackPostRatingMusicBeeMp3NoRating(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("no rating.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == None


    """
    The uploaded mp3 track has a 0 star rating from MusicBee. The corresponding 
    value in the app must then be 0.
    """
    def test_trackPostRatingMusicBeeMp30Star(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("no star.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 0


    """
    The uploaded mp3 track has a 0,5 star rating from MusicBee. The corresponding 
    value in the app must then be 1.
    """
    def test_trackPostRatingMusicBeeMp3HalfStar(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("0 5 star.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 1


    """
    The uploaded mp3 track has a 1 star rating from MusicBee. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingMusicBeeMp31Star(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("1 star.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 2


    """
    The uploaded mp3 track has a 1,5 star rating from MusicBee. The corresponding 
    value in the app must then be 3.
    """
    def test_trackPostRatingMusicBeeMp31AndHalfStar(self):        
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("1 5 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 3
    

    """
    The uploaded mp3 track has a 2 stars rating set from MusicBee. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingMusicBeeMp32Stars(self):       
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("2 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 4


    """
    The uploaded mp3 track has a 2,5 stars rating from MusicBee. The corresponding 
    value in the app must then be 5.
    """
    def test_trackPostRatingMusicBeeMp32AndHalfStar(self):       
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("2 5 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 5
    

    """
    The uploaded mp3 track has a 3 stars rating set from MusicBee. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingMusicBeeMp33Stars(self):       
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("3 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 6
        

    """
    The uploaded mp3 track has a 3,5 stars rating from MusicBee. The corresponding 
    value in the app must then be 7.
    """
    def test_trackPostRatingMusicBeeMp33AndHalfStar(self):       
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("3 5 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 7


    """
    The uploaded mp3 track has a 4 stars rating set from MusicBee. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingMusicBeeMp34Stars(self):       
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("4 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 8
        

    """
    The uploaded mp3 track has a 4,5 stars rating from MusicBee. The corresponding 
    value in the app must then be 9.
    """
    def test_trackPostRatingMusicBeeMp34AndHalfStar(self):       
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("4 5 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 9


    """
    The uploaded mp3 track has a 5 stars rating set from MusicBee. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingMusicBeeMp35Stars(self):       
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("5 stars.mp3")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 10
