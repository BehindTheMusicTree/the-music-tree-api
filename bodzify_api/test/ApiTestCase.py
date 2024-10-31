
from typing import Optional

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from django.http import JsonResponse
from django.urls import reverse

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.AppApiClient import AppApiClient
from bodzify_api.utils import audio_metadata
from bodzify_api.model.user.User import User
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.view.viewset.model.AppModelViewSet import PaginatedResponseFields
from bodzify_api.view.viewset.model.AppModelViewSet import PaginatedResponseFields
from bodzify_api.serializer.schema.track.input.endpoint.post import Fields as LibTrackPostFields
from bodzify_api.serializer.schema.track.output.detailed import Fields as LibTrackGetFields


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

    @staticmethod
    def _merge_two_dicts(dict1, dict2):
        dict1.update(dict2)
        return dict1

    @staticmethod
    def _replace_none_values_by_empty_string(data_dict):
        if data_dict is None:
            return {}
        return {k: ('' if v is None else v) for k, v in data_dict.items()}

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

    def _set_results_attributes(self, response):
        response_json = response.json()
        self.results = response_json[PaginatedResponseFields.RESULTS]
        self.overall_total = response_json[PaginatedResponseFields.OVERALL_TOTAL]

    def _set_saved_lib_track_attribute(self, response):
        lib_track_uuid = response.json()[LibTrackGetFields.UUID]
        self.saved_lib_track = LibraryTrack.objects.get(uuid=lib_track_uuid)
        self.saved_lib_track_metadata = audio_metadata.get_normalized_metadata_from_file(
            file=self.saved_lib_track.track_file.file)

    def _post_lib_track_with_generic_sample(self,
                                            generic_sample_filename_without_extension,
                                            generic_sample_file_extension,
                                            data_dict=None):
        filename_with_extension = generic_sample_filename_without_extension + '.' + generic_sample_file_extension
        generic_sample_abs_path = self.generic_sample_dir_abs_path / filename_with_extension
        return self._post_lib_track(file_abs_path=generic_sample_abs_path, data_dict=data_dict)

    def _post_lib_track_with_generic_sample_no_tags(self, extension='mp3', data_dict=None):
        filename_without_extension = self.LibTrackGenericSamplesFilenameWithoutExtension.TAGS_NONE
        response = self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            data_dict=data_dict)
        return response

    def _post_lib_track_with_specific_sample(self, specific_sample_filename=None, data_dict=None):
        if specific_sample_filename is None:
            return self._post_lib_track(file_abs_path=None, data_dict=data_dict)
        else:
            file_abs_path = self.specific_sample_dir_abs_path / specific_sample_filename
            return self._post_lib_track(file_abs_path=file_abs_path, data_dict=data_dict)

    # Defined here and not in TrackTestCase because other views needs sometimes to post a track for testing purposes
    # (testing metadata updates for example)
    def _post_lib_track(self, file_abs_path, data_dict=None) -> JsonResponse:
        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {LibTrackPostFields.FILE: sample_file}
            if data_dict:
                data_dict = self._merge_two_dicts(file_field_dict, self._replace_none_values_by_empty_string(data_dict))
            else:
                data_dict = file_field_dict
            response = self.api_client.post(path=reverse('library-track-list'), data=data_dict, format='multipart')
            if response.status_code == status.HTTP_201_CREATED:
                self._set_saved_lib_track_attribute(response)
                self._set_result(response)
            return response  # type: ignore

    def setUp(self, methods_names_to_implement: Optional[list[str]] = None) -> None:
        super().setUp(methods_names_to_implement=methods_names_to_implement)

        self.api_client = AppApiClient()
        self._login_as_test_user1()
