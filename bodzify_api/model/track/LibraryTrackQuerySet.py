from django.db.models.query import QuerySet

class LibraryTrackQuerySet(QuerySet):
    def update(self, *args, **kwargs):
        oldGenre = self.genre
        oldArtist = self.artist
        oldAlbum = self.album
        super().update(*args, **kwargs)

        if oldGenre != self.genre:
            self.updatePlaylists(oldGenre=oldGenre)
        if oldAlbum != self.album and oldAlbum != None:
            oldAlbum.deleteIfNoTrackLinked()

        if oldArtist != self.artist and oldArtist != None:
            oldArtist.deleteIfNothingLinked()