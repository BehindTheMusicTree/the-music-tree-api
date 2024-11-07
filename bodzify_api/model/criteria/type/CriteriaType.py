from django.db import models

from bodzify_api import settings


class CriteriaType(models.Model):
    label = models.CharField(unique=True, max_length=settings.CRITERIA_TYPE_LABEL_LEN_MAX)

    def __str__(self) -> str:
        return str(self.pk) + " " + self.label

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(label=""), name="criteria_non_empty_label")]
        db_table = 'bodzify_api_criteria_type'
        verbose_name = 'Criteria Type'
        verbose_name_plural = 'Criteria Types'
