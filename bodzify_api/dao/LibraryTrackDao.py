#!/usr/bin/env python

import os

from mutagen.easyid3 import EasyID3

import bodzify_api.settings as settings
from bodzify_api.models import LibraryTrack, Genre

ID3_TAG_TITLE = "title"
ID3_TAG_ARTIST = "artist"
ID3_TAG_ALBUM = "album"
ID3_TAG_GENRE = "genre"
ID3_TAG_DURATION = "duration"
ID3_TAG_RATING = "titlesort"
ID3_TAG_LANGUAGE = "language"

def updateTags(track):
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

def createFromMineTrack(mineTrack, trackFile, user):
    userLibraryPath = settings.LIBRARIES_PATH + user.get_username() + "/"

    if not os.path.exists(userLibraryPath):
        os.makedirs(userLibraryPath)

    externalTrackName, trackExtension = os.path.splitext(mineTrack.url)

    artistTitle = mineTrack.artist + " - " + mineTrack.title
    libraryFilename = artistTitle + trackExtension
    internalTrackFilePath = userLibraryPath + libraryFilename

    existingFileCount = 0
    while os.path.exists(internalTrackFilePath):
        existingFileCount = existingFileCount + 1
        libraryFilename = artistTitle + " (" + str(existingFileCount) + ")" + trackExtension
        internalTrackFilePath = userLibraryPath + libraryFilename

    with open(internalTrackFilePath, 'wb') as file:
        file.write(trackFile.content)

    # Tags of every myfreemp3 downloaded tracks are empty 
    libraryTrack = LibraryTrack(
        path=internalTrackFilePath,
        user=user, 
        title=mineTrack.title, 
        artist=mineTrack.artist, 
        album="", 
        genre=None, 
        duration=mineTrack.duration,
        rating=-1,
        language="")
    libraryTrack.save()

    updateTags(libraryTrack)

    return libraryTrack

def get(uuid):
    return LibraryTrack.objects.get(uuid=uuid)

def getAllByUser(user):
    return LibraryTrack.objects.filter(user=user)

def delete(uuid):
    track = LibraryTrack.objects.get(uuid=uuid)
    os.remove(track.path)
    track.delete()