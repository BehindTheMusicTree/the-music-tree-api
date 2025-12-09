from rest_framework import status

from api.model.track.Fields import Fields as TrackFields
from api.model.track.Track import Track
from api.serializer.model.track.input.put.Fields import Fields as PutFields
from api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase, PutBodyDataTestCase):

    def test_not_provided_then_unchanged(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        track = self.model_fixture_factory.create_track_with_file(
            **{TrackFields.TITLE: "Love", TrackFields.GENRE: rap_criteria.uuid})

        response = self._put_track(track.uuid, **{PutFields.TITLE: "koko"})

        assert response.status_code == status.HTTP_200_OK
        updated_track = Track.objects.get(uuid=track.uuid)
        assert updated_track.genre == rap_criteria

    def test_ok_when_updating_to_not_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        track = self.model_fixture_factory.create_track_with_file(
            title="hoyo", use_manager_for_genre_playlist_adding=True, genre=rap_criteria)
        rock_criteria = self.model_fixture_factory.create_genre(name="Rock")

        response = self._put_track(uuid=track.uuid, **{PutFields.GENRE: rock_criteria.name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre == rock_criteria

    def test_empty_then_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        track = self.model_fixture_factory.create_track_with_file(
            title="wech", genre=rap_criteria, use_manager_for_genre_playlist_adding=True)

        response = self._put_track(uuid=track.uuid, **{PutFields.GENRE: ''})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre == None

    def test_provided_then_update(self):
        genre_name = "rap"
        track = self.model_fixture_factory.create_track_with_file(title='lolo')

        response = self._put_track(track.uuid, **{PutFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name
