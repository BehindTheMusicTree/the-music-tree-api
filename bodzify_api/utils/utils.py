#!/usr/bin/env python

from django.core.files.base import File as DjangoFile


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class AppDjangoFile(DjangoFile):

    def __init__(self, file_abs_path, *args, **kwargs):
        self.file_abs_path = file_abs_path
        super(AppDjangoFile, self).__init__(*args, **kwargs)
