from rest_framework import status

from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase


class TestCase(ArtistTestCase):

    def test_with_a_track_in_an_album_with_no_other_tracks_then_delete_album(self):
        bertrand_artist = self.model_fixture_factory.create_artist(name='Bertrand')
        xavier_album = self.model_fixture_factory.create_album(name='Xavier', album_artists=[bertrand_artist])
        self.model_fixture_factory.create_lib_track_with_file(
            title="Life", artists=[bertrand_artist], album=xavier_album)
        response = self._delete_artist(bertrand_artist.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Album.objects.filter(user=self.test_user1, uuid=xavier_album.uuid).exists()

    def test_linked_to_a_track_then_delete_track(self):
        artist = self.model_fixture_factory.create_artist(name='Bertrand')
        self.model_fixture_factory.create_lib_track_with_file(title="Life", artists=[artist])
        response = self._delete_artist(artist.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Artist.objects.filter(user=self.test_user1, uuid=artist.uuid).exists()

    def test_with_a_track_and_another_artist_on_the_track_with_no_other_track_then_delete_other_artist(self):
        bertrand_artist = self.model_fixture_factory.create_artist(name='Bertrand')
        coco_artist = self.model_fixture_factory.create_artist(name='Coco')
        self.model_fixture_factory.create_lib_track_with_file(title="Life", artists=[bertrand_artist, coco_artist])
        response = self._delete_artist(bertrand_artist.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Artist.objects.filter(user=self.test_user1, uuid=coco_artist.uuid).exists()
