from unittest.mock import patch

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_exception_then_rollback(self):
        lib_track_title = "Assassin"
        muse_artist = self.model_fixture_factory.create_artist(name="Muse")
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations")
        self.model_fixture_factory.create_lib_track_with_file(title=lib_track_title,
                                                              artists=[muse_artist],
                                                              album=black_holes_album)
        with patch('bodzify_api.model.artist.Artist.Artist.delete') as mock_delete:
            exception_message = "Delete failed!"
            mock_delete.side_effect = Exception(exception_message)

            try:
                self._delete_album(uuid=black_holes_album.uuid)
            except Exception as e:
                assert str(e) == exception_message
                assert LibraryTrack.objects.filter(user=self.test_user1, title=lib_track_title).exists()
