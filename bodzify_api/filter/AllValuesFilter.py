from django_filters import CharFilter


class ForeignKeyFilter(CharFilter):
    def filter(self, queryset, value):
        if value == '':
            return queryset.filter(**{f"{self.field_name}__isnull": True})
        return super().filter(queryset, value)
