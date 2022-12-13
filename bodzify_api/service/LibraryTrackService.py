#!/usr/bin/env python

import os

from mutagen._file import File as MutagenFile
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3

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
TAG_ID3_TITLE = 'TIT2'
TAG_ID3_ARTIST = 'TPE1'
TAG_ID3_ALBUM = 'TALB'
TAG_ID3_GENRE = 'TCON'
TAG_ID3_RATING = 'POPM'
TAG_ID3_LANGUAGE = 'TLAN'

# FLAC files use Vorbis tags
TAG_VORBIS_TITLE = 'title'
TAG_VORBIS_ARTIST = 'artist'
TAG_VORBIS_ALBUM = 'album'
TAG_VORBIS_GENRE = 'genre'
TAG_VORBIS_RATING = 'POPM'
TAG_VORBIS_LANGUAGE = 'language'
TAG_VORBIS_RATING = 'rating'


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
    requestSerializer = RequestSerializerClass(track, data=data, partial=partial)
    requestSerializer.is_valid(raise_exception=True)
    updatedTrack = requestSerializer.save()

    if oldGenre != updatedTrack.genre:
        UpdatePlaylists(track=updatedTrack, user=user, oldGenre=oldGenre)

    UpdateTags(updatedTrack)

    return updatedTrack


def UpdateTags(track):
    trackFile = MP3(track.path)

    titleTag = track.title
    if titleTag is None:
        titleTag = ""
    trackFile[TAG_EASYID3_TITLE] = titleTag

    artistTag = track.artist
    if artistTag is None:
        artistTag = ""
    trackFile[TAG_EASYID3_ARTIST] = artistTag

    albumTag = track.album
    if albumTag is None:
        albumTag = ""
    trackFile[TAG_EASYID3_ALBUM] = albumTag

    if track.genre is None:
        genreTag = ""
    else:
        genreTag = track.genre.name
    trackFile[TAG_EASYID3_FREE_GENRE] = genreTag

    ratingTag = track.rating
    if ratingTag is None:
        ratingTag = -1
    trackFile[TAG_EASYID3_RATING].rating = str(ratingTag)

    languageTag = track.language
    if languageTag is None:
        languageTag = ""
    trackFile[TAG_EASYID3_LANGUAGE] = languageTag
    trackFile.save()


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

    if fileExtension in [".wav", ".WAV", ".mp3"]:
        trackWavTags = MutagenFile(uploadedFile)
        
        title = GetValuesFirstElementIfExistInDicOrEmptyString(trackWavTags, TAG_ID3_TITLE)
        artist = GetValuesFirstElementIfExistInDicOrEmptyString(trackWavTags, TAG_ID3_ARTIST)
        album = GetValuesFirstElementIfExistInDicOrEmptyString(trackWavTags, TAG_ID3_ALBUM)

        if TAG_ID3_GENRE in trackWavTags:
            genreName = trackWavTags[TAG_ID3_GENRE][0]
        else:
            genreName = CriteriaSpecialNames.GENRE_GENRELESS

        duration = trackWavTags.info.length 

        rating = 0
        for key in trackWavTags.tags:
            if TAG_ID3_RATING in key:
                rating = trackWavTags[key].rating

        language = GetValuesFirstElementIfExistInDicOrEmptyString(trackWavTags, TAG_ID3_LANGUAGE)

    elif fileExtension in [".flac", ".FLAC"]:
        trackFlacTags = FLAC(fileobj=uploadedFile)
        
        title = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, TAG_VORBIS_TITLE)
        artist = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, TAG_VORBIS_ARTIST)
        album = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, TAG_VORBIS_ALBUM)

        if TAG_VORBIS_GENRE in trackFlacTags:
            genreName = trackFlacTags[TAG_VORBIS_GENRE][0]
        else:
            genreName = CriteriaSpecialNames.GENRE_GENRELESS

        duration = trackFlacTags.info.length
        rating = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, TAG_VORBIS_RATING)
        language = GetValuesFirstElementIfExistInDicOrEmptyString(
            trackFlacTags, TAG_VORBIS_LANGUAGE)

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

def MoveTemporaryFileToLibrary(user, temporaryFile, libraryTrack):
    userLibraryPath = settings.LIBRARIES_ROOT + user.get_username() + "/"

    if not os.path.exists(userLibraryPath):
        os.makedirs(userLibraryPath)

    externalTrackName, trackExtension = os.path.splitext(temporaryFile.temporary_file_path)

    artistTitle = libraryTrack.artist + " - " + libraryTrack.title
    libraryFilename = artistTitle + trackExtension
    internalTrackFilePath = userLibraryPath + libraryFilename

    existingFileCount = 0
    while os.path.exists(internalTrackFilePath):
        existingFileCount = existingFileCount + 1
        libraryFilename = artistTitle + " (" + str(existingFileCount) + ")" + trackExtension
        internalTrackFilePath = userLibraryPath + libraryFilename

    with open(internalTrackFilePath, 'wb') as file:
        file.write(temporaryFile.content)

    return internalTrackFilePath


def CreateFromMineTrack(user, mineTrack, trackFile):
    internalTrackFilePath = MoveTemporaryFileToLibrary(user=user, temporaryFile=trackFile)

    # Tags of every myfreemp3 downloaded tracks are empty 
    libraryTrack = LibraryTrack(
        user=user, 
        title=mineTrack.title, 
        artist=mineTrack.artist, 
        album="",
        genre=Criteria.objects.get(user=user, name=CriteriaSpecialNames.GENRE_GENRELESS),
        duration=mineTrack.duration,
        rating=-1,
        language="")
    libraryTrack.save(path=internalTrackFilePath)

    libraryTrack.playlists.add(
        Playlist.objects.get(
            user=user, 
            name=PlaylistSpecialNames.GENRE_ALL))
    libraryTrack.playlists.add(
        Playlist.objects.get(
            user=user, 
            name=PlaylistSpecialNames.GENRE_GENRELESS))
    libraryTrack.playlists.add(
        Playlist.objects.get(
            user=user, 
            name=PlaylistSpecialNames.TAG_ALL))
    libraryTrack.save()

    UpdateTags(libraryTrack)

    return libraryTrack


def delete(uuid):
    track = LibraryTrack.objects.get(uuid=uuid)
    os.remove(track.path)
    track.delete()
