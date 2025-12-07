from django.db import models

from api import settings
from api.model.base.BaseModel import BaseModel
from api.model.field.AppCharField import AppCharField


class CriteriaType(BaseModel):
    label = AppCharField(unique=True, max_length=settings.CRITERIA_TYPE_LABEL_LEN_MAX)

    def __str__(self) -> str:
        return f"{self.pk} | {self.label}"

    class Meta:
        constraints = [models.CheckConstraint(condition=~models.Q(label=""), name="criteria_non_empty_label")]
        verbose_name = 'Criteria Type'
        verbose_name_plural = 'Criteria Types'
