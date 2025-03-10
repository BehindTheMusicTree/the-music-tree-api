from unittest.mock import patch

from bodzify_api.model.album.Album import Album
from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase


class TestCase(ArtistTestCase):

    def test_exception_then_rollback(self):
        artist = self.model_fixture_factory.create_artist(name="Muse")
        album_name = "Black Holes and Revelations"
        self.model_fixture_factory.create_album(name=album_name, album_artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="Starlight")

        with patch('bodzify_api.model.track.lib.LibraryTrack.LibraryTrack.delete') as mock_delete:
            exception_message = "Delete failed!"
            mock_delete.side_effect = Exception(exception_message)

            try:
                self._delete_artist(uuid=artist.uuid)
            except Exception as e:
                assert str(e) == exception_message
                assert Album.objects.filter(user=self.test_user1, name=album_name).exists()
