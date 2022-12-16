SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = [
    'bodzify.com',
    'www.bodzify.com',
    '185.224.139.218'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bodzify_api',
        'USER': 'django',
        'PASSWORD': ')}JkS|:KxR+b',
        'HOST': 'localhost',
        'PORT': 5432,
        'DISABLE_SERVER_SIDE_CURSORS': True
    }
}