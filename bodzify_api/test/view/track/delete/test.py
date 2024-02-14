#!/usr/bin/env python
import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


@pytest.mark.django_db
class TrackDeleteViewTestCase(ApiViewTestCase):

    def test_fileDeletion(self):
        filename = "sample.mp3"
        filePathRelativeToMediaDir = self.test_user_library_path_relative_to_media_dir / filename
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=filePathRelativeToMediaDir,
                  title="We're All To Blame",
                  duration=0)
        assert self.doesTrackFilenameExistInTestUserLibrary(filename) == True
        assert track.fileExists == True
        response = self.delete_track(track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(uuid=track.uuid).exists() == False
        assert self.doesTrackFilenameExistInTestUserLibrary(filename) == False

    def test_linkedAlbumAndArtistDeletionAsNothingLinkedToItAnymore(self):
        album_name = "Chuck"
        album = G(Album, user=self.test_user, name=album_name)
        artist_name = "Sum 41"
        artist = G(Artist, user=self.test_user, name=artist_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="We're All To Blame",
                  artist=artist,
                  album=album,
                  duration=0)
        response = self.delete_track(track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(
            user=self.test_user, name=album_name).exists() == False
        assert Artist.objects.filter(
            user=self.test_user, name=artist_name).exists() == False

    def test_whenNoFileLinked(self):
        trackTitle = "We"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title=trackTitle,
                  duration=0)
        response = self.delete_track(track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(
            user=self.test_user, title=trackTitle).exists() == False
        
    def test_removalFromTheAllPlaylist(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="We're All To Blame",
                  duration=0)
        allPlaylist = SimplePlaylist.objects.get(user=self.test_user, name=PLAYLIST_SPECIAL_NAMES.ALL)
        assert track in allPlaylist.librarytrack_set.all()
        response = self.delete_track(track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert track not in allPlaylist.librarytrack_set.all()
        
    def test_removalFromTheGenrePlaylists(self):        
        rock_genre_name = "Rock"
        hardrock_genre_name = "Hard rock"
        emo_genre_name = "Emo"

        data_json = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: rock_genre_name
        }
        self.post_genre(data_json)
        rock_genre = self.saved_genre
        rockPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user, type=CriteriaTypesId.GENRE, criteria=rock_genre)

        data_json = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: hardrock_genre_name,
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock_genre.uuid
        }
        self.post_genre(data_json)
        hardrock_genre = self.saved_genre
        hardrockPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user, type=CriteriaTypesId.GENRE, criteria=hardrock_genre)

        data_json = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: emo_genre_name,
            CRITERIA_ATTRIBUTES_LABEL.PARENT: hardrock_genre.uuid
        }
        self.post_genre(data_json)
        emoGenre = self.saved_genre
        emoPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user, type=CriteriaTypesId.GENRE, criteria=emoGenre)

        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0,
                  genre=emoGenre)
        
        assert track in emoPlaylist.librarytrack_set.all()
        assert track in hardrockPlaylist.librarytrack_set.all()
        assert track in rockPlaylist.librarytrack_set.all()
        
        response = self.delete_track(track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        assert track not in emoPlaylist.librarytrack_set.all()
        assert track not in hardrockPlaylist.librarytrack_set.all()
        assert track not in rockPlaylist.librarytrack_set.all()
        
        
