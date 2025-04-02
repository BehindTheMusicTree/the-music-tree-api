from django.db import models
from django.utils import timezone

from bodzify_api.model.base.BaseModel import BaseModel
from bodzify_api.utils.model import SaveContext


class PublicStandardResource(BaseModel):
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(null=True, editable=True)

    def _perform_save(self, adding: bool, ctx: SaveContext) -> None:
        if not adding:
            self.updated_on = timezone.now()
            ctx.add_modified_field('updated_on')

    class Meta:
        abstract = True
