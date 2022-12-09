#!/usr/bin/env python

import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from django.core.files.storage import default_storage

from mutagen._file import File as MutagenFile
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3

import eyed3 

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


# MP3 track tagging is a mess. Here we'll use 3 tagging libraries : mutagen.mp3 ,mutagen.id3 and 
# mutagen.easyid3 because none of them can handle all the tags 
TAG_EASYID3_TITLE = "title"
TAG_EASYID3_ARTIST = "artist"
TAG_EASYID3_ALBUM = "album"
# We won't user the ID3v1 genre tag referencing a fix list of genres.
# See https://en.wikipedia.org/wiki/List_of_ID3v1_Genres
# Instead we use the "free genre" extended tag.
# See https://web.archive.org/web/20120310015458/http://www.fortunecity.com/underworld/sonic/3/id3tag.html
TAG_EASYID3_FREE_GENRE = "genre"
TAG_MP3_DURATION = "duration" # The duration tag doesn't belong to ID3
TAG_EASYID3_RATING = 'POPM'
TAG_EASYID3_LANGUAGE = "language"

# WAVE (WAV) files are also supposed to use ID3 tags but the tags don't seem to correspond
TAG_WAVE_TITLE = "TIT2"
TAG_WAVE_ARTIST = "TPE1"
TAG_WAVE_ALBUM = "TALB"
TAG_WAVE_GENRE = "TCON"
TAG_WAVE_RATING = 'POPM'
TAG_WAVE_LANGUAGE = "TLAN"

# FLAC files use Vorbis tags
TAG_VORBIS_TITLE = "title"
TAG_VORBIS_ARTIST = "artist"
TAG_VORBIS_ALBUM = "album"
TAG_VORBIS_GENRE = "genre"
TAG_VORBIS_RATING = 'POPM'
TAG_VORBIS_LANGUAGE = "language"
TAG_VORBIS_RATING = "rating"


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

    if type(uploadedFile) == InMemoryUploadedFile:
        file = File(file=uploadedFile, name=uploadedFile.name)
        filePath = settings.MEDIA_TEMP + file.name
        default_storage.save(filePath, file)
    else:
        filePath = uploadedFile.temporary_file_path()

    if fileExtension in [".wav", ".WAV"]:
        print(MutagenFile(uploadedFile).keys)
        trackWavTags = MutagenFile(uploadedFile)
        
        title = GetValuesFirstElementIfExistInDicOrEmptyString(trackWavTags, TAG_WAVE_TITLE)
        artist = GetValuesFirstElementIfExistInDicOrEmptyString(trackWavTags, TAG_WAVE_ARTIST)
        album = GetValuesFirstElementIfExistInDicOrEmptyString(trackWavTags, TAG_WAVE_ALBUM)

        if TAG_WAVE_GENRE in trackWavTags:
            genreName = trackWavTags[TAG_WAVE_GENRE][0]
        else:
            genreName = CriteriaSpecialNames.GENRE_GENRELESS

        duration = trackWavTags.info.length 

        rating = 0
        for key in trackWavTags.tags:
            if TAG_WAVE_RATING in key:
                rating = trackWavTags[key].rating

        language = GetValuesFirstElementIfExistInDicOrEmptyString(trackWavTags, TAG_WAVE_LANGUAGE)

    elif fileExtension in [".flac", ".FLAC"]:
        trackFlacTags = FLAC(filePath)
        
        title = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, TAG_VORBIS_TITLE)
        artist = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, TAG_VORBIS_ARTIST)
        album = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, TAG_VORBIS_ALBUM)

        if TAG_VORBIS_GENRE in trackFlacTags:
            genreName = trackFlacTags[TAG_VORBIS_GENRE][0]
        else:
            genreName = CriteriaSpecialNames.GENRE_GENRELESS

        duration = trackFlacTags.info.length
        rating = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, TAG_VORBIS_RATING)
        language = GetValuesFirstElementIfExistInDicOrEmptyString(trackFlacTags, TAG_VORBIS_LANGUAGE)

    else:
        trackId3Tags = ID3(filePath)
        trackEasyId3Tags = EasyID3(filePath)
        trackMp3Tags = MP3(filePath)

        title = GetValuesFirstElementIfExistInDicOrEmptyString(trackEasyId3Tags, TAG_EASYID3_TITLE)
        artist = GetValuesFirstElementIfExistInDicOrEmptyString(trackEasyId3Tags, TAG_EASYID3_ARTIST)
        album = GetValuesFirstElementIfExistInDicOrEmptyString(trackEasyId3Tags, TAG_EASYID3_ALBUM)

        if TAG_EASYID3_FREE_GENRE in trackEasyId3Tags:
            genreName = trackEasyId3Tags[TAG_EASYID3_FREE_GENRE][0]
        else:
            genreName = CriteriaSpecialNames.GENRE_GENRELESS

        duration = trackMp3Tags.info.length
        
        rating = 0
        for key in trackId3Tags.items():
            if TAG_EASYID3_RATING in key:
                rating = trackId3Tags[key].rating
                
        language = GetValuesFirstElementIfExistInDicOrEmptyString(trackEasyId3Tags, TAG_EASYID3_LANGUAGE)

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


    if type(uploadedFile) == InMemoryUploadedFile:
        default_storage.delete(filePath)

    return track


def AddTrackToGenrePlaylists(user, track):
    genre = track.genre
    while genre is not None:
        track.playlists.add(Playlist.objects.get(user=user, criteria=track.genre))
        genre = genre.parent
    track.save()

def MoveTemporaryFileToLibrary(user, temporaryFile, libraryTrack):
    userLibraryPath = settings.LIBRARIES_ROOT + user.get_username() + "/"
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
