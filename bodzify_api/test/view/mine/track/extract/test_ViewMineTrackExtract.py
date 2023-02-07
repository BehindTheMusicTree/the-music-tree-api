import os

from django.urls import reverse

from rest_framework import status

from bodzify_api.test.view.ViewTestCase import ViewTestCase
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
from bodzify_api.model.track.LibraryTrack import LibraryTrack
import bodzify_api.settings as settings


class MineTrackExtractViewTestCase(ViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewMineTrackExtractData']

    def extract(self, data):
        return self.apiClient.post(
            path=reverse('mine-track-extract'), data=data)

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
        assert track.album == ""
        assert track.genre.name == CriteriaSpecialNames.GENRE_GENRELESS
        assert track.rating == 0
        assert track.file.name == self.testUserLibraryRelativePath + "Jul_-_du_rap.mp3"
        assert os.path.exists(settings.MEDIA_ROOT + track.file.name)

        # With existing artist
        trackUrl = ("https://cs9-15v4.vkuseraudio.net/s/v1/acmp/qCKkBk5i-Rl-QBdJM2m2lGbeRX6gB2ji" +
                    "zqo-ZXY7dSsA7VYaDDbb7nHloh42XVdi1gZ-U0BtWIa1I5qZJ3RspFGJbomdr4P-LwffbPvwWnZ" +
                    "_hyJ2dSP4WIET6pg2tz6yUtco3HKAodQaY85KeQocwpIiOzKLUb1hDAf5a7xQ9_NrLESvCw.mp3")
        data = {
            "url": trackUrl,
            "title": "Summer Moved On",
            "artist": "a-ha",
            # No album field returned by myfreemp3
            "duration": 1.2233,
            "releasedOn": 1290292
        }

        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED

        track = LibraryTrack.objects.get(title="Summer Moved On")
        assert track.artist.name == "a-ha"
        assert track.album == ""
        assert track.genre.name == CriteriaSpecialNames.GENRE_GENRELESS
        assert track.rating == 0
        assert track.file.name == self.testUserLibraryRelativePath + "a-ha_-_Summer_Moved_On.mp3"
        assert os.path.exists(settings.MEDIA_ROOT + track.file.name)
