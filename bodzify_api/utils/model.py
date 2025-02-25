from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SaveContext:
    """Context for save operations"""
    kwargs: Dict[str, Any]
    modified_fields: List[str]
    update_fields: List[str] | None

    @staticmethod
    def create(**kwargs) -> 'SaveContext':
        """Factory method to create SaveContext instances"""
        return SaveContext(
            kwargs=kwargs,
            modified_fields=[],
            update_fields=kwargs.get('update_fields')
        )

    @property
    def should_track_fields(self) -> bool:
        return self.update_fields is not None

    def add_modified_field(self, field: str) -> None:
        """Add a field to modified_fields and update_fields if needed"""
        self.modified_fields.append(field)
        if self.should_track_fields and field not in self.update_fields:
            self.update_fields.append(field)


def ensure_update_field(kwargs: Dict, field_name: str) -> Dict:
    """
    Ensures a field is included in update_fields if update_fields is being used.

    Args:
        kwargs: The kwargs Dict passed to save()
        field_name: The field name to ensure is included

    Returns:
        Modified kwargs Dict with field_name added to update_fields if needed
    """
    if 'update_fields' not in kwargs:
        kwargs['update_fields'] = [field_name]
    elif kwargs['update_fields'] is not None:
        if field_name not in kwargs['update_fields']:
            kwargs['update_fields'].append(field_name)
    return kwargs


def ensure_update_fields(kwargs: Dict, field_names: list[str]) -> Dict:
    """
    Ensures multiple fields are included in update_fields if update_fields is being used.

    Args:
        kwargs: The kwargs Dict passed to save()
        field_names: List of field names to ensure are included

    Returns:
        Modified kwargs Dict with field_names added to update_fields if needed
    """
    if 'update_fields' not in kwargs:
        kwargs['update_fields'] = field_names
    elif kwargs['update_fields'] is not None:
        for field in field_names:
            if field not in kwargs['update_fields']:
                kwargs['update_fields'].append(field)
    return kwargs
