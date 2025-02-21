import logging
from time import sleep

import docker
import docker.errors
import pytest
from rest_framework import status

from bodzify_api import settings
from bodzify_api.model.track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode \
    import FingerprintMissingCauseCode
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s    %(name)s:%(filename)s:%(lineno)d %(message)s')


def stop_docker_container(container_id_or_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id_or_name)
        container.stop()
        logging.debug(f"Container {container_id_or_name} stopped successfully.")
    except docker.errors.NotFound:
        logging.debug(f"Container {container_id_or_name} not found.")
    except Exception as e:
        logging.error(f"Error stopping container {container_id_or_name}: {e}")


def restart_docker_container(container_id_or_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id_or_name)
        container.start()
        sleep(5)  # Wait for the container to restart
        logging.debug(f"Container {container_id_or_name} restarted successfully.")
        container.reload()  # Refresh the container's attributes
        status = container.status
        logging.debug(f"Container {container_id_or_name} status: {status}")
    except docker.errors.NotFound:
        logging.debug(f"Container {container_id_or_name} not found.")
    except Exception as e:
        logging.error(f"Error restarting container {container_id_or_name}: {e}")


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_audio_meta_analysis_not_enabled_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_queenshowmustgoon()

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file and self.saved_object.track_file.fingerprint_missing_cause
        assert self.saved_object.track_file.fingerprint_missing_cause.code.code == \
            FingerprintMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED

    def test_audio_fingerprinter_service_down_then_corresponding_missing_cause(self):
        if not settings.AFP_CONTAINER_NAME:
            self.skipTest("The Audio Fingerprinter is not accessed through a Docker container.")

        stop_docker_container(settings.AFP_CONTAINER_NAME)
        response = self._post_lib_track_with_queenshowmustgoon()
        restart_docker_container(settings.AFP_CONTAINER_NAME)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file and self.saved_object.track_file.fingerprint_missing_cause
        assert self.saved_object.track_file.fingerprint_missing_cause.code.code in [
            FingerprintMissingCauseCode.Codes.SERVICE_NOT_FOUND,
            FingerprintMissingCauseCode.Codes.UNKNOWN_CONNEXION_ERROR
        ]

    def test_audio_fingerprinter_service_ok_then_no_missing_cause(self):
        response = self._post_lib_track_with_queenshowmustgoon()

        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_object.track_file.fingerprint_missing_cause
