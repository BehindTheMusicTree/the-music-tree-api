from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.lib_track.input.put.Fields import Fields as PutFields
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from bodzify_api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, PutBodyDataTestCase):

    def test_not_provided_then_unchanged(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            **{LibTrackFields.TITLE: "Love", LibTrackFields.GENRE: rap_criteria.uuid})

        response = self._put_lib_track(lib_track.uuid, **{})

        assert response.status_code == status.HTTP_200_OK
        updated_lib_track = LibraryTrack.objects.get(uuid=lib_track.uuid)
        assert updated_lib_track.genre == rap_criteria

    def test_ok_when_updating_to_not_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            **{LibTrackFields.TITLE: "koko", LibTrackFields.GENRE: rap_criteria.uuid})
        rock_criteria = self.model_fixture_factory.create_genre(name="Rock")

        data = {PutFields.GENRE_NAME: rock_criteria.name}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre == rock_criteria

    def test_empty_then_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            **{LibTrackFields.TITLE: "koko", LibTrackFields.GENRE: rap_criteria.uuid})

        response = self._put_lib_track(uuid=lib_track.uuid, **{PutFields.GENRE_NAME: ''})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre == None

    def test_provided_then_update(self):
        genre_name = "rap"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title='lolo')

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: genre_name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name
