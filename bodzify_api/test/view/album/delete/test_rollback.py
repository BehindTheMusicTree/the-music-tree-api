from unittest.mock import patch

from rest_framework import status

from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_exception_then_rollback(self):
        uploaded_track_title = "Assassin"
        muse_artist = self.model_fixture_factory.create_artist(name="Muse")
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations")
        self.model_fixture_factory.create_uploaded_track_with_file(
            title=uploaded_track_title, artists=[muse_artist], album=black_holes_album)

        with patch('bodzify_api.model.artist.Artist.Artist.delete') as mock_delete:
            exception_message = "Delete failed!"
            mock_delete.side_effect = Exception(exception_message)

            response = self._delete_album(uuid=black_holes_album.uuid)
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert UploadedTrack.objects.filter(user=self.test_user1, title=uploaded_track_title).exists()
