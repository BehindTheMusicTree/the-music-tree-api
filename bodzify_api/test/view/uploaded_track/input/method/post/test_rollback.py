from unittest.mock import patch

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_exception_then_rollback(self):
        genre_name = "Rock"
        with patch('bodzify_api.model.uploaded_track.UploadedTrack.UploadedTrack.save') as mock_save:
            exception_message = "Save failed!"
            mock_save.side_effect = Exception(exception_message)
            try:
                self._post_uploaded_track(genre_name=genre_name)
            except Exception as e:
                assert str(e) == exception_message
                assert not Genre.objects.filter(user=self.test_user1, name=genre_name).exists()
