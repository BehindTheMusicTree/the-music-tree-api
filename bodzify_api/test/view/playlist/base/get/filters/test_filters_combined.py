

from rest_framework import status

from bodzify_api.model.criteria.CriteriaType import CriteriaTypesLabel
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import SpecialNames as LibTrackMixinSpecialNames
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import TypesLabel as CriteriaPlaylistTypesLabels
from bodzify_api.model.playlist.children.ManualPlaylist import TYPE_LABEL as MANUAL_PLAYLIST_TYPE_LABEL
from bodzify_api.model.playlist.children.ManualPlaylist import SpecialNames as MANUAL_PLAYLIST_SPECIAL_NAMES
from bodzify_api.serializer.schema.playlist.base.input.query_param import Fields as GetQueryParams
from bodzify_api.serializer.schema.playlist.base.output.detailed import Fields as PlaylistGetFields
from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase


class TestCase(BasePlaylistTestCase):

    def test_type_genre_and_name_tagless_then_no_result(self):
        data_dict = {
            GetQueryParams.TYPE: CriteriaPlaylistTypesLabels.GENRE,
            GetQueryParams.NAME: LibTrackMixinSpecialNames.TAGLESS
        }
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 0

    def test_type_genre_and_name_genreless_then_one_result(self):
        data_dict = {
            GetQueryParams.TYPE: CriteriaPlaylistTypesLabels.GENRE,
            GetQueryParams.NAME: LibTrackMixinSpecialNames.GENRELESS
        }
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][PlaylistGetFields.NAME] == LibTrackMixinSpecialNames.GENRELESS

    def test_type_simple_and_name_all_then_one_result(self):
        data_dict = {
            GetQueryParams.TYPE: MANUAL_PLAYLIST_TYPE_LABEL,
            GetQueryParams.NAME: MANUAL_PLAYLIST_SPECIAL_NAMES.ALL
        }
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][PlaylistGetFields.NAME] == MANUAL_PLAYLIST_SPECIAL_NAMES.ALL

    def test_type_genre_and_genre_name_then_results(self):
        genre1_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre1_name)
        genre2_name = "Punk rock"
        self.model_fixture_factory.create_genre(name=genre2_name)

        data_dict = {
            GetQueryParams.TYPE: CriteriaTypesLabel.GENRE,
            GetQueryParams.NAME: 'rock'
        }
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert genre1_name in names
        assert genre2_name in names

    def test_type_simple_and_name_contains_all_then_results(self):
        gmanual_playlist_name = "allez laaaa"
        self.model_fixture_factory.create_manual_playlist(name=gmanual_playlist_name)

        data_dict = {
            GetQueryParams.TYPE: MANUAL_PLAYLIST_TYPE_LABEL,
            GetQueryParams.NAME: 'all'
        }
        response = self._get(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert gmanual_playlist_name in names
        assert MANUAL_PLAYLIST_SPECIAL_NAMES.ALL in names
