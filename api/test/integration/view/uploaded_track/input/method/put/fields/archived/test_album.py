from rest_framework import status

from api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_archived_uploaded_track_then_album_has_plus_1_archived_uploaded_tracks(self):
        album = self.model_fixture_factory.create_album(name="Jojo")
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1", album=album)
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 2", album=album)
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 3", album=album)
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 1", album=album, archived=True)
        track_love = self.model_fixture_factory.create_uploaded_track_with_file(title="Love", album=album)

        response = self._put_uploaded_track(uuid=track_love.uuid, **{PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.album and self.saved_object.album.uploaded_tracks_archived_count == 2

    def test_unarchived_then_album_has_minus_1_archived_uploaded_tracks(self):
        album = self.model_fixture_factory.create_album(name="Jojo")
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1", album=album)
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 2", album=album)
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 3", album=album)
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 1", album=album, archived=True)
        track = self.model_fixture_factory.create_uploaded_track_with_file(title="Love", album=album, archived=True)

        response = self._put_uploaded_track(uuid=track.uuid, **{PutFields.ARCHIVED: "false"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.album and self.saved_object.album.uploaded_tracks_archived_count == 1
