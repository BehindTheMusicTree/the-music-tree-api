#!/usr/bin/env python

import os

from mutagen._file import File as MutagenFile
from mutagen.id3 import Frames
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3UnsupportedVersionError
from mutagen.id3 import CHAP
from mutagen.id3 import TIT2
from mutagen.id3 import CTOC
from mutagen.id3 import TT1
from mutagen.id3 import TCON
from mutagen.id3 import COMM
from mutagen.id3 import TORY
from mutagen.id3 import PIC
from mutagen.id3 import TRCK
from mutagen.id3 import TDRC
from mutagen.id3 import TDAT
from mutagen.id3 import TIME
from mutagen.id3 import LNK
from mutagen.id3 import TYER
from mutagen.id3 import IPLS
from mutagen.id3 import TPE1
from mutagen.id3 import BinaryFrame
from mutagen.id3 import POPM
from mutagen.id3 import APIC
from mutagen.id3 import CRM
from mutagen.id3 import TALB
from mutagen.id3 import TPE2
from mutagen.id3 import TSOT
from mutagen.id3 import TPE2
from mutagen.id3 import TDEN
from mutagen.id3 import TPE2
from mutagen.id3 import TIPL
from mutagen.id3 import Encoding
from mutagen.id3 import ID3Tags

import bodzify_api.settings as settings
import bodzify_api.service.CriteriaService as CriteriaService
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames
from bodzify_api.model.playlist.PlaylistType import PlaylistType
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
from bodzify_api.model.criteria.CriteriaType import CriteriaType
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesIds

# MP3 and Wave (.wav) files use ID3 tags
ID3_TITLE_TAG = 'TIT2'
ID3_ARTIST_TAG = 'TPE1'
ID3_ALBUM_TAG = 'TALB'
ID3_GENRE_TAG = 'TCON'
ID3_RATING_TAG = 'POPM'
ID3_GENRE_APP_EMAIL = 'POPM:bodzify'
ID3_LANGUAGE_TAG = 'TLAN'

# FLAC files use Vorbis tags
VORBIS_TITLE_TAG = 'title'
VORBIS_ARTIST_TAG = 'artist'
VORBIS_ALBUM_TAG = 'album'
VORBIS_GENRE_TAG = 'genre'
VORBIS_RATING_TAG = 'rating'
VORBIS_LANGUAGE_TAG = 'language'


def UpdatePlaylists(track, user, oldGenre):
    newGenre = track.genre

    genrePlaylistType = PlaylistType.objects.get(id=PlaylistTypeIds.GENRE)

    commonGenre = CriteriaService.GetCommonCriteria(oldGenre, newGenre)

    newGenreTreeItem = newGenre

    while newGenreTreeItem != commonGenre:
        track.playlists.add(Playlist.objects.get(
            user=user,
            type=genrePlaylistType,
            criteria=newGenreTreeItem))            
        newGenreTreeItem = newGenreTreeItem.parent

    oldGenreTreeItem = oldGenre

    while oldGenreTreeItem != commonGenre:
        track.playlists.remove(Playlist.objects.get(
            user=user,
            type=genrePlaylistType,
            criteria=oldGenreTreeItem))
        oldGenreTreeItem = oldGenreTreeItem.parent
        
    track.save()


def Update(track, data, partial, RequestSerializerClass, user):
    oldGenre = LibraryTrack.objects.get(uuid=track.uuid).genre

    if data['genre'] is None:
        data['genre'] = Criteria.objects.get(
            user=user, name=CriteriaSpecialNames.GENRE_GENRELESS).uuid

    requestSerializer = RequestSerializerClass(track, data=data, partial=partial)
    requestSerializer.is_valid(raise_exception=True)
    updatedTrack = requestSerializer.save()


    if oldGenre != updatedTrack.genre:
        UpdatePlaylists(track=updatedTrack, user=user, oldGenre=oldGenre)

    UpdateTags(updatedTrack)

    return updatedTrack


def UpdateTags(track):

    titleTag = track.title
    if titleTag is None:
        titleTag = ""

    artistTag = track.artist
    if artistTag is None:
        artistTag = ""

    albumTag = track.album
    if albumTag is None:
        albumTag = ""

    if track.genre is None:
        genreTag = ""
    else:
        genreTag = track.genre.name

    ratingTag = track.rating
    if ratingTag is None:
        ratingTag = 0

    languageTag = track.language
    if languageTag is None:
        languageTag = ""

    if track.fileExtension.lower() in [".wav", ".mp3"]:

        trackId3Tags = ID3(track.file.path)

        trackId3Tags.delall(ID3_RATING_TAG)
        trackId3Tags.delall(ID3_TITLE_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=titleTag))
        trackId3Tags.delall(ID3_ARTIST_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=artistTag))
        trackId3Tags.delall(ID3_ALBUM_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=albumTag))
        trackId3Tags.delall(ID3_GENRE_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=genreTag))
        trackId3Tags.delall(ID3_RATING_TAG)
        trackId3Tags.add(POPM(email=ID3_GENRE_APP_EMAIL, rating=ratingTag))
        trackId3Tags.delall(ID3_LANGUAGE_TAG)
        trackId3Tags.add(TIT2(encoding=3, text=languageTag))


    elif track.fileExtension.lower() == ".flac":
        trackFlacTags = FLAC(track.file.path)
        trackFlacTags[VORBIS_TITLE_TAG] = titleTag
        trackFlacTags[VORBIS_ARTIST_TAG] = artistTag
        trackFlacTags[VORBIS_ALBUM_TAG] = albumTag
        trackFlacTags[VORBIS_GENRE_TAG] = genreTag
        trackFlacTags[VORBIS_RATING_TAG][0] = str(ratingTag)
        trackFlacTags[VORBIS_LANGUAGE_TAG] = languageTag
        trackFlacTags.save(track.file.path)


