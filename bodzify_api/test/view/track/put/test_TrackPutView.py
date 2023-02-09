from rest_framework import status

from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class TrackPutViewTestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData']

    def setUp(self) -> None:
        obj= super().setUp("test/view/track/put/sample/")
        self.copySamplesToTestUserLibrary()
        return obj

    def test_libraryTrackPut(self):
        self.login(self.testUser)

        """
        - On a mp3 file.
        - Existing artist.
        - No new album. The field albumArtistsNames is thus ignored.
        - Language not specified so unchanged.
        - Genre not specified so unchanged.
        """
        data = {
            "title": "Somewhere I Belong",
            "artistName": "Linkin Park",
            "albumName": "",
            "albumArtistsNames": "Garou",
            "rating": 200,
        }
        response = self.putSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(title="Somewhere I Belong")
        assert track.artist.name == "Linkin Park"
        assert track.album_id == None
        assert track.genre.name == "Rock"
        assert track.rating == 200
        assert track.language == "Latin"

        """
        - On a FLAC file.
        - Non existing new artist.
        - Old track didn't have an album.
        - Old artist was empty.
        - Lowest rating.
        """
        data = {
            "title": "Give Me Novocain",
            "artistName": "Green Day",
            "albumName": "American Idiot",
            "albumArtistsNames": "Green Day",
            "genre": "LsjdqoifsjofsiEjf885DD",  
            "rating": 0,
            "language": "English, German"
        }
        response = self.putSampleTrack(trackUuid="36nS4LVDoihoihvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(title="Give Me Novocain")
        assert track.artist.name == "Green Day"
        assert track.album.name == "American Idiot"
        assert track.album.albumArtists.filter(name="Green Day").exists()
        assert track.genre.name == "Rock"
        assert track.rating == 0
        assert track.language == "English, German"

        """
         - On a wav file.
         - Former artist "Joni" not having any track related left. Must be deleted.
         - New artist is empty so no artist.
         - Same album's name as an existing one but with different album artists'names. Thus a new 
         album has to be created.
         - Rating isn't specified so unchanged.
         - The previous track's album hasn't anythink linked to it anymore. It must then be deleted.
        """
        data = {
            "title": "Bohemian Raphsody",
            "artistName": "",
            "albumName": "American Idiot",
            "albumArtistsNames": "Queen",
            "genre": "Lsjdqoiqsicqjsof8800",
            "language": "French"
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBcLYVHJ3A", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(title="Bohemian Raphsody")
        assert track.artist_id == None
        assert track.album.name == "American Idiot"
        assert track.album.albumArtists.filter(name="Queen").exists()
        assert Album.objects.filter(user=self.testUser, name="American Idiot").count() == 2
        assert Album.objects.filter(user=self.testUser, name="BOOM").exists() == False
        assert track.genre.name == "Nu metal"
        assert track.rating == 8
        assert track.language == "French"
        assert Artist.objects.filter(name="Joni").count() == 0

        """
        - title not specified so unchanged.
        - Max rating.
        - Weird language.
        - albumName not specified so unchanged. Thus the albumArtistsNames field is ignored.
        """
        data = {
            "artistName": "",
            "albumArtistsNames": "Queen",
            "genre": "Lsjdqoiqsicqjsof8800",
            "rating": 255,
            "language": "French12ééù12"
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBcLDDDDDS", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="dyFYZTP3anyaUBcLDDDDDS")
        assert track.title == "La Joie"
        assert track.language == "French12ééù12"
        assert track.rating == 255
