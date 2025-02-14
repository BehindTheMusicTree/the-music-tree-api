from typing import Optional, Union
from uuid import UUID

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.AppApiClient import AppApiClient
from bodzify_api.utils import audio_metadata, data_transformer
from bodzify_api.model.user.User import User
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as LibTrackPostFields
from bodzify_api.serializer.schema.model.lib_track.output.detailed import Fields as LibTrackGetFields
from bodzify_api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


class ApiTestCase(AppTestCase):
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

    def _set_result(self, response):
        self.result = response.json()

    def _set_bad_request_result(self, response):
        """Store bad request result details with field-specific error information.

        Handles responses with field errors in the format:
        {
            "code": 2001,
            "message": "Bad Request",
            "success": false,
            "details": [{
                "message": "Validation failed",
                "fieldErrors": {
                    "field1": {"message": "...", "code": "..."},
                    "field2": {"message": "...", "code": "..."}
                }
            }]
        }
        """
        self.bad_request_result = response.json()
        bad_request_result_details = response.json()['details'][0]
        self.bad_request_result_field_errors_json = bad_request_result_details['fieldErrors']

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

    def _set_saved_lib_track_attribute(self, response):
        lib_track_uuid = response.json()[LibTrackGetFields.UUID]
        self.saved_lib_track = LibraryTrack.objects.get(uuid=lib_track_uuid)
        self.saved_lib_track_metadata = \
            audio_metadata.get_normalized_metadata_from_file(file=self.saved_lib_track.track_file.file)

    def _post_lib_track_with_generic_sample(self,
                                            generic_sample_filename_without_extension,
                                            generic_sample_file_extension,
                                            **kwargs) -> Union[JsonResponse, HttpResponse]:
        filename_with_extension = generic_sample_filename_without_extension + '.' + generic_sample_file_extension
        generic_sample_abs_path = self.generic_sample_dir_abs_path / filename_with_extension
        return self._post_lib_track(file_abs_path=generic_sample_abs_path, **kwargs)

    def _post_lib_track_with_generic_sample_no_tags(self,
                                                    extension: str = 'mp3',
                                                    /,
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

            # Extract any custom error handler from kwargs
            on_bad_request = kwargs.pop('on_bad_request', None)

            return self.api_client.post(
                path=reverse('library-track-list'),
                data=kwargs,
                format='multipart',
                on_success=self._set_saved_lib_track_attribute,
                on_bad_request=on_bad_request
            )

    def setUp(self, methods_names_to_implement: Optional[list[str]] = None) -> None:
        super().setUp(methods_names_to_implement=methods_names_to_implement)

        self.api_client = AppApiClient(test_case=self)
        self._login_as_test_user1()

    def _post_album(self, **kwargs):
        return self.api_client.post(path=reverse('album-list'),
                                    data=kwargs,
                                    content_type='application/x-www-form-urlencoded')

    def _put_album(self, uuid: UUID, **kwargs):
        return self.api_client.put(path=reverse('album-detail', kwargs={'pk': uuid}),
                                   data=kwargs,
                                   content_type='application/x-www-form-urlencoded')
