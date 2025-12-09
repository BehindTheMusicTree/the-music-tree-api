from unittest.mock import patch

from rest_framework import status

from api.model.track.Track import Track
from api.test.integration.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_exception_then_rollback(self):
        track_title = "Assassin"
        muse_artist = self.model_fixture_factory.create_artist(name="Muse")
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations")
        self.model_fixture_factory.create_track_with_file(
            title=track_title, artists=[muse_artist], album=black_holes_album)

        with patch('api.model.artist.Artist.Artist.delete') as mock_delete:
            exception_message = "Delete failed!"
            mock_delete.side_effect = Exception(exception_message)

            response = self._delete_album(uuid=black_holes_album.uuid)
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert Track.objects.filter(user=self.test_user1, title=track_title).exists()
