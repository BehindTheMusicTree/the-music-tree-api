from django.contrib import admin

from .model.user.admin.UserAdmin import UserAdmin
from .model.user.User import User
from .model.album.Album import Album
from .model.criteria.Criteria import Criteria
from .model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from .model.all_lib_track_mixin.AllLibTrackMixin import AllLibTrackMixin
from .model.artist.Artist import Artist
from .model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from .model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist
from .model.musicbrainz.recording.MusicbrainzRecording import MusicbrainzRecording
from .model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCause import MusicbrainzRecordingMissingCause
from .model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode
from .model.playlist.BasePlaylist import BasePlaylist
from .model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from .model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from .model.track.lib.LibraryTrack import LibraryTrack
from .model.track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause
from .model.track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import FingerprintMissingCauseCode
from .model.track.file.TrackFile import TrackFile
from .model.user.User import User

admin.site.register(User, UserAdmin)
admin.site.register(LibraryTrack)
admin.site.register(TrackFile)
admin.site.register(FingerprintMissingCause)
admin.site.register(FingerprintMissingCauseCode)
admin.site.register(AllLibTrackMixin)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Criteria)
admin.site.register(CriteriaLineageRel)
admin.site.register(BasePlaylist)
admin.site.register(ManualPlaylist)
admin.site.register(CriteriaPlaylist)
admin.site.register(LibTrackPlaylistPositionRel)
admin.site.register(MusicbrainzRecording)
admin.site.register(MusicbrainzRecordingMissingCause)
admin.site.register(MusicbrainzRecordingMissingCauseCode)
admin.site.register(MusicbrainzArtist)
