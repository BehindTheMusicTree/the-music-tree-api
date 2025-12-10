from django.contrib import admin

from .model.album.Album import Album
from .model.all_tracks_mixin.AllTracksMixin import AllTracksMixin
from .model.artist.Artist import Artist
from .model.criteria.Criteria import Criteria
from .model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from .model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
from .model.musicbrainz_resource.children.artist.MbArtist import MbArtist
from .model.musicbrainz_resource.children.recording.MbRecording import MusicbrainzRecording
from .model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)
from .model.musicbrainz_resource.children.recording.missing_cause.MbRecordingMissingCause import MbRecordingMissingCause
from .model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from .model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from .model.playlist.Playlist import Playlist
from .model.track.Track import Track
from .model.user.admin.UserAdmin import UserAdmin
from .model.user.User import User
from .model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from .model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist


admin.site.register(User, UserAdmin)
admin.site.register(Track)
admin.site.register(AllTracksMixin)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Criteria)
admin.site.register(CriteriaLineageRel)
admin.site.register(Playlist)
admin.site.register(ManualPlaylist)
admin.site.register(CriteriaPlaylist)
admin.site.register(TrackPlaylistRel)
admin.site.register(MusicbrainzRecording)
admin.site.register(MbRecordingMissingCause)
admin.site.register(MbRecordingMissingCauseCode)
admin.site.register(MbArtist)
admin.site.register(SpotifyLibTrack)
admin.site.register(SpotifyArtist)
