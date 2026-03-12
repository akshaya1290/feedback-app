"""
Django Settings Configuration for Student Feedback System

This file contains the complete settings configuration needed.
Make sure to add 'feedback' app and 'corsheaders' when needed.
"""

# Add these to your existing settings.py

# ============================================================================
# ADD TO INSTALLED_APPS
# ============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Add these lines:
    'rest_framework',           # Django REST Framework
    'corsheaders',              # CORS support
    'feedback',                 # Our feedback app
]


# ============================================================================
# ADD TO MIDDLEWARE
# ============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware (before common middleware)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================================
# CORS CONFIGURATION (for frontend-backend communication)
# ============================================================================

# Allow requests from these origins
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    # Add production domains here
    # "https://yourdomain.com",
]

# Allow cross-origin requests with credentials
CORS_ALLOW_CREDENTIALS = True

# CSRF trusted origins (for form submissions)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Allow all HTTP methods
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


# ============================================================================
# REST FRAMEWORK CONFIGURATION
# ============================================================================

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Authentication settings
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    
    # Permissions (customize as needed)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Allow all for now, restrict later
    ],
    
    # JSON response format
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# *** SQLite (Development) ***
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# *** PostgreSQL (Production) ***
# Uncomment to use PostgreSQL and install: pip install psycopg2-binary
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'feedback_system',
        'USER': 'postgres',
        'PASSWORD': 'your_password_here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""

# *** MySQL/MariaDB ***
# Uncomment to use MySQL and install: pip install mysqlclient
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'feedback_system',
        'USER': 'root',
        'PASSWORD': 'your_password_here',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
"""


# ============================================================================
# SECURITY SETTINGS
# ============================================================================

# Development settings (CHANGE these for production!)
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']  # Restrict in production

# Secret key (generate a new one for production!)
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = 'django-insecure-development-key-change-in-production'

# HTTPS settings (uncomment for production)
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'feedback_system.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'feedback': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}


# ============================================================================
# EMAIL CONFIGURATION (for notifications)
# ============================================================================

# Development (console email backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production (SMTP configuration)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'
# DEFAULT_FROM_EMAIL = 'your-email@gmail.com'


# ============================================================================
# STATIC FILES AND MEDIA
# ============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Additional locations of static files
STATICFILES_DIRS = [
    BASE_DIR / 'frontend',  # Your frontend directory
]


# ============================================================================
# TIMEZONE AND INTERNATIONALIZATION
# ============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'  # Change to your timezone
USE_I18N = True
USE_TZ = True


# ============================================================================
# CUSTOM SETTINGS
# ============================================================================

# Maximum feedback comment length
MAX_COMMENT_LENGTH = 500

# Number of top/low courses to show in analytics
ANALYTICS_TOP_COURSES_COUNT = 5

# Negative feedback threshold (rating <= this value)
NEGATIVE_FEEDBACK_THRESHOLD = 2

# Notification threshold for instructors (negative feedback count >= this)
INSTRUCTOR_WARNING_THRESHOLD = 2


# ============================================================================
# ENVIRONMENT VARIABLES (Production)
# ============================================================================

# For production, use environment variables (install python-dotenv)
"""
import os
from decouple import config, Csv

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# CORS
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=Csv())
"""


# ============================================================================
# WSGI CONFIGURATION (for production servers)
# ============================================================================

WSGI_APPLICATION = 'feedback_project.wsgi.application'


# ============================================================================
# DEPLOYMENT CHECKLIST
# ============================================================================

"""
Before deploying to production:

1. ✓ Set DEBUG = False
2. ✓ Generate new SECRET_KEY
3. ✓ Configure ALLOWED_HOSTS with actual domain
4. ✓ Set up PostgreSQL (not SQLite)
5. ✓ Configure CORS_ALLOWED_ORIGINS with production domain
6. ✓ Enable HTTPS security settings
7. ✓ Configure email backend (SMTP)
8. ✓ Set up logging to files
9. ✓ Configure static files serving (whitenoise or nginx)
10. ✓ Run python manage.py collectstatic
11. ✓ Set up database backups
12. ✓ Configure error monitoring (Sentry, etc)
13. ✓ Use environment variables for secrets
14. ✓ Test with gunicorn locally: gunicorn feedback_project.wsgi
15. ✓ Configure web server (nginx/Apache)
"""