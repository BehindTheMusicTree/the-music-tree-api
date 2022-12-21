ALLOWED_HOSTS = [
    '127.0.0.1'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bodzify_api',
        'USER': 'django',
        'PASSWORD': 'G#uwM6&NW0!/',
        'HOST': 'localhost',
        'PORT': 5432,
        'DISABLE_SERVER_SIDE_CURSORS': True
    }
}
print('dev')