
from unittest.mock import patch

from django.db import IntegrityError
from django.test import override_settings
from rest_framework import status

from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.view.error.ApiErrorCode import ApiErrorCodeNumeric


class TestCase(UploadedTrackTestCase):

    @override_settings(DEBUG=False)
    def test_internal_error_then_500_with_response_error_code(self):
        with patch('api.model.uploaded_track.UploadedTrack.UploadedTrack.save') as mock:
            exception_message = "DB Integrity Error"
            mock.side_effect = IntegrityError(exception_message)

            results = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, title='test')
            assert results.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            json = results.json()
            assert json['code'] == ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR
