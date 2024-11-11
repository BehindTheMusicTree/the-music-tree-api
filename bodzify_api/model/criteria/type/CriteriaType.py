from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.BaseModel import BaseModel


class CriteriaType(BaseModel):
    label = models.CharField(unique=True, max_length=settings.CRITERIA_TYPE_LABEL_LEN_MAX)

    def __str__(self) -> str:
        return f"{self.pk} | {self.label}"

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(label=""), name="criteria_non_empty_label")]
        verbose_name = 'Criteria Type'
        verbose_name_plural = 'Criteria Types'
