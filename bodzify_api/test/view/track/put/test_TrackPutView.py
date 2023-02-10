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
        - A album artist is sent twice. Only one must be created.
        - A space lies at the end of the album's artists' names. It musn't be taken into account.
        """
        data = {
            "title": "Give Me Novocain",
            "artistName": "Green Day",
            "albumName": "American Idiot",
            "albumArtistsNames": "Green Day, RATM, Green Day, ",
            "genre": "LsjdqoifsjofsiEjf885DD",  
            "rating": 0,
            "language": "English, German"
        }
        response = self.putSampleTrack(trackUuid="36nS4LVDoihoihvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(title="Give Me Novocain")
        assert track.artist.name == "Green Day"
        assert track.album.name == "American Idiot"
        assert track.album.albumArtists.count() == 2
        assert track.album.albumArtists.filter(name="Green Day").exists()
        assert Artist.objects.filter(name="Green Day").count() == 1
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

        """
        - The old album shared the same name as an other one but with different artists names.
        The new album keeps the same name but puts the same artists names as the other one.
        - artist not specified so unchanged.
        """
        data = {
            "albumName": "Je Casse Tout",
            "albumArtistsNames": "Mich",
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBcSSSSSSS", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="dyFYZTP3anyaUBcSSSSSSS")
        assert track.artist.name == "Mich"
        assert Album.objects.filter(name="Je Casse Tout").count() == 1

        """
        Test 6:
        - The old track's album '1' shared the same name as another one '2' but with different 
        artists names:
            - '1' album's artists are 'A' and 'B';
            - '2' album's artists are 'A' and 'C'.
        The update puts artists 'A' and 'C' on the artists'names of the track's album. Thus:
            - Artist B must be deleted as it has no track linked anymore;
            - Artist A must have 2 tracks;
            - Album '1' must be deleted for the same reason. 
        """
        data = {
            "albumName": "Test6 - Album",
            "albumArtistsNames": "Test6 - Artist1, Test6 - Artist2",
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBc48766YH", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="dyFYZTP3anyaUBc48766YH")
        assert Album.objects.filter(name='Test6 - Album').count() == 1
        assert Album.objects.filter(uuid='Lsji85mqisjdjf88MLKJY').exists() == False
        assert LibraryTrack.objects.filter(album='Lsji85mqisjdjf881DJDHD').count() == 2
        assert Artist.objects.filter(uuid='Lsji85mqisjdjf88L98UJI').exists() == False
