from rest_framework import status

from bodzify_api.model.uploaded_track.Fields import Fields as UploadedTrackFields
from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase, PutBodyDataTestCase):

    def test_not_provided_then_unchanged(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            **{UploadedTrackFields.TITLE: "Love", UploadedTrackFields.GENRE: rap_criteria.uuid})

        response = self._put_uploaded_track(uploaded_track.uuid, **{PutFields.TITLE: "koko"})

        assert response.status_code == status.HTTP_200_OK
        updated_uploaded_track = UploadedTrack.objects.get(uuid=uploaded_track.uuid)
        assert updated_uploaded_track.genre == rap_criteria

    def test_ok_when_updating_to_not_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="hoyo", use_manager_for_genre_playlist_adding=True, genre=rap_criteria)
        rock_criteria = self.model_fixture_factory.create_genre(name="Rock")

        response = self._put_uploaded_track(uuid=uploaded_track.uuid, **{PutFields.GENRE: rock_criteria.name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre == rock_criteria

    def test_empty_then_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="wech", genre=rap_criteria, use_manager_for_genre_playlist_adding=True)

        response = self._put_uploaded_track(uuid=uploaded_track.uuid, **{PutFields.GENRE: ''})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre == None

    def test_provided_then_update(self):
        genre_name = "rap"
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title='lolo')

        response = self._put_uploaded_track(uploaded_track.uuid, **{PutFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name
