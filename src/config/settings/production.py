"""
Production settings for the Pixa project.
"""

import os

from .base import *


# ============================================================
# Production
# ============================================================

DEBUG = False


# ============================================================
# Security
# ============================================================

SECRET_KEY = os.environ['SECRET_KEY']


# ============================================================
# Allowed hosts
# ============================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ['ALLOWED_HOSTS'].split(',')
]


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ['CSRF_TRUSTED_ORIGINS'].split(',')
]


# ============================================================
# Database
# ============================================================

DATABASES = {
    'default': {
        'ENGINE': os.environ['DB_ENGINE'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': int(os.environ['DB_PORT']),
    },
}


# ============================================================
# Email
# ============================================================

MAILERS = {
    'default': {
        'BACKEND': os.environ['EMAIL_BACKEND'],
        'OPTIONS': {
            'host': os.environ['EMAIL_HOST'],
            'port': int(os.environ['EMAIL_PORT']),
            'use_tls': os.environ['EMAIL_USE_TLS'] == 'True',
            'username': os.environ['EMAIL_HOST_USER'],
            'password': os.environ['EMAIL_HOST_PASSWORD'],
        },
    },
}

DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']


# ============================================================
# HTTPS / Security
# ============================================================

SECURE_SSL_REDIRECT = (
    os.environ.get('SECURE_SSL_REDIRECT', 'False') == 'True'
)

SESSION_COOKIE_SECURE = (
    os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
)

CSRF_COOKIE_SECURE = (
    os.environ.get('CSRF_COOKIE_SECURE', 'False') == 'True'
)

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'


# ============================================================
# HTTPS behind Nginx / reverse proxy
# ============================================================

if os.environ.get('USE_HTTPS', 'False') == 'True':
    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https',
    )
