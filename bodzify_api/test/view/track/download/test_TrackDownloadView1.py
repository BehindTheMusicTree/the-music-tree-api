from rest_framework import status

from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase

class TrackDownloadViewTestCase1(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackDownloadData1']


    """
    The requested track's file doesn't exist. The returned status must be "410 GONE".
    """
    def test_libraryTrackDownload1FileNotExisting(self):
        self.login(self.testUser)
        response = self.downloadTrack(trackUuid="36nS4LVDssLh4BvTdlbJEK")
        assert response.status_code == status.HTTP_410_GONE
