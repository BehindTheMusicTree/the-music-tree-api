from django.contrib import admin

from .model.user.admin.UserAdmin import UserAdmin
from .model.user.User import User
from .model.album.Album import Album
from .model.criteria.children.genre.Genre import Genre
from .model.criteria.children.tag.Tag import Tag
from .model.criteria_acendant_rel.children.tag.TagAscendantRel import TagAscendantRel
from .model.criteria_acendant_rel.children.genre.GenreAscendantRel import GenreAscendantRel
from .model.playlist.children.criteria.children.genre.GenrePlaylist import GenrePlaylist
from .model.playlist.children.criteria.children.tag.TagPlaylist import TagPlaylist
from .model.all_lib_track_mixin.AllLibTrackMixin import AllLibTrackMixin
from .model.artist.Artist import Artist
from .model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from .model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist
from .model.musicbrainz.recording.MusicbrainzRecording import MusicbrainzRecording
from .model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCause import MusicbrainzRecordingMissingCause
from .model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode
from .model.playlist.BasePlaylist import BasePlaylist
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
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(GenreAscendantRel)
admin.site.register(TagAscendantRel)
admin.site.register(BasePlaylist)
admin.site.register(LibTrackPlaylistPositionRel)
admin.site.register(ManualPlaylist)
admin.site.register(GenrePlaylist)
admin.site.register(TagPlaylist)
admin.site.register(MusicbrainzRecording)
admin.site.register(MusicbrainzRecordingMissingCause)
admin.site.register(MusicbrainzRecordingMissingCauseCode)
admin.site.register(MusicbrainzArtist)
