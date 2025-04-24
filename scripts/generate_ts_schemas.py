import os
import re
import sys
from typing import Type, cast, Union
from django.db import models
from django.apps import apps
from django.db.models.fields import (
    CharField, TextField, IntegerField, BooleanField, DateTimeField,
    UUIDField, Field
)
from django.contrib.postgres.fields import JSONField, ArrayField as PostgresArrayField
from django.db.models.fields.related import ForeignKey, ManyToManyField, ForeignObjectRel

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

FieldType = Union[Field, ForeignObjectRel]


def get_ts_type(field: FieldType) -> str:
    if isinstance(field, (CharField, TextField)):
        return 'z.string()'
    elif isinstance(field, IntegerField):
        return 'z.number()'
    elif isinstance(field, BooleanField):
        return 'z.boolean()'
    elif isinstance(field, DateTimeField):
        return 'z.string().datetime()'
    elif isinstance(field, UUIDField):
        return 'z.string().uuid()'
    elif isinstance(field, JSONField):
        return 'z.record(z.any())'
    elif isinstance(field, PostgresArrayField):
        base_type = get_ts_type(cast(Field, field.base_field))
        return f'z.array({base_type})'
    elif isinstance(field, (ForeignKey, ManyToManyField)):
        return 'z.string().uuid()'
    else:
        return 'z.any()'


def get_field_validations(field: FieldType) -> str:
    validations = []

    if isinstance(field, Field):
        if field.null:
            validations.append('.nullable()')
        if field.blank:
            validations.append('.optional()')
        if isinstance(field, CharField) and field.max_length:
            validations.append(f'.max({field.max_length})')

    return ''.join(validations)


def generate_schema(model: Type[models.Model], base_schema: str | None = None) -> str:
    schema_lines = []

    if base_schema:
        schema_lines.append(f'export const {model.__name__}Schema = {base_schema}.extend({{')
    else:
        schema_lines.append(f'export const {model.__name__}Schema = z.object({{')

    for field in model._meta.get_fields():
        if field.is_relation and not field.auto_created:
            field = cast(FieldType, field)
            field_name = field.name
            if field.many_to_many:
                field_name = f'{field_name}_ids'
            elif field.one_to_many:
                field_name = f'{getattr(field, "related_name", field.name)}_ids'
            else:
                field_name = f'{field_name}_id'
        else:
            field_name = field.name

        ts_type = get_ts_type(field)
        validations = get_field_validations(field)
        schema_lines.append(f'  {field_name}: {ts_type}{validations},')

    schema_lines.append('});')
    schema_lines.append(f'export type {model.__name__} = z.infer<typeof {model.__name__}Schema>;')

    return '\n'.join(schema_lines)


def generate_imports() -> str:
    return 'import { z } from "zod";\n'


def get_model_path(model: Type[models.Model]) -> str:
    # Get the full Python module path
    module_path = model.__module__

    # Remove the app name from the beginning
    if module_path.startswith('bodzify_api.'):
        module_path = module_path[len('bodzify_api.'):]

    # Convert Python module path to directory path
    path_parts = module_path.split('.')

    # Convert model name to kebab-case
    model_name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', model.__name__).lower()

    # Create the full path
    ts_path = os.path.join('tsexport', 'models', 'domain', *path_parts[:-1], model_name + '.ts')

    return ts_path


def get_relative_import_path(from_path: str, to_path: str) -> str:
    from_parts = os.path.dirname(from_path).split(os.sep)
    to_parts = os.path.dirname(to_path).split(os.sep)

    # Find common prefix
    common = 0
    for f, t in zip(from_parts, to_parts):
        if f != t:
            break
        common += 1

    # Build relative path
    up_count = len(from_parts) - common
    up = '../' * up_count
    down = '/'.join(to_parts[common:])

    if down:
        return up + down + '/uuid'
    return up + 'uuid'


def generate_schemas():
    # Get all models from all installed apps
    all_models = apps.get_models()

    # Filter models that are in your app
    your_models = [model for model in all_models if model._meta.app_label.startswith('bodzify_api')]

    # Create base resource schema
    base_schema = '''export const UuidResourceSchema = z.object({
  id: z.string().uuid(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime().nullable(),
});'''
    base_schema_path = 'tsexport/models/domain/base-resource/uuid.ts'
    os.makedirs(os.path.dirname(base_schema_path), exist_ok=True)
    with open(base_schema_path, 'w') as f:
        f.write(generate_imports() + base_schema)

    # Generate schemas for each model
    for model in your_models:
        if model._meta.abstract:
            continue

        schema = generate_schema(model, 'UuidResourceSchema')
        schema_path = get_model_path(model)

        os.makedirs(os.path.dirname(schema_path), exist_ok=True)
        relative_import = get_relative_import_path(schema_path, base_schema_path)
        with open(schema_path, 'w') as f:
            f.write(generate_imports() + f'import {{ UuidResourceSchema }} from "{relative_import}";\n\n' + schema)


if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodzify_api.settings')
    django.setup()
    generate_schemas()
