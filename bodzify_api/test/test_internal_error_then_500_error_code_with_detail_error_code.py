
from unittest.mock import patch

from django.db import IntegrityError
from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.view.error.ApiErrorCode import ApiErrorCode


class TestCase(LibTrackTestCase):

    def test_internal_error_then_500_with_response_error_code(self):
        with patch('bodzify_api.model.track.lib.LibraryTrack.LibraryTrack.save') as mock:
            exception_message = "DB Integrity Error"
            mock.side_effect = IntegrityError(exception_message)

            results = self._post_lib_track_with_generic_sample_no_tags(title='test')
            assert results.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            json = results.json()
            assert json['code'] == ApiErrorCode.SYSTEM_INTERNAL_ERROR
