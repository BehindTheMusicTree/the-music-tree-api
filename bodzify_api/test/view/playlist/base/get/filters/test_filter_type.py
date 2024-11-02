

from rest_framework import status

from bodzify_api.serializer.schema.playlist.base.output.detailed import Fields as PlaylistGetFields
from bodzify_api.test.get_filters.GetFilterWithSpecificValuesTestCase import GetFilterWithSpecificValuesTestCase
from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase


class TestCase(GetFilterWithSpecificValuesTestCase, BasePlaylistTestCase):

    def setUp(self, methods_names_to_implement=None):
        specific_values = [
            CriteriaPlaylistTypesLabels.GENRE,
            CriteriaPlaylistTypesLabels.TAG,
            MANUAL_PLAYLIST_SPECIAL_NAMES
        ]
        return super().setUp(specific_values=specific_values,
                             allow_empty_value=False,
                             methods_names_to_implement=methods_names_to_implement)

    def test_is_not_provided_then_results(self):
        rock_criteria_name = "Rock"
        self.model_fixture_factory.create_genre(name=rock_criteria_name)

        manual_playlist_name = "Teuf"
        self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)

        response = self._get()
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 5
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert rock_criteria_name in names
        assert manual_playlist_name in names
        assert LibTrackMixinSpecialNames.GENRELESS in names
        assert LibTrackMixinSpecialNames.TAGLESS in names
        assert MANUAL_PLAYLIST_SPECIAL_NAMES.ALL in names

    def test_is_empty_then_error(self):
        data_dict = {GetQueryParams.TYPE: ''}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_value_is_genre_then_resultst(self):
        rock_criteria_name = "Rock n roll"
        self.model_fixture_factory.create_genre(name=rock_criteria_name)
        data_dict = {GetQueryParams.TYPE: CriteriaPlaylistTypesLabels.GENRE}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert rock_criteria_name in names
        assert LibTrackMixinSpecialNames.GENRELESS in names

    def test_value_is_tag_then_results(self):
        data_dict = {GetQueryParams.TYPE: CriteriaPlaylistTypesLabels.TAG}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert LibTrackMixinSpecialNames.TAGLESS in names

    def test_value_is_simple_then_results(self):
        manual_playlist_name = "Teuf"
        self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)
        self.model_fixture_factory.create_genre(name='rock')

        data_dict = {GetQueryParams.TYPE: MANUAL_PLAYLIST_TYPE_LABEL}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert MANUAL_PLAYLIST_SPECIAL_NAMES.ALL in names
        assert manual_playlist_name in names

    def test_value_is_wrong_then_error(self):
        data_dict = {GetQueryParams.TYPE: 'wrong_value'}
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
