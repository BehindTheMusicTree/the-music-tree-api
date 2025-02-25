from django.core.files import File


class AppDjangoFile(File):

    def __init__(self, file_abs_path: str, *args, **kwargs):
        self.file_abs_path = file_abs_path
        super().__init__(file_abs_path, *args, **kwargs)
