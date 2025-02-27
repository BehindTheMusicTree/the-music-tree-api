import pytest
from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(LibTrackTestCase):

    def test_delete_then_delete_file(self):
        track = self.model_fixture_factory.create_lib_track_with_file(
            title="We're All To Blame", test_lib_track_filename=TestLibTrackFilename.RECORDING_KEMAR_FRANCE_MP3)
        assert self.test_user1.does_track_filename_exist_in_lib(TestLibTrackFilename.RECORDING_KEMAR_FRANCE_MP3)
        assert track.track_file.file

        response = self._delete_lib_track(uuid=track.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not LibraryTrack.objects.filter(user=self.test_user1, uuid=track.uuid).exists()
        assert not self.test_user1.does_track_filename_exist_in_lib(TestLibTrackFilename.RECORDING_KEMAR_FRANCE_MP3)
