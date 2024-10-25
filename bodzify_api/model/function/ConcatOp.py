
#!/usr/bin/env python

from django.db import models


class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None  # type: ignore
    output_field = models.TextField()  # type: ignore
    template = "%(expressions)s"
