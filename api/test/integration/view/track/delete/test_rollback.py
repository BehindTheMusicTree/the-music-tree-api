from unittest.mock import patch

from api.model.track.Track import Track
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_exception_then_rollback(self):
        album = self.model_fixture_factory.create_album(name="album")
        track = self.model_fixture_factory.create_track_with_file(title="joie", album=album)

        with patch('api.model.album.Album.Album.save') as mock:
            exception_message = "Save failed!"
            mock.side_effect = Exception(exception_message)

            try:
                self._delete_track(uuid=track.uuid)
            except Exception as e:
                assert str(e) == exception_message
                assert Track.objects.filter(uuid=track.uuid).exists()
