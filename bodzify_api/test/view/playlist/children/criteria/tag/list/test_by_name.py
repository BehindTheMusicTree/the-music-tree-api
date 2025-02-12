from rest_framework import status

from bodzify_api.model.playlist.children.criteria.tag.TagPlaylist import TagPlaylist
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.filtering.set.playlist.Fields import Fields as FilterFields
from bodzify_api.test.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.playlist.children.criteria.tag.TagPlaylistTestCase import TagPlaylistTestCase


class TestCase(TagPlaylistTestCase, NotNullableFreeCharFilterTestCase):

    def test_empty_then_error(self):
        self.model_fixture_factory.create_tag(name="Fiesta")

        response = self._get_tag_playlists(**{FilterFields.NAME: ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_genre_playlists_then_not_in_results(self):
        tag = self.model_fixture_factory.create_tag(name="foot")
        gnere = self.model_fixture_factory.create_genre(name="footcode")

        response = self._get_tag_playlists(**{FilterFields.NAME: 'foot'})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert tag.name in result_names
        assert gnere.name not in result_names

    def test_contains_in_another_case_then_results(self):
        criteria1 = self.model_fixture_factory.create_tag(name="Fiesta")
        criteria2 = self.model_fixture_factory.create_tag(name="Fiestaabilly")
        self.model_fixture_factory.create_tag(name="Punk")

        response = self._get_tag_playlists(**{FilterFields.NAME: 'RO'})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert criteria1.name in result_names
        assert criteria2.name in result_names

    def test_not_provided_then_results(self):
        criteria1 = self.model_fixture_factory.create_tag(name="Fiesta")
        criteria2 = self.model_fixture_factory.create_tag(name="Fiestaabilly")
        criteria3 = self.model_fixture_factory.create_tag(name="Punk")

        response = self._get_tag_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 4
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert criteria1.name in result_names
        assert criteria2.name in result_names
        assert criteria3.name in result_names

    def test_name_in_tagless_and_criteria_name_then_results(self):
        tag_tag = self.model_fixture_factory.create_tag(name="tag")
        tag_fiesta = self.model_fixture_factory.create_tag(name="Fiesta")

        response = self._get_tag_playlists(**{FilterFields.NAME: 'taG'})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert tag_tag.name in result_names
        assert tag_fiesta.name not in result_names
        tagless_playlist: TagPlaylist = TagPlaylist.objects.get(user=self.test_user1, criteria=None)
        assert tagless_playlist.name in result_names
