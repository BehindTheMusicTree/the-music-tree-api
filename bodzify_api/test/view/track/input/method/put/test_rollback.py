from unittest.mock import patch

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.serializer.schema.model.lib_track.input.Fields import Fields


class TestCase(LibTrackTestCase):

    def test_exception_then_rollback(self):
        original_genre = self.model_fixture_factory.create_genre(name="rock")
        track = self.model_fixture_factory.create_lib_track_with_file(
            title="joie", genre=original_genre)
        new_genre_name = "Rock"
        with patch('bodzify_api.model.track.lib.LibraryTrack.LibraryTrack.save') as mock:
            exception_message = "Save failed!"
            mock.side_effect = Exception(exception_message)

            try:
                self._put_lib_track(uuid=track.uuid, **{Fields.GENRE_NAME: new_genre_name})
            except Exception as e:
                assert str(e) == exception_message
                assert track in original_genre.lib_tracks.all()
