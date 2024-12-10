from rest_framework import status

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.schema.model.lib_track.input.put import Fields as PutFields
from bodzify_api.test.view.track.input.method.put.fields.NullableFieldTestCase import NullableFieldTestCase


class TestCase(NullableFieldTestCase):

    def test_not_provided_then_unchanged(self):
        artist = self.model_fixture_factory.create_artist(name="a-ha")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", artists=[artist])

        response = self._put_lib_track(lib_track.uuid, **{})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.artists.count() == 1
        assert self.saved_lib_track.artists.first() == artist

    def test_empty_then_none(self):
        artist_old = self.model_fixture_factory.create_artist(name="a-ha")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", artists=[artist_old])

        response = self._put_lib_track(uuid=lib_track.uuid, **{PutFields.ARTISTS_NAMES: ''})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.artists.count() == 0

    def test_one_artist_then_update(self):
        artist_old = self.model_fixture_factory.create_artist(name="a-ha")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", artists=[artist_old])
        artist_new = self.model_fixture_factory.create_artist(name="Koko")

        data = {PutFields.ARTISTS_NAMES: artist_new.name}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.artists.count() == 1
        assert self.saved_lib_track.artists.first() == artist_new

    def test_two_artists_then_update(self):
        artist_old = self.model_fixture_factory.create_artist(name="a-ha")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", artists=[artist_old])
        artist_new_1 = self.model_fixture_factory.create_artist(name="Chopin")
        artist_new_2 = self.model_fixture_factory.create_artist(name="Lopato")

        data = {PutFields.ARTISTS_NAMES: f"{artist_new_1.name}, {artist_new_2.name}"}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.artists.count() == 2
        assert self.saved_lib_track.artists.filter(name=artist_new_1.name).exists()
        assert self.saved_lib_track.artists.filter(name=artist_new_2.name).exists()
        assert not self.saved_lib_track.artists.filter(name=artist_old.name).exists()

    def test_delete_old_one_because_nothing_linked_to_it(self):
        artist_name = "a-ha"
        artist = self.model_fixture_factory.create_artist(name=artist_name)
        track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", artists=[artist])

        data = {PutFields.ARTISTS_NAMES: "Autre artiste"}
        response = self._put_lib_track(uuid=track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert not Artist.objects.filter(user=self.test_user1, name=artist_name).exists()

    def test_not_delete_old_one_because_a_track_linked_to_it(self):
        artist_name = "a-ha"
        artist = self.model_fixture_factory.create_artist(name=artist_name)
        track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="Josie", artists=[artist])

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARTISTS_NAMES: artist_name})
        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(user=self.test_user1, name=artist_name).exists()

    def test_not_delete_old_one_because_an_album_linked_to_it(self):
        artist_name = "a-ha"
        artist = self.model_fixture_factory.create_artist(name=artist_name)
        track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", artists=[artist])
        album = self.model_fixture_factory.create_album(name="Hunting High and Low", album_artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="Josie", album=album)

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARTISTS_NAMES: artist_name})

        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(user=self.test_user1, name=artist_name).exists()
