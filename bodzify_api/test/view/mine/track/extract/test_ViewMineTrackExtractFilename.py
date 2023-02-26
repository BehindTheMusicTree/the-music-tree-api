#!/usr/bin/env python
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class MineTrackExtractViewTestFilename(MineTrackExtractViewTestCase):

    fixtures = ['initial_data', 'TestUserData']

    """
    When extracting a mp3 track proviging a title "I'm Here" and an artist "Roméo", the resulting 
    filename should be "Roméo_-_I_m_Here.mp3".
    """
    def test_mineTrackExtractFilenameWithOnlyTitle(self):
        self.login(self.testUser)

        trackUrl = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
        + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_KN414JidBi"
        + "kY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
            "title": "I'm Here",
            "artist": "Roméo",
        }
        response = self.extract(data=data)
        trackUuid = response.data['uuid']
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.filename == "Roméo_-_I_m_Here.mp3"


    """
    When extracting a mp3 track proviging only a title ("Hellö") and no artist, the resulting 
    filename should be "Hellö.mp3".
    """
    def test_mineTrackExtractFilenameWithOnlyTitle(self):
        self.login(self.testUser)

        trackUrl = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
        + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_KN414JidBi"
        + "kY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
            "title": "Hellö",
        }
        response = self.extract(data=data)
        trackUuid = response.data['uuid']
        track = LibraryTrack.objects.get(uuid=trackUuid)
        assert track.filename == "Hellö.mp3"