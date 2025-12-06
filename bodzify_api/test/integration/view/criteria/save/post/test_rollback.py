from unittest.mock import patch

from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.integration.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_exception_then_rollback(self):
        genre_name = "Rock"
        with patch('bodzify_api.model.playlist.children.criteria.CriteriaPlaylist.CriteriaPlaylist.save') as mock:
            exception_message = "Save failed!"
            mock.side_effect = Exception(exception_message)

            response = self._post_genre(name=genre_name)
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert not Genre.objects.filter(user=self.test_user1, name=genre_name).exists()
