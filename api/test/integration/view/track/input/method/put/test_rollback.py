from unittest.mock import patch

from api.serializer.model.track.input.Fields import Fields
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_exception_then_rollback(self):
        original_genre = self.model_fixture_factory.create_genre(name="rock")
        track = self.model_fixture_factory.create_track_with_file(title="joie", genre=original_genre)
        new_genre_name = "Rock"

        with patch('api.model.track.Track.Track.save') as mock:
            exception_message = "Save failed!"
            mock.side_effect = Exception(exception_message)

            try:
                self._put_track(uuid=track.uuid, **{Fields.GENRE: new_genre_name})
            except Exception as e:
                assert str(e) == exception_message
                assert track in original_genre.tracks.all()
