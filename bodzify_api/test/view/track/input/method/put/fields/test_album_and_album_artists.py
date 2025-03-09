from rest_framework import status

from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.model.lib_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, PutBodyDataTestCase):

    def test_not_provided_then_unchanged(self):
        album = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", album=album)

        response = self._put_lib_track(lib_track.uuid, **{})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.album == album

    def test_empty_then_none(self):
        album_old = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", album=album_old)

        data = {PutFields.ALBUM_NAME: '', PutFields.ALBUM_ARTISTS_NAMES_ARRAY: []}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.album == None

    def test_provided_then_update(self):
        album_artist_new = self.model_fixture_factory.create_artist(name="James")
        album_old = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", album=album_old)
        album_artist_new = self.model_fixture_factory.create_artist(name="Harden")
        album_new = self.model_fixture_factory.create_album(name="koko", album_artists=[album_artist_new])

        data = {PutFields.ALBUM_NAME: album_new.name, PutFields.ALBUM_ARTISTS_NAMES_ARRAY: [album_artist_new.name]}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.album == album_new
        assert self.saved_object.album.album_artists.count() == 1
        assert self.saved_object.album.album_artists.first() == album_artist_new

    def test_provided_with_multiple_artists_then_update(self):
        album_old = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", album=album_old)
        album_new_name = "koko"
        album_artist_new_1 = self.model_fixture_factory.create_artist(name="James")
        album_artist_new_2 = self.model_fixture_factory.create_artist(name="Koko")

        data = {PutFields.ALBUM_NAME: album_new_name,
                PutFields.ALBUM_ARTISTS_NAMES_ARRAY: [album_artist_new_1.name, album_artist_new_2.name]}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.album.name == album_new_name
        assert self.saved_object.album.album_artists.count() == 2
        assert self.saved_object.album.album_artists.filter(name=album_artist_new_1.name).exists()
        assert self.saved_object.album.album_artists.filter(name=album_artist_new_2.name).exists()

    def test_nothing_linked_to_old_album_anymore_then_delete_it(self):
        old_album_artist = self.model_fixture_factory.create_artist(name="a-ha")
        old_album = self.model_fixture_factory.create_album(name="Le Noir", album_artists=[old_album_artist])
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", album=old_album)

        data = {PutFields.ALBUM_NAME: "Paul", PutFields.ALBUM_ARTISTS_NAMES_ARRAY: ["James"]}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert not Album.objects.filter(user=self.test_user1, uuid=old_album.uuid).exists()

    def test_nothing_linked_to_old_album_artist_anymore_then_delete_it(self):
        old_album_artist = self.model_fixture_factory.create_artist(name="a-ha")
        old_album = self.model_fixture_factory.create_album(name="Le Noir", album_artists=[old_album_artist])
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", album=old_album)

        data = {PutFields.ALBUM_NAME: "Paul", PutFields.ALBUM_ARTISTS_NAMES_ARRAY: ["James"]}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert not Artist.objects.filter(user=self.test_user1, uuid=old_album_artist.uuid).exists()

    def test_a_track_still_linked_to_old_album_then_not_delete_it(self):
        album_name = "La Saucisse"
        album = self.model_fixture_factory.create_album(name=album_name)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="Josie", album=album)

        data = {PutFields.ALBUM_NAME: "Paul", PutFields.ALBUM_ARTISTS_NAMES_ARRAY: ["James"]}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.filter(user=self.test_user1, name=album_name).exists()

    def test_delete_old_album_artist_because_nothing_linked_to_it(self):
        album_artist_name = "a-ha"
        album_artist = self.model_fixture_factory.create_artist(name=album_artist_name)
        album = self.model_fixture_factory.create_album(name="Jojo", album_artists=[album_artist])
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", album=album)

        data = {PutFields.ALBUM_ARTISTS_NAMES_ARRAY: ["Other artist"]}
        response = self._put_lib_track(uuid=lib_track.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert not Artist.objects.filter(user=self.test_user1, name=album_artist_name).exists()

    def test_not_delete_old_album_artist_because_a_track_linked_to_it(self):
        album_artist_name = "a-ha"
        album_artist = self.model_fixture_factory.create_artist(name=album_artist_name)
        album = self.model_fixture_factory.create_album(name="Jojo", album_artists=[album_artist])
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="Josie", album=album)

        response = self._put_lib_track(
            uuid=lib_track.uuid, **{PutFields.ALBUM_ARTISTS_NAMES_ARRAY: [album_artist_name]})
        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(user=self.test_user1, name=album_artist_name).exists()

    def test_not_delete_old_album_artist_because_annother_album_with_a_track_linked_to_it(self):
        album_artist_name = "a-ha"
        album_artist = self.model_fixture_factory.create_artist(name=album_artist_name)
        album = self.model_fixture_factory.create_album(name="Jojo", album_artists=[album_artist])
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", album=album)
        album2 = self.model_fixture_factory.create_album(name="Jojo2", album_artists=[album_artist])
        self.model_fixture_factory.create_lib_track_with_file(title="Josie", album=album2)

        response = self._put_lib_track(uuid=lib_track.uuid, **{PutFields.ALBUM_ARTISTS_NAMES_ARRAY: ["Other artist"]})
        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(user=self.test_user1, name=album_artist_name).exists()

    def test_old_album_artist_linked_to_another_album_with_a_track_then_not_delete_it(self):
        album_artist_name = "a-ha"
        album_artist = self.model_fixture_factory.create_artist(name=album_artist_name)
        album = self.model_fixture_factory.create_album(name="Jojo", album_artists=[album_artist])
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", album=album)
        album2 = self.model_fixture_factory.create_album(name="Jojo2", album_artists=[album_artist])
        self.model_fixture_factory.create_lib_track_with_file(title="Josie", album=album2)

        response = self._put_lib_track(uuid=lib_track.uuid, **{PutFields.ALBUM_ARTISTS_NAMES_ARRAY: ["Other artist"]})
        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(user=self.test_user1, name=album_artist_name).exists()
