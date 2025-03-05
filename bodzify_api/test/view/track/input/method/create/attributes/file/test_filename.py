from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as LibTrackPostFields
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.utils.lib_track.TestLibTrackUrl import TestLibTrackUrl
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_ok_when_max_length(self):
        response = self._post_lib_track(TestLibTrackFilename.FILENAME_150_LONG_MP3)

        assert response.status_code == status.HTTP_201_CREATED

    def test_error_when_too_long(self):
        response = self._post_lib_track(TestLibTrackFilename.FILENAME_151_MP3)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_FILENAME

    def test_title_and_one_artist_name_in_data_then_filename_with_artist_and_title(self):
        title = "ImHere"
        artist_name = "Roméo"
        data_dict = {
            LibTrackPostFields.TITLE: title,
            LibTrackPostFields.ARTISTS_NAMES_ARRAY: [artist_name],
        }
        response = self._post_lib_track_from_url(TestLibTrackUrl.MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.filename == \
            f"{artist_name} - {title}.mp3"

    def test_title_and_multiple_artists_name_in_data_then_filename_with_artist_and_title(self):
        title = "ImHere"
        artist_name1 = "Roméo"
        artist_name2 = "Juliet"
        data_dict = {
            LibTrackPostFields.TITLE: title,
            LibTrackPostFields.ARTISTS_NAMES_ARRAY: [artist_name1, artist_name2],
        }
        response = self._post_lib_track_from_url(TestLibTrackUrl.MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.filename == f"{artist_name1}, {artist_name2} - {title}.mp3"

    def test_title_and_artist_with_spaces_then_filename_with_spaces(self):
        title = " Im Here "
        artist_name = " Rom éo "
        data_dict = {
            LibTrackPostFields.TITLE: title,
            LibTrackPostFields.ARTISTS_NAMES_ARRAY: [artist_name],
        }
        response = self._post_lib_track_from_url(TestLibTrackUrl.MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.filename == f"{artist_name} - {title}.mp3"

    def test_title_and_artist_with_special_characters_then_filename_with_them(self):
        title = "I'm Here"
        artist_name = "Rom#éo"
        data_dict = {
            LibTrackPostFields.TITLE: title,
            LibTrackPostFields.ARTISTS_NAMES_ARRAY: [artist_name],
        }
        response = self._post_lib_track_from_url(TestLibTrackUrl.MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.filename == f"{artist_name} - {title}.mp3"

    def test_only_title_in_data_then_filename_with_title(self):
        title = "Hellö"
        response = self._post_lib_track_from_url(TestLibTrackUrl.MP3, **{LibTrackPostFields.TITLE: title})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.filename == f"{title}.mp3"

    def test_not_providing_title_nor_artist_and_original_filename_too_long_then_generate_filename(self):
        response = self._post_lib_track_from_url(TestLibTrackUrl.LONG_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert len(self.saved_object.track_file.filename) == \
            settings.LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH

    def test_same_filename_so_suffixe_added(self):
        self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)
        track1 = self.saved_object

        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)
        track2 = self.saved_object

        assert response.status_code == status.HTTP_201_CREATED
        assert track1.track_file
        assert track1.track_file.filename == TestLibTrackFilename.METADATA_NONE_MP3
        assert track2.track_file.filename.startswith(TestLibTrackFilename.METADATA_NONE_MP3[:-4])
        assert track2.track_file.filename.endswith('.mp3')
