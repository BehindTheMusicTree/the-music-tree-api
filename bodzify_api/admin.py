from django.contrib import admin

from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.criteria.CriteriaAscendantRelation import CriteriaAscendantRelation
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaType
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.File import File

admin.site.register(Criteria)
admin.site.register(CriteriaAscendantRelation)
admin.site.register(CriteriaType)
admin.site.register(Playlist)
admin.site.register(PlaylistLibTrackRelation)
admin.site.register(SimplePlaylist)
admin.site.register(CriteriaPlaylist)
admin.site.register(LibraryTrack)
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(File)
