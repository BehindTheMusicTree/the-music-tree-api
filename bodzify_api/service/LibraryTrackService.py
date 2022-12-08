#!/usr/bin/env python

import os

from django.core.files.uploadedfile import SimpleUploadedFile

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


ID3_TAG_TITLE = "title"
ID3_TAG_ARTIST = "artist"
ID3_TAG_ALBUM = "album"
ID3_TAG_GENRE = "genre"
ID3_TAG_DURATION = "duration"
ID3_TAG_RATING = "titlesort"
ID3_TAG_LANGUAGE = "language"


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
    trackFile = EasyID3(track.path)

    titleTag = track.title
    if titleTag is None:
        titleTag = ""
    trackFile[ID3_TAG_TITLE] = titleTag

    artistTag = track.artist
    if artistTag is None:
        artistTag = ""
    trackFile[ID3_TAG_ARTIST] = artistTag

    albumTag = track.album
    if albumTag is None:
        albumTag = ""
    trackFile[ID3_TAG_ALBUM] = albumTag

    if track.genre is None:
        genreTag = ""
    else:
        genreTag = track.genre.name
    trackFile[ID3_TAG_GENRE] = genreTag

    ratingTag = track.rating
    if ratingTag is None:
        ratingTag = -1
    trackFile[ID3_TAG_RATING] = str(ratingTag)

    languageTag = track.language
    if languageTag is None:
        languageTag = ""
    trackFile[ID3_TAG_LANGUAGE] = languageTag
    trackFile.save()


def CreateFromUpload(user, temporaryFile):
    trackIdTags = EasyID3(temporaryFile.temporary_file_path())

    genreName = trackIdTags[ID3_TAG_GENRE]
    if Criteria.objects.filter(
        user=user, type__id=CriteriaTypesIds.GENRE, name=genreName).exists():
        genre = Criteria.objects.get(user=user, type__id=CriteriaTypesIds.GENRE, name=genreName)
    else:
        genre = Criteria(
            user=user,
            type=CriteriaType.objects.get(id=CriteriaTypesIds.GENRE),
            name=genreName,
            parent=Criteria.objects.get(user=user, name=CriteriaSpecialNames.GENRE_ALL)
        ).save()

    track = LibraryTrack(
        user=user,
        file=temporaryFile,
        title=trackIdTags[ID3_TAG_TITLE],
        artist=trackIdTags[ID3_TAG_ARTIST],
        album=trackIdTags[ID3_TAG_ALBUM],
        genre=genre,
        rating=trackIdTags[ID3_TAG_RATING],
        language=trackIdTags[ID3_TAG_LANGUAGE]
    ).save()

    AddTrackToGenrePlaylists(user, track)
    track.playlists.add(Playlist.objects.get(
            user=user,
            criteria__name=CriteriaSpecialNames.TAG_ALL
        )
    )
    return track.save()


def AddTrackToGenrePlaylists(user, track):
    while genre is not None:
        track.playlists.add(Playlist.objects.get(user=user, genre=track.genre))
        genre = genre.parent

def MoveTemporaryFileToLibrary(user, temporaryFile, libraryTrack):
    userLibraryPath = settings.LIBRARIES_PATH + user.get_username() + "/"
    userLibraryPath = settings.LIBRARIES_PATH + user.get_username() + "/"

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
