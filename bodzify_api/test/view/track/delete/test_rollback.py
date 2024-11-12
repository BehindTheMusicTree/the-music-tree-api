from unittest.mock import patch

from bodzify_api.model.album.Album import Album
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_exception_then_rollback(self):
        album = self.model_fixture_factory.create_album(name="album")
        track = self.model_fixture_factory.create_lib_track_with_file(title="joie", album=album)

        with patch('bodzify_api.model.album.Album.Album.save') as mock:
            exception_message = "Save failed!"
            mock.side_effect = Exception(exception_message)

            try:
                self._delete_lib_track(uuid=track.uuid)
            except Exception as e:
                assert str(e) == exception_message
                assert LibraryTrack.objects.filter(uuid=track.uuid).exists()
