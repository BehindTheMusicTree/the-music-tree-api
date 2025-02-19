from rest_framework import status

from bodzify_api.serializer.schema.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.test.field.filter.foreign_key.PrivateForeignKeyFilterTestCase import PrivateForeignKeyFilterTestCase
from bodzify_api.test.view.playlist.children.criteria.tag.TagPlaylistTestCase import TagPlaylistTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(TagPlaylistTestCase, PrivateForeignKeyFilterTestCase):

    def setUp(self, methods_names_to_implement=None):
        return super().setUp(allow_empty_value=True, methods_names_to_implement=methods_names_to_implement)

    def test_not_provided_then_results(self):
        tag_fiesta = self.model_fixture_factory.create_tag(name="Fiesta")
        self.model_fixture_factory.create_tag(name="Fiestaabilly")
        self.model_fixture_factory.create_tag(name="Koko", parent=tag_fiesta)

        response = self._get_tag_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 4

    def test_invalid_uuid_then_error(self):
        self.model_fixture_factory.create_tag(name="Fiesta")

        response = self._get_tag_playlists(**{RietrieveFields.PARENT: 'invalid-uuid'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FIELD] == RietrieveFields.PARENT
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.CODE] == FieldValidationErrorCode.BLANK.value

    def test_empty_then_results(self):
        tag_fiesta = self.model_fixture_factory.create_tag(name="Fiesta")
        tag_fiestaabilly = self.model_fixture_factory.create_tag(name="Fiestaabilly")
        tag_koko = self.model_fixture_factory.create_tag(name="Koko", parent=tag_fiesta)

        response = self._get_tag_playlists(**{RietrieveFields.PARENT: ''})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 3
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert tag_fiesta.name in result_names
        assert tag_fiestaabilly.name in result_names
        assert tag_koko.name not in result_names

    def test_tags_playlist_parent_corresponds_to_filter_then_return_instances(self):
        tag_fiesta = self.model_fixture_factory.create_tag(name="Fiesta")
        tag_fiestaabilly = self.model_fixture_factory.create_tag(name="Fiestaabilly", parent=tag_fiesta)
        tag_punk = self.model_fixture_factory.create_tag(name="Punk", parent=tag_fiesta)

        response = self._get_tag_playlists(**{RietrieveFields.PARENT: tag_fiesta.criteria_playlist.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert tag_fiestaabilly.name in result_names
        assert tag_punk.name in result_names
