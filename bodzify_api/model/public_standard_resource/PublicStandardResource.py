from django.db import models
from django.utils import timezone

from bodzify_api.model.base.BaseModel import BaseModel
from bodzify_api.utils.model import SaveContext


class PublicStandardResource(BaseModel):
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(null=True, editable=True)

    def save(self, *args, **kwargs):
        adding = self._state.adding
        ctx = self._create_save_context(**kwargs)
        kwargs = self._prepare_save(ctx)
        self._perform_save(adding=adding, ctx=ctx)
        if ctx.modified_fields and not ctx.should_track_fields:
            kwargs['update_fields'] = ctx.modified_fields
        super().save(*args, **kwargs)
        self._post_save(adding=adding)

    def _prepare_save(self, ctx: SaveContext) -> dict:
        return ctx.kwargs

    def _perform_save(self, adding: bool, ctx: SaveContext) -> None:
        if not adding:
            self.updated_on = timezone.now()
            ctx.add_modified_field('updated_on')

    def _post_save(self, adding: bool) -> None:
        pass

    class Meta:
        abstract = True