def GetValuesFirstElementIfExistInDicOrEmptyString(dic, key):
    if key in dic:
        return dic[key][0]
    else:
        return ""


def GetValuesFirstElementIfExistInDicOrZero(dic, key):
    if key in dic:
        return dic[key][0]
    else:
        return 0


def CreateFromUpload(user, uploadedFile):
    filename, fileExtension = os.path.splitext(uploadedFile.name)

    if fileExtension.lower() in [".wav", ".mp3"]:
        trackId3Tags = MutagenFile(uploadedFile)
        
        title = GetValuesFirstElementIfExistInDicOrEmptyString(trackId3Tags, ID3_TITLE_TAG)
        artist = GetValuesFirstElementIfExistInDicOrEmptyString(trackId3Tags, ID3_ARTIST_TAG)
        album = GetValuesFirstElementIfExistInDicOrEmptyString(trackId3Tags, ID3_ALBUM_TAG)

        if ID3_GENRE_TAG in trackId3Tags:
            genreName = trackId3Tags[ID3_GENRE_TAG][0]
        else:
            genreName = CriteriaSpecialNames.GENRE_GENRELESS

        duration = trackId3Tags.info.length 

        rating = 0
        for key in trackId3Tags.tags:
            if ID3_RATING_TAG in key:
                rating = trackId3Tags[key].rating

        language = GetValuesFirstElementIfExistInDicOrEmptyString(trackId3Tags, ID3_LANGUAGE_TAG)

    elif fileExtension.lower() == ".flac":
        trackFlacTags = FLAC(fileobj=uploadedFile)
        
        title = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, VORBIS_TITLE_TAG)
        artist = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, VORBIS_ARTIST_TAG)
        album = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, VORBIS_ALBUM_TAG)

        if VORBIS_GENRE_TAG in trackFlacTags:
            genreName = trackFlacTags[VORBIS_GENRE_TAG][0]
        else:
            genreName = CriteriaSpecialNames.GENRE_GENRELESS

        duration = trackFlacTags.info.length
        rating = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, VORBIS_RATING_TAG)
        if rating == "":
            rating = "0"
        language = GetValuesFirstElementIfExistInDicOrEmptyString(
            trackFlacTags, VORBIS_LANGUAGE_TAG)

    if Criteria.objects.filter(
        user=user, type__id=CriteriaTypesIds.GENRE, name=genreName).exists():
        genre = Criteria.objects.get(user=user, type__id=CriteriaTypesIds.GENRE, name=genreName
        )
    else:
        genre = Criteria.objects.create(
            user=user,
            type=CriteriaType.objects.get(id=CriteriaTypesIds.GENRE),
            name=genreName,
            parent=Criteria.objects.get(user=user, name=CriteriaSpecialNames.GENRE_ALL)
        )
        Playlist.objects.create(
            user=user,
            criteria=genre,
            name=genre.name,
            type=PlaylistType.objects.get(pk=PlaylistTypeIds.GENRE)
        )

    track = LibraryTrack.objects.create(
        user=user,
        file=uploadedFile,
        title=title,
        artist=artist,
        album=album,
        genre=genre,
        duration=duration,
        rating=rating,
        language=language
    )

    AddTrackToGenrePlaylists(user, track)

    return track


def AddTrackToGenrePlaylists(user, track):
    genre = track.genre
    while genre is not None:
        track.playlists.add(Playlist.objects.get(user=user, criteria=genre))
        genre = genre.parent
    track.save()


def CreateFromMineTrack(user, mineTrack, trackTempFileAbsolutePath):
    # Tags of every myfreemp3 downloaded tracks are empty 
    libraryTrack = LibraryTrack(
        user=user, 
        title=mineTrack.title, 
        artist=mineTrack.artist, 
        album="",
        genre=Criteria.objects.get(user=user, name=CriteriaSpecialNames.GENRE_GENRELESS),
        duration=mineTrack.duration,
        rating=0,
        language="")
    libraryTrack.file.name = trackTempFileAbsolutePath
    libraryTrack.save()

    libraryTrack.playlists.add(
        Playlist.objects.get(
            user=user, 
            name=PlaylistSpecialNames.GENRE_ALL))
    libraryTrack.playlists.add(
        Playlist.objects.get(
            user=user, 
            name=PlaylistSpecialNames.GENRE_GENRELESS))
    libraryTrack.save()

    UpdateTags(libraryTrack)

    return libraryTrack


def delete(uuid):
    track = LibraryTrack.objects.get(uuid=uuid)
    os.remove(track.path)
    track.delete()
