from django.urls import reverse

from bodzify_api.test.view.ViewTestCase import ViewTestCase


class TrackViewTestCase(ViewTestCase):

    def postSampleTrack(self, sampleFileName):
        with open(self.sampleDirectoryAbsolutePath + sampleFileName, "rb") as sampleFile:
            return self.apiClient.post(
                path=reverse('librarytrack-list'), data={'file': sampleFile})

    def putSampleTrack(self, trackUuid, data):
        return self.apiClient.put(
            path=reverse('librarytrack-detail', kwargs={'pk':trackUuid}), data=data)

    def downloadTrack(self, trackUuid):
        return self.apiClient.get(path=reverse('librarytrack-download', kwargs={'pk':trackUuid}))
