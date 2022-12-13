from django.urls import reverse

from bodzify_api.test.view.ViewTestCase import ViewTestCase


class LibraryTrackViewTestCase(ViewTestCase):

    def postSampleTrack(self, sampleFileName):
        with open(self.sampleAbsolutePath + sampleFileName, "rb") as sampleFile:
            return self.apiClient.post(
                path=reverse('librarytrack-list'), data={'file': sampleFile})

    def putSampleTrack(self, data):
        return self.apiClient.put(data=data)
