
from django.contrib import admin

from bodzify_api.model.user.UserAdmin import UserAdmin
from .model.user.User import User

from bodzify_api.model.album.Album import Album
from bodzify_api.model.AllLibTrackMixin import AllLibTrackMixin
from bodzify_api.model.Artist import Artist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaAscendantRel import CriteriaAscendantRel
from bodzify_api.model.criteria.CriteriaType import CriteriaType
from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist
from bodzify_api.model.musicbrainz.recording.MusicbrainzRecording import MusicbrainzRecording
from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCause \
    import MusicbrainzRecordingMissingCause
from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.ManualPlaylist import ManualPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause
from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCauseCode \
    import FingerprintMissingCauseCode
from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.model.user.User import User


admin.site.register(User, UserAdmin)
admin.site.register(LibraryTrack)
admin.site.register(TrackFile)
admin.site.register(FingerprintMissingCause)
admin.site.register(FingerprintMissingCauseCode)
admin.site.register(AllLibTrackMixin)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Criteria)
admin.site.register(CriteriaAscendantRel)
admin.site.register(CriteriaType)
admin.site.register(BasePlaylist)
admin.site.register(LibTrackPlaylistPositionRel)
admin.site.register(ManualPlaylist)
admin.site.register(CriteriaPlaylist)
admin.site.register(MusicbrainzRecording)
admin.site.register(MusicbrainzRecordingMissingCause)
admin.site.register(MusicbrainzRecordingMissingCauseCode)
admin.site.register(MusicbrainzArtist)
