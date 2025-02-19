from rest_framework import status

from bodzify_api.serializer.schema.model.playlist.children.manual.output.Fields import Fields
from bodzify_api.test.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields
from bodzify_api.filtering.set.playlist.Fields import Fields as FilterFields


class TestCase(ManualPlaylistTestCase, NotNullableFreeCharFilterTestCase):

    def test_empty_then_error(self):
        self.model_fixture_factory.create_manual_playlist(name="foot")
        self.model_fixture_factory.create_manual_playlist(name="cuisine")

        response = self._get_manual_playlists(name='')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FieldErrors.FIELD] == FilterFields.NAME
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.BLANK.value

    def test_contains_in_another_case_then_results(self):
        manual_playlist1 = self.model_fixture_factory.create_manual_playlist(name="foot")
        manual_playlist2 = self.model_fixture_factory.create_manual_playlist(name="football")
        self.model_fixture_factory.create_manual_playlist(name="cuisine")

        response = self._get_manual_playlists(name='FOO')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[Fields.NAME] for result in self.results]
        assert manual_playlist1.name in result_names
        assert manual_playlist2.name in result_names

    def test_not_provided_then_results(self):
        manual_playlist1 = self.model_fixture_factory.create_manual_playlist(name="foot")
        manual_playlist2 = self.model_fixture_factory.create_manual_playlist(name="football")
        self.model_fixture_factory.create_manual_playlist(name="cuisine")

        response = self._get_manual_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 3
        result_names = [result[Fields.NAME] for result in self.results]
        assert manual_playlist1.name in result_names
        assert manual_playlist2.name in result_names
        assert "cuisine" in result_names
