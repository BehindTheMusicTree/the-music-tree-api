
from unittest.mock import patch

from django.db import IntegrityError
from django.test import override_settings
from rest_framework import status

from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.view.error.ApiErrorCode import ApiErrorCodeNumeric


class TestCase(LibTrackTestCase):

    @override_settings(DEBUG=False)
    def test_internal_error_then_500_with_response_error_code(self):
        with patch('bodzify_api.model.track.lib.LibraryTrack.LibraryTrack.save') as mock:
            exception_message = "DB Integrity Error"
            mock.side_effect = IntegrityError(exception_message)

            results = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, title='test')
            assert results.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            json = results.json()
            assert json['code'] == ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR
