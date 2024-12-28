from rest_framework import status

from bodzify_api.filter.set.playlist.Fields import Fields as FilterSetFields
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames
from bodzify_api.model.playlist.children.manual.ManualPlaylistTypeLabel import VALUE as MANUAL_PLAYLIST_TYPE_LABEL
from bodzify_api.serializer.schema.model.playlist.base.output.detailed import Fields as PlaylistGetFields
from bodzify_api.test.get_filters.char.EnumCharFilterTestCase import EnumCharFilterTestCase
from bodzify_api.test.view.playlist.base.PlaylistTestCase import PlaylistTestCase


class TestCase(EnumCharFilterTestCase, PlaylistTestCase):

    def setUp(self, methods_names_to_implement=None):
        specific_values = [CriterialessPlaylistNames.GENRE, CriterialessPlaylistNames.TAG]
        return super().setUp(specific_values=specific_values,
                             allow_empty_value=False,
                             methods_names_to_implement=methods_names_to_implement)

    def test_not_provided_then_results(self):
        rock_criteria_name = "Rock"
        self.model_fixture_factory.create_genre(name=rock_criteria_name)
        manual_playlist_name = "Teuf"
        self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)

        response = self._get_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 5
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert rock_criteria_name in names
        assert manual_playlist_name in names
        assert CriterialessPlaylistNames.GENRE in names
        assert CriterialessPlaylistNames.TAG in names

    def test_empty_then_error(self):
        response = self._get_playlists(**{FilterSetFields.TYPE_LABEL: ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_value_is_genre_then_results(self):
        rock_criteria_name = "Rock n roll"
        self.model_fixture_factory.create_genre(name=rock_criteria_name)

        response = self._get_playlists(**{FilterSetFields.TYPE_LABEL: CriterialessPlaylistNames.GENRE})

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert rock_criteria_name in names
        assert CriterialessPlaylistNames.GENRE in names

    def test_value_is_tag_then_results(self):
        response = self._get_playlists(**{FilterSetFields.TYPE_LABEL: CriterialessPlaylistNames.TAG})

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert CriterialessPlaylistNames.TAG in names

    def test_value_is_manual_then_results(self):
        manual_playlist_name = "Teuf"
        self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)
        self.model_fixture_factory.create_genre(name='rock')

        response = self._get_playlists(**{FilterSetFields.TYPE_LABEL: MANUAL_PLAYLIST_TYPE_LABEL})

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert manual_playlist_name in names

    def test_value_is_wrong_then_error(self):
        response = self._get_playlists(**{FilterSetFields.TYPE_LABEL: 'wrong_value'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
