from rest_framework import status

from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase

class TrackDownloadViewTestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackDownloadData']
    sampleDirectoryRelativePath = "test/view/track/download/sample/"

    def test_libraryTrackDownload(self):
        self.login(self.testUser)

        # File no longer exists
        response = self.downloadTrack(trackUuid="36nS4LVDssLh4BvTdlbJEK")
        assert response.status_code == status.HTTP_410_GONE

        # OK
        response = self.downloadTrack(trackUuid="lyluyfvluyluycutc")
        assert response.status_code == status.HTTP_200_OK
