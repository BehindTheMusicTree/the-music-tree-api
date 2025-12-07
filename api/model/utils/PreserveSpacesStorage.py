from django.core.files.storage import FileSystemStorage


class PreserveSpacesStorage(FileSystemStorage):
    def get_valid_name(self, name):
        return name
