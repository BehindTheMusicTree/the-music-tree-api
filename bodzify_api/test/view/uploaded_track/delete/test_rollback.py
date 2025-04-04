from unittest.mock import patch

from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_exception_then_rollback(self):
        album = self.model_fixture_factory.create_album(name="album")
        track = self.model_fixture_factory.create_uploaded_track_with_file(title="joie", album=album)

        with patch('bodzify_api.model.album.Album.Album.save') as mock:
            exception_message = "Save failed!"
            mock.side_effect = Exception(exception_message)

            try:
                self._delete_uploaded_track(uuid=track.uuid)
            except Exception as e:
                assert str(e) == exception_message
                assert UploadedTrack.objects.filter(uuid=track.uuid).exists()
