import os
import requests
import myfreemp3api.settings as apiSettings

def downloadExternalSong (user, song):
    userLibraryPath = apiSettings.LIBRARIES_PATH + user.get_username() + "/"

    if not os.path.exists(userLibraryPath):
        os.makedirs(userLibraryPath)

    externalSongUrl = song.url
    externalSong = requests.get(externalSongUrl)
    externalSongName, externalSongExtension = os.path.splitext(externalSongUrl)

    internalSongFilePathWithoutExtension = userLibraryPath + "/" + song.artist + " - " + song.title
    internalSongFilePath = internalSongFilePathWithoutExtension + externalSongExtension

    existingFileCount = 0
    while os.path.exists(internalSongFilePath):
        existingFileCount = existingFileCount + 1
        internalSongFilePath = internalSongFilePathWithoutExtension + " (" + str(existingFileCount) + ")" + externalSongExtension


    with open(internalSongFilePath, 'wb') as file:
        file.write(externalSong.content)
