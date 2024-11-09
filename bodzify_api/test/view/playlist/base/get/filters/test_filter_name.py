from typing import Optional

from rest_framework import status

from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.test.get_filters.GetFilterWithFreeValuesTestCase import GetFilterWithFreeValuesTestCase
from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase
from bodzify_api.filter.set.playlist.Fields import Fields as GetQueryParams
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylistWithoutCriteriaNames \
    import CriteriaPlaylistWithoutCriteriaNames


class TestCase(GetFilterWithFreeValuesTestCase, BasePlaylistTestCase):

    def setUp(self, allow_empty_value: bool = False, methods_names_to_implement: Optional[list[str]] = None) -> None:
        super().setUp(allow_empty_value=allow_empty_value, methods_names_to_implement=methods_names_to_implement)

    def test_is_empty_then_error(self) -> None:
        data_dict = {GetQueryParams.NAME: ''}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_is_not_provided_then_results(self) -> None:
        self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_manual_playlist(name="Teuf")

        response = self._get()
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == BasePlaylist.objects.filter(user=self.test_user1).count()

    def test_different_case_then_results(self) -> None:
        manual_playlist_name = "Teuf"
        self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)

        data_dict = {GetQueryParams.NAME: manual_playlist_name.upper()}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        names_lowered = [result[GetQueryParams.NAME].lower() for result in self.results]
        assert manual_playlist_name.lower() in names_lowered

    def test_genreless_special_name_then_results(self) -> None:
        data_dict = {GetQueryParams.NAME: 'geNr'}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GetQueryParams.NAME] == CriteriaPlaylistWithoutCriteriaNames.GENRE

    def test_tagless_special_name_then_results(self) -> None:
        data_dict = {GetQueryParams.NAME: 'aGl'}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GetQueryParams.NAME] == CriteriaPlaylistWithoutCriteriaNames.TAG

    def test_value_in_simple_criteria_and_special_names_then_results(self) -> None:
        manual_playlist_name = "lEsson"
        self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)
        criteria_name = "leSsa"
        self.model_fixture_factory.create_genre(name=criteria_name)

        data_dict = {GetQueryParams.NAME: 'Less'}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 4
        names_lowered = [result[GetQueryParams.NAME].lower() for result in self.results]
        assert manual_playlist_name.lower() in names_lowered
        assert criteria_name.lower() in names_lowered
        assert CriteriaPlaylistWithoutCriteriaNames.GENRE.lower() in names_lowered
        assert CriteriaPlaylistWithoutCriteriaNames.TAG.lower() in names_lowered
