#!/usr/bin/env python

from pathlib import Path
import pytest
from rest_framework import status
from bodzify_api.model.File import File
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_file_deletion(self):
        filename = "sample.mp3"
        file_path_relative_to_media_dir = self.test_user.lib_path_relative_to_media_dir / filename
        file_obj = self.model_fixture_factory.create_file(file_path=Path(file_path_relative_to_media_dir))
        track = self.model_fixture_factory.create_lib_track(file_obj=file_obj, title="We're All To Blame")
        assert self.test_user.does_track_filename_exist_in_lib(filename) == True
        assert track.file_obj.file
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(uuid=track.uuid).exists() == False
        assert self.test_user.does_track_filename_exist_in_lib(filename) == False

    def test_when_no_file_linked(self):
        track_title = "We"
        track = self.model_fixture_factory.create_lib_track(title=track_title)
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(title=track_title).exists() == False
