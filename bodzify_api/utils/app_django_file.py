
from django.core.files.base import File as DjangoFile


class AppDjangoFile(DjangoFile):

    def __init__(self, file_abs_path, *args, **kwargs):
        self.file_abs_path = file_abs_path
        super(AppDjangoFile, self).__init__(*args, **kwargs)
