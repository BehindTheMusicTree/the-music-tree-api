from rest_framework import status

from bodzify_api.test.utils.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase
from bodzify_api.serializer.model.album.Fields import Fields as AlbumFields
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(AlbumTestCase, NotNullableFreeCharFilterTestCase):

    def test_empty_then_error(self):
        response = self._get_albums(name='')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == AlbumFields.NAME
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.BLANK.value

    def test_contains_in_another_case_then_results(self):
        album = self.model_fixture_factory.create_album(name="Muse")
        self.model_fixture_factory.create_album(name="Jon")

        response = self._get_albums(name='MUs')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][AlbumFields.NAME] == album.name

    def test_not_provided_then_results(self):
        self.model_fixture_factory.create_album(name="Muse")
        self.model_fixture_factory.create_album(name="Jon")

        response = self._get_albums()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
