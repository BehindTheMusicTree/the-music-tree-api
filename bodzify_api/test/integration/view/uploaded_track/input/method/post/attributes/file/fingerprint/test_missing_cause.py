import logging
from time import sleep

import docker
import docker.errors
import pytest
from requests.exceptions import ReadTimeout, ConnectTimeout, ConnectionError as RequestsConnectionError
from rest_framework import status
from urllib3.exceptions import ReadTimeoutError, ConnectTimeoutError

from bodzify_api import settings
from bodzify_api.model.uploaded_track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import (
    FingerprintMissingCauseCode
)
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s    %(name)s:%(filename)s:%(lineno)d %(message)s')

DOCKER_TIMEOUT = 5


def stop_docker_container(container_id_or_name):
    try:
        client = docker.from_env(timeout=DOCKER_TIMEOUT)
        container = client.containers.get(container_id_or_name)
        container.stop(timeout=DOCKER_TIMEOUT)
        logging.debug(f"Container {container_id_or_name} stopped successfully.")
    except (ReadTimeout, ReadTimeoutError, ConnectTimeout, ConnectTimeoutError, RequestsConnectionError) as e:
        error_msg = f"Failed to stop container {container_id_or_name}: Docker daemon connection timeout. Is Docker running?"
        logging.error(error_msg)
        raise ConnectionError(error_msg) from e
    except docker.errors.NotFound:
        error_msg = f"Failed to stop container {container_id_or_name}: Container not found."
        logging.error(error_msg)
        raise
    except docker.errors.APIError as e:
        error_msg = f"Failed to stop container {container_id_or_name}: Docker API error - {e}"
        logging.error(error_msg)
        raise
    except docker.errors.DockerException as e:
        error_str = str(e).lower()
        if "timeout" in error_str or "timed out" in error_str:
            error_msg = f"Failed to stop container {container_id_or_name}: Docker daemon connection timeout. Is Docker running?"
            logging.error(error_msg)
            raise ConnectionError(error_msg) from e
        error_msg = f"Failed to stop container {container_id_or_name}: Docker error - {e}"
        logging.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to stop container {container_id_or_name}: Unexpected error - {type(e).__name__}: {e}"
        logging.error(error_msg)
        raise


def restart_docker_container(container_id_or_name):
    try:
        client = docker.from_env(timeout=DOCKER_TIMEOUT)
        container = client.containers.get(container_id_or_name)
        container.start()
        sleep(5)
        logging.debug(f"Container {container_id_or_name} restarted successfully.")
        container.reload()
        status = container.status
        logging.debug(f"Container {container_id_or_name} status: {status}")
    except (ReadTimeout, ReadTimeoutError, ConnectTimeout, ConnectTimeoutError, RequestsConnectionError) as e:
        error_msg = f"Failed to restart container {container_id_or_name}: Docker daemon connection timeout. Is Docker running?"
        logging.error(error_msg)
        raise ConnectionError(error_msg) from e
    except docker.errors.NotFound:
        error_msg = f"Failed to restart container {container_id_or_name}: Container not found."
        logging.error(error_msg)
        raise
    except docker.errors.APIError as e:
        error_msg = f"Failed to restart container {container_id_or_name}: Docker API error - {e}"
        logging.error(error_msg)
        raise
    except docker.errors.DockerException as e:
        error_str = str(e).lower()
        if "timeout" in error_str or "timed out" in error_str:
            error_msg = f"Failed to restart container {container_id_or_name}: Docker daemon connection timeout. Is Docker running?"
            logging.error(error_msg)
            raise ConnectionError(error_msg) from e
        error_msg = f"Failed to restart container {container_id_or_name}: Docker error - {e}"
        logging.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to restart container {container_id_or_name}: Unexpected error - {type(e).__name__}: {e}"
        logging.error(error_msg)
        raise


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_audio_fingerprinter_service_down_then_corresponding_missing_cause(self):
        if not settings.AFP_CONTAINER_NAME:
            self.skipTest("The Audio Fingerprinter is not accessed through a Docker container.")

        stop_docker_container(settings.AFP_CONTAINER_NAME)
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3)
        restart_docker_container(settings.AFP_CONTAINER_NAME)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file and self.saved_object.track_file.fingerprint_missing_cause
        assert self.saved_object.track_file.fingerprint_missing_cause.code.code in [
            FingerprintMissingCauseCode.Codes.SERVICE_NOT_FOUND,
            FingerprintMissingCauseCode.Codes.UNKNOWN_CONNEXION_ERROR
        ]

    def test_audio_fingerprinter_service_ok_then_no_missing_cause(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_object.track_file.fingerprint_missing_cause
