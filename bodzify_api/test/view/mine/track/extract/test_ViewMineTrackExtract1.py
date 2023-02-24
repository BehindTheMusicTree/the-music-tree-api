#!/usr/bin/env python
import os
from django.urls import reverse
from rest_framework import status
from bodzify_api.test.view.mine.track.extract.MineTrackExtractViewTestCase import (
        MineTrackExtractViewTestCase)
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
from bodzify_api.model.track.LibraryTrack import LibraryTrack
import bodzify_api.settings as settings


class MineTrackExtractViewTestCase(MineTrackExtractViewTestCase):

    fixtures = ['initial_data', 'TestUserData']

    def test_mineTrackExtrack(self):
        self.login(self.testUser)

        trackUrl = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
        + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_KN414JidBi"
        + "kY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
            "title": "du rap",
            "artist": "Jul",
            # No album field returned by myfreemp3
            "duration": 1.2233,
            "releasedOn": 1290292
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(title="du rap")
        assert track.artist.name == "Jul"
        assert track.album == None
        assert track.genre.name == CriteriaSpecialNames.GENRE_GENRELESS
        assert track.rating == 0
        assert track.file.name == self.testUserLibraryRelativePath + "Jul_-_du_rap.mp3"
        assert os.path.exists(settings.MEDIA_ROOT + track.file.name)
