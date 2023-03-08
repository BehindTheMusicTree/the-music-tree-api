from rest_framework import status

from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase

class TrackDownloadViewTestCase2(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackDownloadData2']
    sampleDirectoryRelativePath = "test/view/track/download/sample/2/"

    """
    The requested track's file exists. The returned status must be "200 OK".
    """
    def test_libraryTrackDownload2FileExisting(self):
        self._login(self.testUser)
        response = self._downloadTrack(trackUuid="lyluyfvluyluycutc")
        assert response.status_code == status.HTTP_200_OK
