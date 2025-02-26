from typing import Generic, Type, TypeVar, Union
from uuid import UUID

from django.db import models
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.user.User import User
from bodzify_api.model.uuid.Fields import Fields as UuidModelFields
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as LibTrackPostFields
from bodzify_api.test.AppApiClient import AppApiClient
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.utils import audio_metadata, data_transformer
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields
from bodzify_api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


T = TypeVar('T', bound=models.Model)


class ApiTestCase(AppTestCase, Generic[T]):
    """Base class for API test cases that handle model instances.

    Child classes should:
    1. Define model_class class variable pointing to their model
    2. Override _set_saved_object if custom fetching logic is needed
    3. Use handle_response=self._set_results in API calls
    """

    model_class: Type[T]  # Must be defined in child classes
    saved_object: T  # Must be defined in child classes

    class LibTrackGenericSamplesFilenameWithoutExtension:
        BELOW_1_SEC = "below 1 sec"
        ONE_STAR = "1 star"
        TAGS_NONE = "tags none"
        TAGS_3_ARTISTS_AND_2_COMMAS_IN_ARTIST = "tags 3 artists and two commas in artist"
        TAGS_ALBUM_KOKO_WITHOUT_ALBUM_ARTISTS = "tags album koko without album artists"
        TAGS_ALBUM_ARTISTS_KOKO_WITHOUT_ALBUM = "tags album artists koko without album"
        TAGS_MAX_LEN_WITH_LETTER_A = "tags max length with letter a"

    api_client: AppApiClient
    saved_lib_track: LibraryTrack
    saved_lib_track_metadata: dict

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

    def _set_saved_object(self, response):
        """Get model instance from response UUID.

        Child classes must define model_class class attribute.
        """
        if not hasattr(self, 'model_class') or self.model_class is None:
            raise NotImplementedError("Test case must define model_class")

        uuid = response.json()[UuidModelFields.UUID]
        # At this point model_class is guaranteed to be a Model class with objects manager
        self.saved_object = self.model_class.objects.get(uuid=uuid)  # type: ignore
        if isinstance(self.saved_object, LibraryTrack):
            self._set_saved_lib_track_metadata(response)

    def _set_single_result(self, response):
        self.result = response.json()
        if hasattr(self, 'model_class'):
            self._set_saved_object(response)
        else:
            raise NotImplementedError("Test case must define model_class")

    def _set_results(self, response):
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            self._set_bad_request_result(response)
        elif response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            # list endpoints return paginated results
            if isinstance(response.json(), dict) and PaginatedResponseFields.RESULTS in response.json():
                self._set_results_attributes(response)
            else:
                self._set_single_result(response)

    def _set_bad_request_result(self, response):
        """Store bad request result details with field-specific error information.

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
        bad_request_result_details = self.bad_request_result[ErrorResponseFields.DETAILS][0]
        self.bad_request_result_field_errors_json = bad_request_result_details[ErrorResponseFields.FIELD_ERRORS]

        # Convert field errors to a list format for easier testing
        self.bad_request_result_field_errors = []
        for field_name, error_list in self.bad_request_result_field_errors_json.items():
            # error_list is a list of error dictionaries
            for error in error_list:
                self.bad_request_result_field_errors.append({
                    ErrorResponseFields.FieldErrors.FIELD: field_name,
                    ErrorResponseFields.FieldErrors.MESSAGE: error[ErrorResponseFields.MESSAGE],
                    ErrorResponseFields.FieldErrors.CODE: error[ErrorResponseFields.FieldErrors.CODE]
                })

    def _set_results_attributes(self, response):
        response_json = response.json()
        self.results = response_json[PaginatedResponseFields.RESULTS]
        self.results_overall_total = response_json[PaginatedResponseFields.OVERALL_TOTAL]

    def _set_saved_lib_track_metadata(self, response):
        saved_lib_track: LibraryTrack = self.saved_object  # type: ignore
        self.saved_lib_track_metadata = \
            audio_metadata.get_merged_normalized_metadata(file=saved_lib_track.track_file.file)

    def _post_lib_track_with_generic_sample(self,
                                            generic_sample_filename_without_extension,
                                            generic_sample_file_extension,
                                            **kwargs) -> Union[JsonResponse, HttpResponse]:
        filename_with_extension = generic_sample_filename_without_extension + '.' + generic_sample_file_extension
        generic_sample_abs_path = self.generic_sample_dir_abs_path / filename_with_extension
        return self._post_lib_track(file_abs_path=generic_sample_abs_path, **kwargs)

    def _post_lib_track_with_generic_sample_no_tags(self,
                                                    extension: str = 'mp3',
                                                    **kwargs) -> Union[JsonResponse, HttpResponse]:
        filename_without_extension = self.LibTrackGenericSamplesFilenameWithoutExtension.TAGS_NONE
        response = self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            **kwargs)
        return response

    def _post_lib_track_with_specific_sample(self,
                                             specific_sample_filename=None,
                                             **kwargs) -> Union[JsonResponse, HttpResponse]:
        if specific_sample_filename is None:
            return self._post_lib_track(file_abs_path=None, **kwargs)
        else:
            file_abs_path = self.specific_sample_dir_abs_path / specific_sample_filename
            return self._post_lib_track(file_abs_path=file_abs_path, **kwargs)

    # Defined here and not in TrackTestCase because other views needs sometimes to post a track for testing purposes
    # (testing metadata updates for example)
    def _post_lib_track(self, file_abs_path, **kwargs) -> Union[JsonResponse, HttpResponse]:
        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {LibTrackPostFields.TRACK_FILE_PUBLIC: sample_file}
            if kwargs:
                kwargs = data_transformer.merge_two_dicts(file_field_dict, kwargs)
            else:
                kwargs = file_field_dict

            return self.api_client.post(
                path=reverse('library-track-list'),
                data=kwargs,
                format='multipart',
                handle_response=self._set_results
            )

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        super().setUp(methods_names_to_implement=methods_names_to_implement)

        self.api_client = AppApiClient(test_case=self)
        self._login_as_test_user1()

    def _post_album(self, **kwargs):
        return self.api_client.post(
            path=reverse('album-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _put_album(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('album-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )
