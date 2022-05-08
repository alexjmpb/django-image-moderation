"""
Custom settings file to run tests
"""
import os

INSTALLED_APPS = [
    'image_moderation',
    'tests',
]

IMAGE_MODERATION = {
    'AWS_ACCESS_KEY': os.getenv('AWS_ACCESS_KEY_ID'),
    'AWS_SECRET_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
