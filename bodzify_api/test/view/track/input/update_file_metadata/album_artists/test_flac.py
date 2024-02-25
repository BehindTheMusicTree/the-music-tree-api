#!/usr/bin/env python

from bodzify_api.test.view.track.input.update_file_metadata.album_artists.UpdateFileMetadataAlbumArtistTestCase \
    import UpdateFileMetadataAlbumArtistTestCase


class TestCase(UpdateFileMetadataAlbumArtistTestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(file_extension='flac', methodName=methodName)
