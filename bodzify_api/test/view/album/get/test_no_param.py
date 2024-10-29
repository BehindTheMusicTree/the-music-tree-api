#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_get(self):
        sum41_artist = self.model_fixture_factory.create_artist(name="Sum 41")
        allkiller_album = self.model_fixture_factory.create_album(name="All Killer No Filler",
                                                                  year=2001,
                                                                  album_artists=[sum41_artist],)
        chuck_album = self.model_fixture_factory.create_album(name="Chuck", year=2004, album_artists=[sum41_artist])

        self.model_fixture_factory.create_lib_track_with_file(title="In Too Deep",
                                                              artists=[sum41_artist],
                                                              album=chuck_album)
        self.model_fixture_factory.create_lib_track_with_file(title="We're All To Blame",
                                                              artists=[sum41_artist],
                                                              album=chuck_album)
        self.model_fixture_factory.create_lib_track_with_file(title="Pieces",
                                                              artists=[sum41_artist],
                                                              album=allkiller_album)
        response = self._get_albums()
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
