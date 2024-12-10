from unittest.mock import patch

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_exception_then_rollback(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_metal = self.model_fixture_factory.create_genre(name="Metal")

        with patch('bodzify_api.model.playlist.children.criteria.CriteriaPlaylist.CriteriaPlaylist.save') as mock:
            exception_message = "Save failed!"
            mock.side_effect = Exception(exception_message)

            try:
                self._put_genre(uuid=genre_punk.uuid, parent=genre_metal.uuid)
            except Exception as e:
                assert str(e) == exception_message
                genre: Genre = Genre.objects.get(user=self.test_user1, uuid=genre_punk.uuid)
                assert genre.parent == genre_rock
