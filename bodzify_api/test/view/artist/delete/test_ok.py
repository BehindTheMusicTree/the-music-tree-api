#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.test.view.artist.ArtistViewTestCase import ArtistViewTestCase
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ArtistViewDeleteTestCase(ArtistViewTestCase):

    def test_with_one_track_linked(self):
        muse_artist = G(Artist, name="Muse", user=self.test_user)
        assassin_track = G(LibraryTrack, user=self.test_user, title="Assassin", artist=muse_artist)

        response = self._delete(artistUuid=muse_artist.uuid)  # type: ignore

        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert Artist.objects.filter(uuid=muse_artist.uuid).exists() == False  # type: ignore
        assert LibraryTrack.objects.filter(uuid=assassin_track.uuid).exists() == False  # type: ignore

    """
    - A track 'Life' with artist 'Bertrand' and album 'Xavier'.
    - Album 'Xavier' has album artists 'Bertrand' and 'Coco'.
    - Deleting artist 'Bertrand' should delete:
        - track 'Life';
        - album 'Xavier' as it has no track linked anymore;
        - artist 'Coco' as it has nor album nor track linked to it anymore.
    """

    def test_with_album_and_album_artist_deletion(self):
        bertrand_artist = G(Artist, user=self.test_user, name='Bertrand')
        coco_artist = G(Artist, user=self.test_user, name='Coco')
        xavier_album = G(Album, user=self.test_user, name='Xavier', album_artists=[bertrand_artist, coco_artist])
        life_track = G(LibraryTrack, user=self.test_user, title="Life", artist=bertrand_artist, album=xavier_album)

        response = self._delete(bertrand_artist.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert LibraryTrack.objects.filter(uuid=life_track.uuid).exists() == False  # type: ignore
        assert Album.objects.filter(uuid=xavier_album.uuid).exists() == False  # type: ignore
        assert Artist.objects.filter(uuid=coco_artist).exists() == False
