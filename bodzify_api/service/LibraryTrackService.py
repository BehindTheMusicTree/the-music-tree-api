#!/usr/bin/env python

import os

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
TAG_EASYID3_RATING = 'POPM'
TAG_EASYID3_LANGUAGE = "language"

TAG_MP3_DURATION = "duration"

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


def CreateFromUpload(user, temporaryFile):
    filename, fileExtension = os.path.splitext(temporaryFile.name)

    if fileExtension in ["flac", "FLAC"]:
        trackId3Tags = ID3(temporaryFile.temporary_file_path())
        trackEasyId3Tags = EasyID3(temporaryFile.temporary_file_path())
        trackMp3Tags = MP3(temporaryFile.temporary_file_path())

        title =trackEasyId3Tags[TAG_EASYID3_TITLE][0]
        artist = trackEasyId3Tags[TAG_EASYID3_ARTIST][0]
        album = trackEasyId3Tags[TAG_EASYID3_ALBUM][0]
        genreName = trackEasyId3Tags[TAG_EASYID3_FREE_GENRE][0]
        rating = next(v for k,v in trackId3Tags.items() if TAG_EASYID3_RATING in k).rating
        duration = trackMp3Tags.info.length
        language = trackEasyId3Tags[TAG_EASYID3_LANGUAGE][0]
        
    else:
        trackFlacTags = FLAC(temporaryFile.temporary_file_path())

        title = trackFlacTags[TAG_EASYID3_TITLE][0]
        artist = trackFlacTags[TAG_EASYID3_ARTIST][0]
        album = trackFlacTags[TAG_EASYID3_ALBUM][0]
        genreName = trackFlacTags[TAG_VORBIS_GENRE][0]
        duration = trackFlacTags.info.length
        rating = trackFlacTags[TAG_VORBIS_RATING][0]
        language = trackFlacTags[TAG_EASYID3_LANGUAGE][0]


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
        file=temporaryFile,
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
