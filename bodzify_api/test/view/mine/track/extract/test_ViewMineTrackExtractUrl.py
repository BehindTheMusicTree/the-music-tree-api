#!/usr/bin/env python
import os
from django.urls import reverse
from rest_framework import status
import bodzify_api.service.AudioMetadataService as AudioMetadataService
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
from bodzify_api.model.track.LibraryTrack import LibraryTrack
import bodzify_api.settings as settings


class MineTrackExtractViewTestUrl(MineTrackExtractViewTestCase):

    fixtures = ['initial_data', 'TestUserData']

    """
    Trying to extract a track from a wrong url should fail with a 400 (bad request).
    """
    def test_mineTrackExtrackUrlWrong(self):
        self.login(self.testUser)

        trackUrl = ("https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3")
        data = {
            "url": trackUrl,
            "title": "du rap",
            "artist": "Jul",
            "releasedOn": 1290292
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
