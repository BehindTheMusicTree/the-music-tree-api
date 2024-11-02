from django.contrib import admin


from .model.user.UserAdmin import UserAdmin
from .model.user.User import User
from .model.album.Album import Album
from .model.criteria.Genre import Genre
from .model.criteria.Tag import Tag
from .model.playlist.children.criteria.children.GenrePlaylist import GenrePlaylist
from .model.playlist.children.criteria.children.TagPlaylist import TagPlaylist
from .model.AllLibTrackMixin import AllLibTrackMixin
from .model.artist.Artist import Artist
from .model.criteria.CriteriaAscendantRel import CriteriaAscendantRel
from .model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from .model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist
from .model.musicbrainz.recording.MusicbrainzRecording import MusicbrainzRecording
from .model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCause import MusicbrainzRecordingMissingCause
from .model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode
from .model.playlist.BasePlaylist import BasePlaylist
from .model.playlist.children.ManualPlaylist import ManualPlaylist
from .model.track.lib.LibraryTrack import LibraryTrack
from .model.track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause
from .model.track.file.fingerprinting.missing_cause.FingerprintMissingCauseCode import FingerprintMissingCauseCode
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
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(CriteriaAscendantRel)
admin.site.register(BasePlaylist)
admin.site.register(LibTrackPlaylistPositionRel)
admin.site.register(ManualPlaylist)
admin.site.register(GenrePlaylist)
admin.site.register(TagPlaylist)
admin.site.register(MusicbrainzRecording)
admin.site.register(MusicbrainzRecordingMissingCause)
admin.site.register(MusicbrainzRecordingMissingCauseCode)
admin.site.register(MusicbrainzArtist)
