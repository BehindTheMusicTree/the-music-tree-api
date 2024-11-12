from unittest.mock import patch

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_exception_then_rollback(self):
        genre_name = "Rock"
        with patch('bodzify_api.model.track.lib.LibraryTrack.LibraryTrack') as mock:
            exception_message = "Save failed!"
            mock.side_effect = Exception(exception_message)
            try:
                self._post_lib_track_with_generic_sample_no_tags(genre_name=genre_name)
            except Exception as e:
                assert str(e) == exception_message
                assert not Genre.objects.filter(user=self.test_user1, name=genre_name).exists()
