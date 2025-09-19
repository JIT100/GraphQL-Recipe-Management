from .base import *
import os
from datetime import timedelta

# Development settings
DEBUG = True

# Default SECRET_KEY for local development only
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Local allowed hosts if not set in base
if not ALLOWED_HOSTS:
	ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Development DB: use dockerized Postgres via POSTGRES_* env vars
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get('POSTGRES_DB', 'recipe'),
		'USER': os.environ.get('POSTGRES_USER', 'admin'),
		'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'admin'),
		'HOST': os.environ.get('POSTGRES_HOST', 'db'),
		'PORT': os.environ.get('POSTGRES_PORT', '5432'),
	}
}

# Shorter token lifetime for development convenience
SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
}
