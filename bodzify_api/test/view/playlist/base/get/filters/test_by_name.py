from rest_framework import status

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.test.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.playlist.base.PlaylistTestCase import PlaylistTestCase
from bodzify_api.filtering.set.playlist.Fields import Fields as GetQueryParams
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames


class TestCase(PlaylistTestCase, NotNullableFreeCharFilterTestCase):

    def setUp(self) -> None:
        super().setUp(allow_empty_value=False, methods_names_to_implement=None)

    def test_empty_then_error(self) -> None:
        response = self._get_playlists(**{GetQueryParams.NAME: ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_provided_then_results(self) -> None:
        self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_manual_playlist(name="Teuf")

        response = self._get_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == Playlist.objects.filter(user=self.test_user1).count()

    def test_contains_in_another_case_then_results(self) -> None:
        manual_playlist_name = "Teuf"
        self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)

        response = self._get_playlists(**{GetQueryParams.NAME: manual_playlist_name.upper()})

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        names_lowered = [result[GetQueryParams.NAME].lower() for result in self.results]
        assert manual_playlist_name.lower() in names_lowered

    def test_genreless_special_name_then_results(self) -> None:
        response = self._get_playlists(**{GetQueryParams.NAME: 'geNr'})

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GetQueryParams.NAME] == CriterialessPlaylistNames.GENRE

    def test_tagless_special_name_then_results(self) -> None:
        response = self._get_playlists(**{GetQueryParams.NAME: 'aGl'})

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GetQueryParams.NAME] == CriterialessPlaylistNames.TAG

    def test_value_in_simple_criteria_and_special_names_then_results(self) -> None:
        manual_playlist_name = "lEsson"
        self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)
        criteria_name = "leSsa"
        self.model_fixture_factory.create_genre(name=criteria_name)

        response = self._get_playlists(**{GetQueryParams.NAME: 'Less'})

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 4
        names_lowered = [result[GetQueryParams.NAME].lower() for result in self.results]
        assert manual_playlist_name.lower() in names_lowered
        assert criteria_name.lower() in names_lowered
        assert CriterialessPlaylistNames.GENRE.lower() in names_lowered
        assert CriterialessPlaylistNames.TAG.lower() in names_lowered
