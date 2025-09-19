from .base import *
import os
import dj_database_url

# Production specific settings
DEBUG = False

# Secret key must be provided in environment
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is required in production")

# Hosts
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",") if os.environ.get("ALLOWED_HOSTS") else ["localhost"]

# Database - expect Render's DATABASE_URL or similar
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required in production")
DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# Security hardening
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Static files - WhiteNoise
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# If you need to trust the X-Forwarded-Proto header (when behind a proxy)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Add any production-only middleware tweaks here (base.py should already include WhiteNoise)

# Simple JWT production settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.environ.get('SIMPLE_JWT_SIGNING_KEY', os.environ.get('SECRET_KEY')),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
