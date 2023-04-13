from django.contrib import admin
from .model.playlist.CriteriaPlaylist import CriteriaPlaylist
from .model.playlist.SimplePlaylist import SimplePlaylist
from .model.track.LibraryTrack import LibraryTrack
from .model.criteria.Criteria import Criteria
from .model.criteria.CriteriaType import CriteriaType
from .model.playlist.Playlist import Playlist
from .model.playlist.PlaylistType import PlaylistType
from .model.Album import Album
from .model.Artist import Artist

admin.site.register(Criteria)
admin.site.register(CriteriaType)
admin.site.register(Playlist)
admin.site.register(SimplePlaylist)
admin.site.register(CriteriaPlaylist)
admin.site.register(PlaylistType)
admin.site.register(LibraryTrack)
admin.site.register(Album)
admin.site.register(Artist)
