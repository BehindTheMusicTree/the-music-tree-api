import shutil
import time
from pathlib import Path

import pytest

from api import settings
from api.model.uploaded_track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import FingerprintMissingCauseCode
from api.test.utils.AppTestCase import AppTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.utils.audio_fingerprinter import utils as audio_fingerprinter_utils


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(AppTestCase):

    @pytest.mark.critical
    def test_audio_fingerprinter_connection_ok(self):
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                print(f"test_audio_fingerprinter_connection_ok (attempt {attempt + 1}/{max_retries})")
                file_abs_path = self.TEST_FILES_BASE_DIR / UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3.value
                filename = file_abs_path.name

                pool_dir = Path(settings.FILE_UPLOAD_TEMP_DIR)
                pool_file_path = pool_dir / filename

                shutil.copy2(file_abs_path, pool_file_path)

                try:
                    fingerprint, duration_in_sec = audio_fingerprinter_utils.post_fingerprint_audio(
                        filename=filename, title="Test Track", user_id=str(self.test_user1.pk))

                    assert fingerprint is not None
                    assert duration_in_sec is not None
                    return
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"Error: {e}")
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    raise
                finally:
                    if pool_file_path.exists():
                        pool_file_path.unlink()
            except AssertionError:
                if attempt < max_retries - 1:
                    print(f"Test failed, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                raise
