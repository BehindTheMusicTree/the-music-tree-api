# Django Upgrade Guide: 5.0.3 → 5.2.8

This guide provides step-by-step instructions to upgrade Django from version 5.0.3 to 5.2.8.

## Prerequisites

- Python 3.14 (as specified in project requirements)
- Virtual environment activated
- Database backup (recommended)
- Git branch for the upgrade work

## Step-by-Step Upgrade Process

### Step 1: Create a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b chore/upgrade-django-5.2.8
```

### Step 2: Review Current Dependencies

Check your current Django-related dependencies in `requirements.txt`:
- Django==5.0.3
- djangorestframework==3.15.1
- django-filter==22.1
- django-cors-headers==4.3.1
- django-extensions==3.2.1
- django-polymorphic==3.1.0
- django-model-utils==5.0.0
- django-stubs==5.1.1
- djangorestframework-stubs==3.15.1
- pytest-django==4.8.0

### Step 3: Check for Deprecation Warnings

Run your test suite with deprecation warnings enabled to identify any issues:

```bash
python -Wa manage.py test
```

Or with pytest:

```bash
python -Wa -m pytest
```

Note any deprecation warnings and address them before upgrading.

### Step 4: Update Django and Related Dependencies

Update `requirements.txt` with compatible versions:

**Core Django:**
- `Django==5.2.8` (upgrade from 5.0.3)

**Django-related packages that may need updates:**
- `django-stubs==5.2.1` (upgrade from 5.1.1 for Django 5.2 compatibility)
- `djangorestframework-stubs==3.15.1` (verify compatibility)

**Other dependencies to verify:**
- `asgiref` - Django 5.2 requires asgiref>=3.8.0
- `djangorestframework` - Verify compatibility with Django 5.2
- `django-filter` - Verify compatibility with Django 5.2
- `django-cors-headers` - Verify compatibility with Django 5.2
- `django-extensions` - Verify compatibility with Django 5.2
- `django-polymorphic` - Verify compatibility with Django 5.2
- `django-model-utils` - Verify compatibility with Django 5.2
- `pytest-django` - Verify compatibility with Django 5.2

### Step 5: Install Updated Dependencies

```bash
pip install --upgrade Django==5.2.8
pip install -r requirements.txt
```

Or update all at once:

```bash
pip install --upgrade -r requirements.txt
```

### Step 6: Verify Django Version

```bash
python manage.py --version
```

Should output: `5.2.8`

### Step 7: Run Database Migrations Check

Check if any new migrations are needed:

```bash
python manage.py makemigrations --dry-run
```

If migrations are needed, create them:

```bash
python manage.py makemigrations
```

### Step 8: Run Tests

Execute the full test suite:

```bash
pytest
```

Or with Django's test runner:

```bash
python manage.py test
```

Pay attention to:
- Test failures
- Deprecation warnings
- Import errors
- Database-related errors

### Step 9: Check for Breaking Changes

Review Django 5.2 release notes for breaking changes:
- [Django 5.2 Release Notes](https://docs.djangoproject.com/en/5.2/releases/5.2/)
- [Django 5.2.8 Release Notes](https://docs.djangoproject.com/en/5.2/releases/5.2.8/)

Common areas to check:
- Database backend compatibility
- Middleware changes
- Template system changes
- Admin interface changes
- Security settings

### Step 10: Update Settings (if needed)

Review `bodzify_api/settings.py` for any deprecated settings:

- Check `DATABASES` configuration (should be compatible)
- Verify `MIDDLEWARE` order (should be compatible)
- Review `INSTALLED_APPS` (should be compatible)
- Check security settings (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, etc.)

### Step 11: Test Application Manually

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Test critical functionality:
   - User authentication
   - API endpoints
   - File uploads
   - Database queries
   - Admin interface

### Step 12: Update Documentation

Update the following files if Django version is mentioned:
- `README.md` - Update Django version badge
- `CHANGELOG.md` - Add entry under `[Unreleased]` → `Changed`

### Step 13: Commit Changes

```bash
git add requirements.txt
git add CHANGELOG.md
git add README.md  # if updated
git commit -m "chore: upgrade Django to 5.2.8"
```

### Step 14: Create Pull Request

Create a PR targeting the `develop` branch with:
- Title: `chore: upgrade Django to 5.2.8`
- Description: Include summary of changes and test results
- Ensure all CI checks pass

## Post-Upgrade Checklist

- [ ] All tests pass
- [ ] No deprecation warnings
- [ ] Application starts without errors
- [ ] Database migrations applied successfully
- [ ] API endpoints working correctly
- [ ] Admin interface accessible
- [ ] File uploads working
- [ ] Authentication working
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

## Rollback Plan

If issues occur, rollback to previous version:

```bash
git checkout develop
pip install Django==5.0.3
pip install -r requirements.txt
python manage.py migrate
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Check if third-party packages are compatible with Django 5.2.8
2. **Database Errors**: Ensure database migrations are up to date
3. **Middleware Errors**: Verify middleware order and compatibility
4. **Template Errors**: Check template syntax compatibility
5. **Test Failures**: Review test code for deprecated features

### Getting Help

- Check [Django 5.2 Release Notes](https://docs.djangoproject.com/en/5.2/releases/5.2/)
- Review [Django Upgrade Guide](https://docs.djangoproject.com/en/5.2/howto/upgrade-version/)
- Check package documentation for compatibility information

## Notes

- Django 5.2.8 is a bugfix release, so breaking changes should be minimal
- Most Django 5.0 code should be compatible with Django 5.2
- Focus on testing to ensure everything works correctly
- Keep an eye on third-party package compatibility


