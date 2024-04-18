from django.contrib import admin
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.playlist.Playlist import Playlist
from .model.playlist.children.SimplePlaylist import SimplePlaylist
from .model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from .model.track.LibraryTrack import LibraryTrack
from .model.criteria.Criteria import Criteria
from .model.criteria.CriteriaType import CriteriaType
from .model.Album import Album
from .model.Artist import Artist

admin.site.register(Criteria)
admin.site.register(CriteriaType)
admin.site.register(Playlist)
admin.site.register(PlaylistLibTrackRelation)
admin.site.register(SimplePlaylist)
admin.site.register(CriteriaPlaylist)
admin.site.register(LibraryTrack)
admin.site.register(Album)
admin.site.register(Artist)
