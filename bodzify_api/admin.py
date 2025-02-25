from django.contrib import admin

from .model.album.Album import Album
from .model.all_lib_tracks_mixin.AllLibTracksMixin import AllLibTracksMixin
from .model.artist.Artist import Artist
from .model.criteria.Criteria import Criteria
from .model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from .model.lib_track_playlist_rel.LibTrackPlaylistRel import \
    LibTrackPlaylistRel
from .model.musicbrainz_resource.children.artist.MusicbrainzArtist import \
    MusicbrainzArtist
from .model.musicbrainz_resource.children.recording.missing_cause.code.MusicbrainzRecordingMissingCauseCode import \
    MusicbrainzRecordingMissingCauseCode
from .model.musicbrainz_resource.children.recording.missing_cause.MusicbrainzRecordingMissingCause import \
    MusicbrainzRecordingMissingCause
from .model.musicbrainz_resource.children.recording.MusicbrainzRecording import \
    MusicbrainzRecording
from .model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from .model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from .model.playlist.Playlist import Playlist
from .model.track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import \
    FingerprintMissingCauseCode
from .model.track.file.fingerprinting.missing_cause.FingerprintMissingCause import \
    FingerprintMissingCause
from .model.track.file.TrackFile import TrackFile
from .model.track.lib.LibraryTrack import LibraryTrack
from .model.user.admin.UserAdmin import UserAdmin
from .model.user.User import User

admin.site.register(User, UserAdmin)
admin.site.register(LibraryTrack)
admin.site.register(TrackFile)
admin.site.register(FingerprintMissingCause)
admin.site.register(FingerprintMissingCauseCode)
admin.site.register(AllLibTracksMixin)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Criteria)
admin.site.register(CriteriaLineageRel)
admin.site.register(Playlist)
admin.site.register(ManualPlaylist)
admin.site.register(CriteriaPlaylist)
admin.site.register(LibTrackPlaylistRel)
admin.site.register(MusicbrainzRecording)
admin.site.register(MusicbrainzRecordingMissingCause)
admin.site.register(MusicbrainzRecordingMissingCauseCode)
admin.site.register(MusicbrainzArtist)