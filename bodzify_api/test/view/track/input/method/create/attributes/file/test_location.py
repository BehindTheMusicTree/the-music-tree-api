#!/usr/bin/env python

from pathlib import Path
from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_in_library(self):
        filename_without_extension = self.LibTrackGenericSamplesFilenameWithoutExtension.TAGS_NONE
        file_extension = 'wav'
        filename_with_extension = f'{filename_without_extension}.{file_extension}'
        response = self.post_lib_track_with_generic_sample_no_tags(extension=file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert Path(self.lib_track_saved.track_file.file.name) == \
            self.test_user.LIBRARIES_DIR_relative_to_media_dir / filename_with_extension
        assert self.test_user.does_track_filename_exist_in_lib(filename_with_extension)
