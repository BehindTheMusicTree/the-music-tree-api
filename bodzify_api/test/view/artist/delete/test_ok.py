#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.artist.ArtistViewTestCase import ArtistViewTestCase


class ArtistViewDeleteTestCase(ArtistViewTestCase):

    def test_with_a_track_in_an_album_with_no_other_tracks_then_delete_it(self):
        bertrand_artist = self.model_fixture_factory.create_artist(name='Bertrand')
        xavier_album = self.model_fixture_factory.create_album(name='Xavier', album_artists=[bertrand_artist])
        self.model_fixture_factory.create_lib_track(
            title="Life", artists=[bertrand_artist], album=xavier_album)
        response = self._delete(bertrand_artist.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(uuid=xavier_album.uuid).exists() == False

    def test_linked_to_a_track_then_delete_it(self):
        bertrand_artist = self.model_fixture_factory.create_artist(name='Bertrand')
        coco_artist = self.model_fixture_factory.create_artist(name='Coco')
        self.model_fixture_factory.create_lib_track(title="Life", artists=[bertrand_artist])
        response = self._delete(bertrand_artist.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Artist.objects.filter(uuid=coco_artist).exists() == False

    def test_with_a_track_and_another_artist_on_the_track_with_no_other_ones_then_delete_other_artist(self):
        bertrand_artist = self.model_fixture_factory.create_artist(name='Bertrand')
        coco_artist = self.model_fixture_factory.create_artist(name='Coco')
        self.model_fixture_factory.create_lib_track(title="Life", artists=[bertrand_artist])
        response = self._delete(bertrand_artist.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Artist.objects.filter(uuid=coco_artist).exists() == False
