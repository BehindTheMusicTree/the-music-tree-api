from django.contrib import admin

from .model.track.LibraryTrack import LibraryTrack
from .model.criteria.Criteria import Criteria
from .model.playlist.Playlist import Playlist

admin.site.register(LibraryTrack)
admin.site.register(Criteria)
admin.site.register(Playlist)
