from rest_framework import status

from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TrackDeleteViewTestCase(UploadedTrackTestCase):

    def test_delete_then_delete_file(self):
        track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="We're All To Blame",
            test_uploaded_track_filename=UploadedTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3)
        assert self.test_user1.does_track_filename_exist_in_lib(UploadedTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3)
        assert track.track_file.file

        response = self._delete_uploaded_track(uuid=track.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not UploadedTrack.objects.filter(user=self.test_user1, uuid=track.uuid).exists()
        assert not self.test_user1.does_track_filename_exist_in_lib(
            UploadedTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3)
