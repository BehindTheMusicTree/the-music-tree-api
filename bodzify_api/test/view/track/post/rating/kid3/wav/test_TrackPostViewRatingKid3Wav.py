#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseRatingKid3Wav(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/rating/kid3/wav/sample/"

    """
    The uploaded wav track has a no rating from Kid3. The corresponding 
    value in the app must then be None.
    """
    def test_trackPostRatingKid3WavNoRating(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("no rating.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == None

    """
    The uploaded wav track has a 1 star rating from Kid3. The corresponding 
    value in the app must then be 2.
    """
    def test_trackPostRatingKid3Wav1Star(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("1 star.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 2
    

    """
    The uploaded wav track has a 2 stars rating set from Kid3. The corresponding 
    value in the app must then be 4.
    """
    def test_trackPostRatingKid3Wav2Stars(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("2 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 4
    

    """
    The uploaded wav track has a 3 stars rating set from Kid3. The corresponding 
    value in the app must then be 6.
    """
    def test_trackPostRatingKid3Wav3Stars(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("3 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 6

    """
    The uploaded wav track has a 4 stars rating set from Kid3. The corresponding 
    value in the app must then be 8.
    """
    def test_trackPostRatingKid3Wav4Stars(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("4 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 8

    """
    The uploaded wav track has a 5 stars rating set from Kid3. The corresponding 
    value in the app must then be 10.
    """
    def test_trackPostRatingKid3Wav5Stars(self):
        self.login(self.testUser)
        response = self._loginAndPostSampleTrack("5 stars.wav")
        trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.rating == 10