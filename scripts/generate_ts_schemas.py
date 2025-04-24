import os
import re
import sys
import shutil
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

# Base directory for TypeScript exports
BASE_DIR = 'frontend/domain'

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

    # Generate interface for abstract models
    if model._meta.abstract:
        schema_lines.append(f'export interface {model.__name__} {{')
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

            ts_type = get_ts_type(field).replace('z.', '').replace('()', '')
            if field.null:
                ts_type += ' | null'
            schema_lines.append(f'  {field_name}: {ts_type};')
        schema_lines.append('}')
    else:
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

    # If there's only one model in this path, don't create a directory
    if len(path_parts) == 1:
        return os.path.join(BASE_DIR, model_name + '.ts')

    # Create the full path with directories
    ts_path = os.path.join(BASE_DIR, 'model', *path_parts[:-1], model_name + '.ts')

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
        return f'@/models/domain/{down}/uuid'
    return '@/models/domain/uuid'


def count_files_in_directories(models: list[Type[models.Model]]) -> dict[str, int]:
    """Count how many files would be in each directory."""
    counts = {}
    for model in models:
        path = get_model_path(model)
        dir_path = os.path.dirname(path)
        counts[dir_path] = counts.get(dir_path, 0) + 1
    return counts


def get_final_path(path: str, dir_counts: dict[str, int]) -> str:
    """Get the final path for a file, moving it up if it would be alone in its entire subtree."""
    dir_path = os.path.dirname(path)

    # Check if there are any files in subdirectories
    has_files_in_subtree = False
    for count_path, count in dir_counts.items():
        if count_path.startswith(dir_path + os.sep):
            has_files_in_subtree = True
            break

    # Only move up if this is the only file in the entire subtree
    if dir_counts.get(dir_path, 0) <= 1 and not has_files_in_subtree:
        return os.path.join(os.path.dirname(dir_path), os.path.basename(path))
    return path


def clean_base_dir():
    """Remove and recreate the base directory to ensure clean state."""
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    os.makedirs(BASE_DIR)


def generate_schemas():
    # Clean base directory first
    clean_base_dir()

    # Get all models from all installed apps
    all_models = apps.get_models()

    # Filter models that are in your app
    your_models = [model for model in all_models if model._meta.app_label.startswith('bodzify_api')]

    # Count files in each directory
    dir_counts = count_files_in_directories(your_models)

    # Create base resource schema
    base_schema = '''export const UuidResourceSchema = z.object({
  id: z.string().uuid(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime().nullable(),
});'''
    base_schema_path = os.path.join(BASE_DIR, 'uuid.ts')
    # Create parent directory for base schema
    os.makedirs(os.path.dirname(base_schema_path), exist_ok=True)
    with open(base_schema_path, 'w') as f:
        f.write(generate_imports() + base_schema)

    # Generate schemas for each model
    for model in your_models:
        schema = generate_schema(model, 'UuidResourceSchema')
        schema_path = get_model_path(model)
        # Get the final path, moving the file up if it would be alone
        final_path = get_final_path(schema_path, dir_counts)

        # Create parent directory
        os.makedirs(os.path.dirname(final_path), exist_ok=True)

        relative_import = get_relative_import_path(final_path, base_schema_path)
        with open(final_path, 'w') as f:
            f.write(generate_imports() + f'import {{ UuidResourceSchema }} from "{relative_import}";\n\n' + schema)


if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodzify_api.settings')
    django.setup()
    generate_schemas()
