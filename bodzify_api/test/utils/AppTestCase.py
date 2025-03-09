from pathlib import Path
from typing import Generic, Type, TypeVar, Union, cast

from django.core.management import call_command
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.user.User import User
from bodzify_api.model.uuid.Fields import Fields as UuidModelFields
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as LibTrackPostFields
from bodzify_api.test.utils.AppApiClient import AppApiClient
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.utils.ModelFixtureFactory import ModelFixtureFactory
from bodzify_api.utils import audio_metadata, data_transformer
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields
from bodzify_api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


T = TypeVar('T', bound=models.Model)


class AppTestCase(TestCase, Generic[T]):
    model_class: Type[T]  # Must be defined in child classes
    saved_object: T  # Must be defined in child classes

    api_client: AppApiClient
    saved_lib_track_metadata: dict

    TEST_FILES_BASE_DIR = Path(__file__).parent.parent / 'utils' / 'lib_track' / 'files'

    def _login_as_user(self, user: User):
        self.api_client.force_authenticate(user=user)
        AccessToken.for_user(user)
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer {access}')

    def _login_as_test_user1(self):
        self._login_as_user(self.test_user1)

    def _login_as_test_user2(self):
        self._login_as_user(self.test_user2)

    def _login_as_test_admin(self):
        self._login_as_user(self.test_admin_user)

    def _logout(self):
        self.api_client.force_authenticate(user=None)

    def _set_saved_object_from_response(self, response):
        if not hasattr(self, 'model_class') or self.model_class is None:
            raise NotImplementedError("Test case must define model_class")

        uuid = response.json()[UuidModelFields.UUID]
        # At this point model_class is guaranteed to be a Model class with objects manager
        self.saved_object = self.model_class.objects.get(uuid=uuid)  # type: ignore
        if isinstance(self.saved_object, LibraryTrack):
            self._set_saved_lib_track_metadata()

    def _set_single_result(self, response):
        self.result = response.json()
        if hasattr(self, 'model_class'):
            self._set_saved_object_from_response(response)
        else:
            raise NotImplementedError("Test case must define model_class")

    def _set_results(self, response):
        if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            if response.status_code is not status.HTTP_204_NO_CONTENT:
                # list endpoints return paginated results
                if isinstance(response.json(), dict) and PaginatedResponseFields.RESULTS in response.json():
                    self._set_results_attributes(response)
                else:
                    self._set_single_result(response)
        else:
            self._set_error_response_result(response)

    def _set_error_response_result(self, response):
        """
        Handles responses with field errors in the format:
        {
            "code": 2001,
            "message": "Bad Request",
            "success": false,
            "details": [{
                "message": "One or more fields contain invalid data. Please check the error details for specific 
                    validation requirements",
                "fieldErrors": {
                    "field1": {"message": "...", "code": "..."},
                    "field2": {"message": "...", "code": "..."}
                }
            }]
        }
        """
        self.bad_request_result = response.json()
        bad_request_result_details = self.bad_request_result[ErrorResponseFields.DETAILS]
        self.bad_request_result_field_errors_json = bad_request_result_details.get(ErrorResponseFields.FIELD_ERRORS)
        if self.bad_request_result_field_errors_json:
            # Convert field errors to a list format for easier testing
            self.bad_request_result_field_errors = []
            for field_name, error_list in self.bad_request_result_field_errors_json.items():
                # error_list is a list of error dictionaries
                for error in error_list:
                    self.bad_request_result_field_errors.append({
                        'field': field_name,
                        'message': error['message'],
                        'code': error['code']
                    })

    def _set_results_attributes(self, response):
        response_json = response.json()
        self.results = response_json[PaginatedResponseFields.RESULTS]
        self.results_overall_total = response_json[PaginatedResponseFields.OVERALL_TOTAL]

    def _set_saved_lib_track_metadata(self):
        saved_lib_track = cast(LibraryTrack, self.saved_object)
        self.saved_lib_track_metadata = audio_metadata.get_merged_app_metadata(file=saved_lib_track.track_file.file)

    # Defined here and not in LibTrackTestCase because other views needs sometimes to post a track for testing purposes
    # (testing metadata updates for example)
    def _post_lib_track(self, test_lib_track_filename: TestLibTrackFilename = TestLibTrackFilename.DEFAULT_MP3, **kwargs
                        ) -> Union[JsonResponse, HttpResponse]:
        file_abs_path = self.TEST_FILES_BASE_DIR / test_lib_track_filename

        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {LibTrackPostFields.TRACK_FILE_PUBLIC: sample_file}
            if kwargs:
                kwargs = data_transformer.merge_two_dicts(file_field_dict, kwargs)
            else:
                kwargs = file_field_dict

            return self.api_client.post(
                path=reverse('library-track-list'), data=kwargs, format='multipart', handle_response=self._set_results)

    def _post_lib_track_being_logged_out(self):
        self._logout()
        return self.api_client.post(
            path=reverse('library-track-list'), data={}, format='multipart', handle_response=self._set_results)

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:

        call_command('loaddata', 'app')
        self.test_admin_user = User.objects.create_superuser(
            username='test_admin', password='test_admin', email='test_admin@example.com', is_test_user=True)

        self.test_user1 = User.objects.create_instance(
            username='pytest_user1', password='pytest_user1', email='pytest@user1.com', is_test_user=True)

        self.test_user2 = User.objects.create_instance(
            username='pytest_user2', password='pytest_user2', email='pytest@user2.com', is_test_user=True)

        self.model_fixture_factory = ModelFixtureFactory(
            default_test_user=self.test_user1, test_lib_track_dir=self.TEST_FILES_BASE_DIR,)

        super().setUp()

        if methods_names_to_implement:
            for method_name in methods_names_to_implement:
                if not hasattr(self, method_name) or not callable(getattr(self, method_name)):
                    raise NotImplementedError(f"Subclasses must implement the '{method_name}' method")

        self.api_client = AppApiClient(test_case=self)
        self._login_as_test_user1()
