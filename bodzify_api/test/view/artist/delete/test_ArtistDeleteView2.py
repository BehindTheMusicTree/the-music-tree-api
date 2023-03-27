#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.test.view.artist.ArtistViewTestCase import ArtistViewTestCase
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ArtistDeleteViewTestCase2(ArtistViewTestCase):

    """
    - A track 'Life' with artist 'Bertrand' and album 'Xavier'.
    - Album 'Xavier' has album artists 'Bertrand' and 'Coco'.
    - Deleting artist 'Bertrand' should delete:
        - track 'Life';
        - album 'Xavier' as it has no track linked anymore;
        - artist 'Coco' as it has nor album nor track linked to it anymore.
    """

    def test_artistDelete2(self):
        bertrandArtist = G(Artist, user=self.testUser, name='Bertrand')
        cocoArtist = G(Artist, user=self.testUser, name='Coco')
        xavierAlbum = G(Album,
                        user=self.testUser,
                        name='Xavier',
                        albumArtists=[bertrandArtist, cocoArtist])
        lifeTrack = G(LibraryTrack,
                      user=self.testUser,
                      title="Life",
                      artist=bertrandArtist,
                      album=xavierAlbum,
                      genre=self.testUserGenrelessGenre,
                      duration=0)
        response = self._loginAndDelete(bertrandArtist.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(uuid=lifeTrack.uuid).exists() == False
        assert Album.objects.filter(uuid=xavierAlbum.uuid).exists() == False
        assert Artist.objects.filter(uuid=cocoArtist).exists() == False
