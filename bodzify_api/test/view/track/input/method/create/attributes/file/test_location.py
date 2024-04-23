#!/usr/bin/env python

from pathlib import Path
from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_inLibrary(self):
        filename = self.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_NONE
        file_extension = 'wav'
        filename_with_underscores_and_extension = filename.replace(' ', '_') + '.' + file_extension
        response = self.post_lib_track_with_generic_sample_no_tags(extension=file_extension)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert Path(self.saved_lib_track.file_obj.name) == \
            self.test_user_lib_path_relative_to_media_dir / filename_with_underscores_and_extension
        assert self._does_track_filename_exist_in_test_user_lib(filename_with_underscores_and_extension)
