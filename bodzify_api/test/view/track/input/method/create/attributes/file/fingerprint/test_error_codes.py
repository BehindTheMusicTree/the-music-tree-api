#!/usr/bin/env python

import logging
from time import sleep
import docker
import docker.errors

from rest_framework import status

from bodzify_api.model.track_file.FingerprintingErrorCode import FINGERPRINTING_ERROR_CODES
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api import settings

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


class TestCase(TrackTestCase):
    def test_audio_fingerprinter_service_down_then_corresponding_error_code(self):
        stop_docker_container(settings.AUDIO_FINGERPRINTER_CONTAINER_NAME)
        response = self.post_lib_track_with_specific_sample("Y do i - Carmina Burana Remix - 7m52.mp3")
        restart_docker_container(settings.AUDIO_FINGERPRINTER_CONTAINER_NAME)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.fingerprinting_error_code.pk in [
            FINGERPRINTING_ERROR_CODES.SERVICE_NOT_FOUND, FINGERPRINTING_ERROR_CODES.UNKNOWN_CONNEXION_ERROR]

    def test_audio_fingerprinter_service_not_down_then_no_error_code(self):
        response = self.post_lib_track_with_specific_sample("Y do i - Carmina Burana Remix - 7m52.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_lib_track.track_file.fingerprinting_error_code
