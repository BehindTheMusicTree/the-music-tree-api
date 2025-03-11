from rest_framework import status

from bodzify_api.filtering.set.playlist.Fields import Fields as Filters
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames
from bodzify_api.model.playlist.PlaylistTypesLabel import PlaylistTypesLabel
from bodzify_api.serializer.model.playlist.base.output.detailed import Fields as PlaylistGetFields
from bodzify_api.test.view.playlist.base.PlaylistTestCase import PlaylistTestCase


class TestCase(PlaylistTestCase):

    def test_type_genre_and_name_tagless_then_no_result(self):
        data_dict = {
            Filters.TYPE_LABEL_PUBLIC: PlaylistTypesLabel.GENRE,
            Filters.NAME: CriterialessPlaylistNames.TAG
        }
        response = self._get_playlists(**data_dict)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 0

    def test_type_genre_and_name_genreless_then_one_result(self):
        data_dict = {
            Filters.TYPE_LABEL_PUBLIC: PlaylistTypesLabel.GENRE,
            Filters.NAME: CriterialessPlaylistNames.GENRE
        }
        response = self._get_playlists(**data_dict)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][PlaylistGetFields.NAME] == CriterialessPlaylistNames.GENRE

    def test_type_genre_and_genre_name_then_results(self):
        genre1_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre1_name)
        genre2_name = "Punk rock"
        self.model_fixture_factory.create_genre(name=genre2_name)

        data_dict = {
            Filters.TYPE_LABEL_PUBLIC: PlaylistTypesLabel.GENRE,
            Filters.NAME: 'rock'
        }
        response = self._get_playlists(**data_dict)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert genre1_name in names
        assert genre2_name in names
