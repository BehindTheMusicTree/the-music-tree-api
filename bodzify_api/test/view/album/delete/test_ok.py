from rest_framework import status

from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_delete_then_ok(self):
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations")
        response = self._delete_album(uuid=black_holes_album.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_2_tracks_linked_then_delete_them(self):
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations")
        assassin_track = self.model_fixture_factory.create_lib_track_with_file(
            title="Allumer le feu",
            test_lib_track_filename=LibTrackTestFilename.
            RECORDING_ALLUMERLEFEU_2_MATCHES_ONE_WITH_MORE_RELEASE_GROUPS_MP3,
            album=black_holes_album)

        starlight_track = self.model_fixture_factory.create_lib_track_with_file(
            title="Starlight",
            test_lib_track_filename=LibTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3,
            album=black_holes_album)

        assert self.test_user1.does_track_filename_exist_in_lib(
            LibTrackTestFilename.RECORDING_ALLUMERLEFEU_2_MATCHES_ONE_WITH_MORE_RELEASE_GROUPS_MP3)
        assert self.test_user1.does_track_filename_exist_in_lib(LibTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3)

        response = self._delete_album(uuid=black_holes_album.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Album.objects.filter(user=self.test_user2, uuid=black_holes_album.uuid).exists()
        assert not LibraryTrack.objects.filter(user=self.test_user2, title=assassin_track.title).exists()
        assert not LibraryTrack.objects.filter(user=self.test_user2, title=starlight_track.title).exists()
        assert not self.test_user1.does_track_filename_exist_in_lib(
            LibTrackTestFilename.RECORDING_ALLUMERLEFEU_2_MATCHES_ONE_WITH_MORE_RELEASE_GROUPS_MP3)
        assert not self.test_user1.does_track_filename_exist_in_lib(LibTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3)

    def test_delete_then_delete_track_artist_as_nothing_linked_to_it_anymore(self):
        muse_artist = self.model_fixture_factory.create_artist(name="Muse")
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations")
        self.model_fixture_factory.create_lib_track_with_file(
            title="Assassin", artists=[muse_artist], album=black_holes_album)

        response = self._delete_album(uuid=black_holes_album.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Artist.objects.filter(user=self.test_user1, name=muse_artist.name).exists()

    def test_delete_then_dont_delete_track_artist_as_tracks_still_linked_to_it(self):
        muse_artist = self.model_fixture_factory.create_artist(name="Muse")
        album = self.model_fixture_factory.create_album(name="Black Holes And Revelations")
        self.model_fixture_factory.create_lib_track_with_file(
            title="Assassin", artists=[muse_artist], album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="Supermassive Black Hole", artists=[muse_artist])

        response = self._delete_album(uuid=album.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Artist.objects.filter(user=self.test_user1, name=muse_artist.name).exists()

    def test_delete_then_delete_album_artist_as_tracks_nothing_linked_to_it_anymore(self):
        matthew_artist = self.model_fixture_factory.create_artist(name="Matthew Bellamy")
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations",
                                                                    album_artists=[matthew_artist])
        response = self._delete_album(uuid=black_holes_album.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Artist.objects.filter(user=self.test_user1, name=matthew_artist.name).exists()

    def test_delete_then_dont_delete_album_artist_as_tracks_still_linked_to_it(self):
        matthew_artist = self.model_fixture_factory.create_artist(name="Matthew Bellamy")
        black_holes_album = self.model_fixture_factory.create_album(name="Black Holes And Revelations",
                                                                    album_artists=[matthew_artist])
        self.model_fixture_factory.create_lib_track_with_file(title="Supermassive Black Hole",
                                                              artists=[matthew_artist])
        response = self._delete_album(uuid=black_holes_album.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Artist.objects.filter(user=self.test_user1, name=matthew_artist.name).exists()
